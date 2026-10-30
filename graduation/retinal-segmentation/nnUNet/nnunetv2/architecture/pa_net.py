import torch
import torch.nn as nn
import torch.nn.functional as F


# ================= clDice 核心算法 (建议放在 pa_net.py 顶部) =================

def soft_erode(img):
    if len(img.shape)==4:
        p1 = -F.max_pool2d(-img, (3,1), (1,1), (1,0))
        p2 = -F.max_pool2d(-p1, (1,3), (1,1), (0,1))
        return p2
    # 兼容 3D (针对 nnU-Net 的通用性)
    elif len(img.shape)==5:
        p1 = -F.max_pool3d(-img, (3,1,1), (1,1,1), (1,0,0))
        p2 = -F.max_pool3d(-p1, (1,3,1), (1,1,1), (0,1,0))
        p3 = -F.max_pool3d(-p2, (1,1,3), (1,1,1), (0,0,1))
        return p3

def soft_dilate(img):
    if len(img.shape)==4:
        return F.max_pool2d(img, (3,3), (1,1), (1,1))
    elif len(img.shape)==5:
        return F.max_pool3d(img, (3,3,3), (1,1,1), (1,1,1))

def soft_open(img):
    return soft_dilate(soft_erode(img))

def soft_skel(img, iter_):
    img_mans = img
    for _ in range(iter_):
        img_erode = soft_erode(img)
        img_open = soft_open(img_erode)
        delta = F.relu(img_erode - img_open)
        img_mans = torch.max(img_mans, delta)
        img = img_erode
    return img_mans

class SoftclDiceLoss(nn.Module):
    def __init__(self, iter_=3, smooth=1.):
        super(SoftclDiceLoss, self).__init__()
        self.iter = iter_
        self.smooth = smooth

    def forward(self, y_pred, y_true):
        """
        注意：nnU-Net 传入的 y_true 通常是 one-hot 或包含 class 索引。
        眼底分割通常是 0(背景) 和 1(血管)。
        """
        # 如果 y_true 是类别索引，转换为 one-hot 概率图
        if len(y_true.shape) != len(y_pred.shape):
            y_true = F.one_hot(y_true.long(), y_pred.shape[1]).permute(0, 3, 1, 2).float()
            
        skel_true = soft_skel(y_true, self.iter)
        skel_pred = soft_skel(y_pred, self.iter)
        
        # 只计算血管类（通道1）的重叠
        tprec = (torch.sum(torch.multiply(skel_pred[:, 1:], y_true[:, 1:])) + self.smooth) / (torch.sum(skel_pred[:, 1:]) + self.smooth)    
        tsens = (torch.sum(torch.multiply(skel_true[:, 1:], y_pred[:, 1:])) + self.smooth) / (torch.sum(skel_true[:, 1:]) + self.smooth)    
        
        return 1.0 - 2.0 * (tprec * tsens) / (tprec + tsens)


class PANetCombinedLoss(nn.Module):
    def __init__(self, base_loss, cldice_weight=0.3, iter_=3):
        """
        base_loss: nnU-Net 默认的 DC_and_CE_loss (DeepSupervisionWrapper)
        cldice_weight: clDice 的权重，建议 0.3
        iter_: 骨架提取的迭代次数
        """
        super().__init__()
        self.base_loss = base_loss
        self.cldice = SoftclDiceLoss(iter_=iter_)
        self.w = cldice_weight

    def forward(self, prediction, target):
        # 1. 计算 nnU-Net 标准的深监督 Dice + CE Loss
        l_base = self.base_loss(prediction, target)
        
        # 2. 提取最高分辨率层的预测值和真值进行 clDice 计算
        # 在 nnU-Net 中，训练模式下预测值是一个 list
        if isinstance(prediction, (list, tuple)):
            # 对主输出层做 Sigmoid 归一化到 [0, 1]
            p0 = torch.sigmoid(prediction[0])
            t0 = target[0]
        else:
            p0 = torch.sigmoid(prediction)
            t0 = target
            
        # 3. 计算拓扑损失
        l_cl = self.cldice(p0, t0)
        
        # 返回加权总和
        return l_base + self.w * l_cl

# ================= 基础模块定义 =================



class LFAU(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.dw_conv = nn.Conv2d(channels, channels, kernel_size=3, padding=1, groups=channels)

    def forward(self, x):
        return self.dw_conv(x) + x


class GatedAxialAttention(nn.Module):
    def __init__(self, channels, heads=8, dim_head=16, axis='width'):
        super().__init__()
        self.heads, self.dim_head, self.axis = heads, dim_head, axis
        inner_dim = heads * dim_head
        self.to_qkv = nn.Conv2d(channels, inner_dim * 3, kernel_size=1, bias=False)
        self.to_out = nn.Conv2d(inner_dim, channels, kernel_size=1)

    def forward(self, x):
        b, c, h, w = x.shape
        qkv = self.to_qkv(x).chunk(3, dim=1)
        q, k, v = map(lambda t: t.view(b, self.heads, self.dim_head, h, w), qkv)
        if self.axis == 'width':
            q, k = q.permute(0, 1, 3, 4, 2), k.permute(0, 1, 3, 2, 4)
            dots = torch.matmul(q, k) * (self.dim_head ** -0.5)
            attn = dots.softmax(dim=-1)
            v = v.permute(0, 1, 3, 4, 2)
            out = torch.matmul(attn, v).permute(0, 1, 4, 2, 3).contiguous()
        else:
            q, k = q.permute(0, 1, 4, 3, 2), k.permute(0, 1, 4, 2, 3)
            dots = torch.matmul(q, k) * (self.dim_head ** -0.5)
            attn = dots.softmax(dim=-1)
            v = v.permute(0, 1, 4, 3, 2)
            out = torch.matmul(attn, v).permute(0, 1, 4, 3, 2).contiguous()
        return self.to_out(out.view(b, -1, h, w))


class EPA(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.gaa_w = GatedAxialAttention(channels, axis='width')
        self.gaa_h = GatedAxialAttention(channels, axis='height')
        self.dw_conv = nn.Conv2d(channels, channels, kernel_size=3, padding=1, groups=channels)
        self.gelu = nn.GELU()

    def forward(self, x):
        gaa_out = self.gaa_h(self.gaa_w(x))
        return self.gelu(gaa_out + self.dw_conv(x)) + x


class CFFN(nn.Module):
    def __init__(self, channels, expansion=4):
        super().__init__()
        inner_dim = channels * expansion
        self.net = nn.Sequential(
            nn.Conv2d(channels, inner_dim, 1),
            nn.Conv2d(inner_dim, inner_dim, 3, padding=1, groups=inner_dim),
            nn.Conv2d(inner_dim, channels, 1)
        )

    def forward(self, x):
        return self.net(x) + x


class LPT(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.lfau, self.epa, self.cffn = LFAU(channels), EPA(channels), CFFN(channels)

    def forward(self, x):
        return self.cffn(self.epa(self.lfau(x)))


class AFFM(nn.Module):
    def __init__(self, in_channels_list, out_channels):
        super().__init__()
        self.convs = nn.ModuleList([nn.Conv2d(c, out_channels, 1) for c in in_channels_list])
        self.to_weights = nn.Sequential(
            nn.Conv2d(out_channels * len(in_channels_list), len(in_channels_list), 1),
            nn.Softmax(dim=1)
        )

    def forward(self, f_list, f0):
        target_res = f0.shape[2:]
        processed = [F.interpolate(self.convs[i](f), size=target_res, mode='bilinear', align_corners=False) for i, f in
                     enumerate(f_list)]
        weights = self.to_weights(torch.cat(processed, dim=1))
        f_fusion = sum([processed[i] * weights[:, i:i + 1, :, :] for i in range(len(processed))])
        return torch.cat([f_fusion, f0], dim=1)


class ConvBlock(nn.Module):
    def __init__(self, in_ch, out_ch, dropout_p=0.2):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1, bias=False), nn.BatchNorm2d(out_ch),
            nn.GELU(), nn.Dropout(dropout_p),
            nn.Conv2d(out_ch, out_ch, 3, padding=1, bias=False), nn.BatchNorm2d(out_ch),
            nn.GELU(), nn.Dropout(dropout_p)
        )

    def forward(self, x): return self.block(x)


# ================= 主架构定义 =================

class PANet(nn.Module):
    def __init__(self, num_classes, input_channels=1, **kwargs):
        super().__init__()
        self.n_stages = kwargs.get('n_stages', 4)
        features = kwargs.get('features_per_stage', [32, 64, 128, 256])
        self.deep_supervision = kwargs.get('deep_supervision', False)

        # Encoder
        self.encoder, self.downsamples = nn.ModuleList(), nn.ModuleList()
        curr_ch = input_channels
        for i in range(self.n_stages - 1):
            self.encoder.append(ConvBlock(curr_ch, features[i]))
            self.downsamples.append(nn.MaxPool2d(2))
            curr_ch = features[i]

        # Bottleneck
        self.bottleneck_conv = ConvBlock(curr_ch, features[-1])
        self.lpt = LPT(features[-1])

        # Decoder
        self.decoder, self.upsamples, self.affms = nn.ModuleList(), nn.ModuleList(), nn.ModuleList()
        prev_ch = features[-1]

        for i in range(self.n_stages - 2, -1, -1):
            self.upsamples.append(nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False))
            self.affms.append(AFFM(features[:self.n_stages - 1], features[i]))
            self.decoder.append(ConvBlock(features[i] + prev_ch, features[i]))
            prev_ch = features[i]

        self.final_conv = nn.Conv2d(features[0], num_classes, 1)

        self.seg_heads = nn.ModuleList([
            nn.Conv2d(features[i], num_classes, 1)
            for i in range(1, self.n_stages - 1)
        ])

    def forward(self, x):
        enc_outs = []
        curr = x
        for i in range(self.n_stages - 1):
            curr = self.encoder[i](curr)
            enc_outs.append(curr)
            curr = self.downsamples[i](curr)

        curr = self.lpt(self.bottleneck_conv(curr))

        ds_outs = []
        for i in range(self.n_stages - 1):
            curr = self.upsamples[i](curr)
            curr = self.affms[i](enc_outs, curr)
            curr = self.decoder[i](curr)

            # 只有在明确开启深监督时才收集辅助输出，节省计算资源
            if getattr(self, 'deep_supervision', False) and i < self.n_stages - 2:
                ds_outs.append(self.seg_heads[-(i + 1)](curr))

        out = self.final_conv(curr)

        # --- 核心防御逻辑：适配 NoDS 实验 ---
        # 1. 物理检查：如果 deep_supervision 开关没开，无论什么模式都只返回单 Tensor
        if not getattr(self, 'deep_supervision', False):
            return out

        # 2. 只有开启了开关，且在训练模式下，才返回 List 供深监督包装器使用
        if self.training:
            # 确保辅助输出存在，否则退回到单 Tensor
            return [out] + ds_outs[::-1] if ds_outs else out

        # 3. 验证或测试模式返回单 Tensor
        return out


class PANet_LPTOnly(PANet):
    def forward(self, x):
        enc_outs = []
        curr = x
        for i in range(self.n_stages - 1):
            curr = self.encoder[i](curr)
            enc_outs.append(curr)
            curr = self.downsamples[i](curr)

        curr = self.lpt(self.bottleneck_conv(curr))

        ds_outs = []
        for i in range(self.n_stages - 1):
            curr = self.upsamples[i](curr)
            skip_connection = enc_outs[-(i + 1)]
            curr = torch.cat([skip_connection, curr], dim=1)
            curr = self.decoder[i](curr)

            # 同步防御逻辑
            if getattr(self, 'deep_supervision', False) and i < self.n_stages - 2:
                ds_outs.append(self.seg_heads[-(i + 1)](curr))

        out = self.final_conv(curr)

        # --- 子类也必须同步防御逻辑，防止消融实验崩溃 ---
        if not getattr(self, 'deep_supervision', False):
            return out

        if self.training:
            return [out] + ds_outs[::-1] if ds_outs else out

        return out

#
# import torch
# import torch.nn as nn
# import torch.nn.functional as F


class DeformableAttention(nn.Module):
    def __init__(self, channels, heads=8, n_points=4):  # 1. 调回 4 点
        super().__init__()
        self.heads = heads
        self.n_points = n_points
        self.dim_head = channels // heads

        # 2. 输出通道改为 heads * n_points * 3 (2个坐标偏移 + 1个掩码权重)
        self.offset_mask_conv = nn.Conv2d(channels, heads * n_points * 3, kernel_size=3, padding=1)
        self.attn_weights = nn.Conv2d(channels, heads * n_points, kernel_size=3, padding=1)
        self.to_out = nn.Conv2d(channels, channels, kernel_size=1)

    def forward(self, x):
        b, c, h, w = x.shape

        # 生成基础网格
        grid_y, grid_x = torch.meshgrid(
            torch.linspace(-1, 1, h, device=x.device, dtype=x.dtype),
            torch.linspace(-1, 1, w, device=x.device, dtype=x.dtype),
            indexing='ij'
        )
        grid = torch.stack([grid_x, grid_y], dim=-1).unsqueeze(0).contiguous()

        # 3. 预测偏移和掩码
        out_conv = self.offset_mask_conv(x)
        # 将输出拆分为偏移量(offsets)和掩码(masks)
        o1, o2, mask = torch.chunk(out_conv, 3, dim=1)

        # 偏移量处理
        offsets = torch.cat([o1, o2], dim=1).permute(0, 2, 3, 1).reshape(b, h, w, self.heads, self.n_points, 2)
        offsets = torch.tanh(offsets) * (10.0 / max(h, w))
        sampling_locations = grid.view(1, h, w, 1, 1, 2) + offsets

        # 4. 掩码处理：使用 Sigmoid 限制在 [0, 1] 之间
        mask = torch.sigmoid(mask).reshape(b, self.heads, self.n_points, h, w)
        mask = mask.permute(0, 1, 3, 4, 2).reshape(b * self.heads, h * w, 1, self.n_points)

        # 5. 采样逻辑 (Grouped Sampling)
        v = x.reshape(b * self.heads, self.dim_head, h, w).contiguous()
        sampling_locations = sampling_locations.reshape(b * self.heads, h * w, self.n_points, 2).contiguous()
        sampled_feat = F.grid_sample(v, sampling_locations, mode='bilinear', padding_mode='zeros', align_corners=False)

        # 6. 计算注意力权重
        attn = self.attn_weights(x).reshape(b, self.heads, self.n_points, h, w)
        attn = attn.permute(0, 1, 3, 4, 2).reshape(b * self.heads, h * w, 1, self.n_points)
        attn = torch.softmax(attn, dim=-1)

        # 7. 【核心改动】同时应用注意力权重和调制掩码
        # 最终权重 = 注意力分数 * 调制掩码
        final_attn = attn * mask

        sampled_feat = sampled_feat.permute(0, 2, 3, 1).contiguous()
        out = torch.matmul(final_attn, sampled_feat)

        out = out.reshape(b, self.heads, h, w, self.dim_head).permute(0, 1, 4, 2, 3).reshape(b, c, h, w).contiguous()
        return self.to_out(out)


# 更新后的 EPA，使用可变形注意力替换 GAA
class EPA_Deformable(nn.Module):
    def __init__(self, channels):
        super().__init__()
        # 用一个可变形注意力层覆盖全局几何感知
        self.deform_attn = DeformableAttention(channels)
        self.dw_conv = nn.Conv2d(channels, channels, kernel_size=3, padding=1, groups=channels)
        self.gelu = nn.GELU()

    def forward(self, x):
        # 这里的逻辑对应论文 EPA 的并行结构 [cite: 102, 241]
        attn_out = self.deform_attn(x)
        return self.gelu(attn_out + self.dw_conv(x)) + x


# 更新 LPT 结构
class LPT_Deformable(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.lfau = LFAU(channels)  # 保持局部特征接收 [cite: 102]
        self.epa = EPA_Deformable(channels)
        self.cffn = CFFN(channels)

    def forward(self, x):
        return self.cffn(self.epa(self.lfau(x)))


# 消融版本模型：No AFFM + Deformable LPT
class PANet_DeformableLPT_NoAFFM(PANet):
    def __init__(self, num_classes, input_channels=1, **kwargs):
        super().__init__(num_classes, input_channels, **kwargs)
        # 重新初始化 LPT 为可变形版本
        features = kwargs.get('features_per_stage', [32, 64, 128, 256])
        self.lpt = LPT_Deformable(features[-1])

    def forward(self, x):
        enc_outs = []
        curr = x
        for i in range(self.n_stages - 1):
            curr = self.encoder[i](curr)
            enc_outs.append(curr)
            curr = self.downsamples[i](curr)

        curr = self.lpt(self.bottleneck_conv(curr))

        ds_outs = []
        for i in range(self.n_stages - 1):
            curr = self.upsamples[i](curr)
            # 只有这里变了：用 cat 代替 AFFM
            skip = enc_outs[-(i + 1)]
            curr = torch.cat([skip, curr], dim=1)
            curr = self.decoder[i](curr)

            # --- 关键修复：把深监督辅助头逻辑接回来 ---
            if getattr(self, 'deep_supervision', False) and i < self.n_stages - 2:
                ds_outs.append(self.seg_heads[-(i + 1)](curr))

        out = self.final_conv(curr)

        # === 修复后的防御逻辑 ===
        # 1. 如果完全不想要深监督（推理模式或显式关闭）
        if not getattr(self, 'deep_supervision', False) and not self.training:
            return out

        # 2. 训练模式下，nnU-Net 必须接收 List
        if self.training:
            # 即使 ds_outs 为空，也要返回 [out]，确保与 target 的 list 格式对齐
            return [out] + ds_outs[::-1] if ds_outs else [out]

        # 3. 验证模式
        return out


# ================= 完全体：可变形 LPT + AFFM =================

class PANet_DeformableLPT_Full(PANet):
    def __init__(self, num_classes, input_channels=1, **kwargs):
        # 显式开启深监督，因为基类 PANet 需要它来初始化辅助头 [cite: 539]
        if 'deep_supervision' not in kwargs:
            kwargs['deep_supervision'] = True

        super().__init__(num_classes, input_channels, **kwargs)

        # 获取特征维度
        features = kwargs.get('features_per_stage', [32, 64, 128, 256])

        # 核心修改：将 bottleneck 处的 LPT 替换为可变形版本
        # 此时 self.affms 已经在父类的 super().__init__ 中初始化完成了 [cite: 168]
        self.lpt = LPT_Deformable(features[-1])

    # 注意：这里不需要重写 forward 函数！
    # 因为父类 PANet 的 forward 已经包含了完整的 AFFM 融合逻辑 [cite: 174]


class MultiScaleDeformableAttention(nn.Module):
    def __init__(self, query_channels, key_channels_list, heads=8, n_points=4):
        super().__init__()
        self.heads = heads
        self.n_points = n_points
        self.n_levels = len(key_channels_list)
        self.dim_head = query_channels // heads

        # 1. 映射各层特征到统一维度 (Query 维度)
        self.value_projs = nn.ModuleList([
            nn.Conv2d(c, query_channels, kernel_size=1) for c in key_channels_list
        ])

        # 2. 预测偏移和掩码：为每一层特征预测独立的 4 个采样点
        # 输出通道：heads * n_levels * n_points * 3 (x, y, mask)
        self.offset_mask_conv = nn.Conv2d(query_channels, heads * self.n_levels * n_points * 3, kernel_size=3,
                                          padding=1)
        self.attn_weights = nn.Conv2d(query_channels, heads * self.n_levels * n_points, kernel_size=3, padding=1)
        self.to_out = nn.Conv2d(query_channels, query_channels, kernel_size=1)

    def forward(self, x, feat_list):
        # x: [B, C, H, w] (来自 Bottleneck)
        # feat_list: List of [B, Ci, Hi, Wi] (来自 Encoder 各层)
        b, c, h, w = x.shape

        # 预测总偏移、掩码和权重
        out_conv = self.offset_mask_conv(x)
        o1, o2, mask = torch.chunk(out_conv, 3, dim=1)

        # 整理偏移 [B, H, W, heads, n_levels, n_points, 2]
        offsets = torch.cat([o1, o2], dim=1).permute(0, 2, 3, 1).reshape(b, h, w, self.heads, self.n_levels,
                                                                         self.n_points, 2)
        offsets = torch.tanh(offsets) * 0.1

        # 整理掩码 [B, heads, n_levels, n_points, H, W]
        mask = torch.sigmoid(mask).reshape(b, self.heads, self.n_levels, self.n_points, h, w)

        # 整理注意力权重 [B, heads, n_levels, n_points, H, W]
        attn = self.attn_weights(x).reshape(b, self.heads, self.n_levels, self.n_points, h, w)
        attn = torch.softmax(attn.reshape(b, self.heads, -1, h, w), dim=2).reshape(b, self.heads, self.n_levels,
                                                                                   self.n_points, h, w)

        # 基础网格 (Query 分辨率)
        grid_y, grid_x = torch.meshgrid(
            torch.linspace(-1, 1, h, device=x.device, dtype=x.dtype),
            torch.linspace(-1, 1, w, device=x.device, dtype=x.dtype),
            indexing='ij'
        )
        grid = torch.stack([grid_x, grid_y], dim=-1).unsqueeze(0)  # [1, H, W, 2]

        aggregated_feat = 0
        for i, feat in enumerate(feat_list):
            # 投影当前层特征到统一维度
            v = self.value_projs[i](feat)
            _, _, v_h, v_w = v.shape

            # 计算在该层的采样坐标
            # 虽然各层分辨率不同，但 grid_sample 使用归一化坐标 (-1 to 1)
            level_offsets = offsets[:, :, :, :, i, :, :]  # [B, H, W, heads, n_points, 2]
            sampling_locs = grid.view(1, h, w, 1, 1, 2) + level_offsets

            # 分组采样
            v_grouped = v.reshape(b * self.heads, self.dim_head, v_h, v_w).contiguous()
            locs_grouped = sampling_locs.reshape(b * self.heads, h * w, self.n_points, 2).contiguous()
            sampled = F.grid_sample(v_grouped, locs_grouped, mode='bilinear', padding_mode='zeros', align_corners=False)

            # 计算当前层的权重并应用
            level_weight = (attn[:, :, i, :, :, :] * mask[:, :, i, :, :, :]).permute(0, 1, 3, 4, 2)
            level_weight = level_weight.reshape(b * self.heads, h * w, 1, self.n_points)

            sampled = sampled.permute(0, 2, 3, 1).contiguous()
            out_level = torch.matmul(level_weight, sampled)
            aggregated_feat += out_level.reshape(b, self.heads, h, w, self.dim_head).permute(0, 1, 4, 2, 3).reshape(b,
                                                                                                                    c,
                                                                                                                    h,
                                                                                                                    w)

        return self.to_out(aggregated_feat)


# 更新适配器
class EPA_MSDeformable(nn.Module):
    def __init__(self, query_channels, key_channels_list):
        super().__init__()
        self.ms_deform_attn = MultiScaleDeformableAttention(query_channels, key_channels_list)
        self.dw_conv = nn.Conv2d(query_channels, query_channels, kernel_size=3, padding=1, groups=query_channels)
        self.gelu = nn.GELU()

    def forward(self, x, feat_list):
        attn_out = self.ms_deform_attn(x, feat_list)
        return self.gelu(attn_out + self.dw_conv(x)) + x

class CoordAtt(nn.Module):
    def __init__(self, inp, oup, reduction=32):
        super(CoordAtt, self).__init__()
        self.pool_h = nn.AdaptiveAvgPool2d((None, 1))
        self.pool_w = nn.AdaptiveAvgPool2d((1, None))
        mip = max(8, inp // reduction)
        self.conv1 = nn.Conv2d(inp, mip, kernel_size=1, stride=1, padding=0)
        # 将 BatchNorm2d 换成 InstanceNorm2d，它对小 batch 极其鲁棒
        self.bn1 = nn.InstanceNorm2d(mip)
        self.act = nn.GELU()
        self.conv_h = nn.Conv2d(mip, oup, kernel_size=1, stride=1, padding=0)
        self.conv_w = nn.Conv2d(mip, oup, kernel_size=1, stride=1, padding=0)

    def forward(self, x):
        n, c, h, w = x.size()
        x_h = self.pool_h(x)
        x_w = self.pool_w(x).permute(0, 1, 3, 2)
        y = torch.cat([x_h, x_w], dim=2)
        y = self.act(self.bn1(self.conv1(y)))
        x_h, x_w = torch.split(y, [h, w], dim=2)
        x_w = x_w.permute(0, 1, 3, 2)
        a_h = self.conv_h(x_h).sigmoid()
        a_w = self.conv_w(x_w).sigmoid()
        return x * a_w * a_h


class LPT_MSDeformable(nn.Module):
    def __init__(self, query_channels, key_channels_list):
        super().__init__()
        # 在入口处加入 CA 增强
        self.ca = CoordAtt(query_channels, query_channels)
        self.lfau = LFAU(query_channels)
        self.epa = EPA_MSDeformable(query_channels, key_channels_list)
        self.cffn = CFFN(query_channels)

    def forward(self, x, feat_list):
        # 先经过坐标注意力，再进行局部特征提取和多尺度采样
        x = self.ca(x)
        return self.cffn(self.epa(self.lfau(x), feat_list))


# 新模型：多尺度可变形 LPT (No AFFM)
class PANet_MSDeformableLPT_NoAFFM(PANet):
    def __init__(self, num_classes, input_channels=1, **kwargs):
        super().__init__(num_classes, input_channels, **kwargs)
        features = kwargs.get('features_per_stage', [32, 64, 128, 256])
        # 传入所有 Encoder 层和 Bottleneck 层的通道列表
        self.lpt = LPT_MSDeformable(features[-1], features)

    def forward(self, x):
        enc_outs = []
        curr = x
        for i in range(self.n_stages - 1):
            curr = self.encoder[i](curr)
            enc_outs.append(curr)
            curr = self.downsamples[i](curr)

        # 瓶颈层：不仅输入当前特征，还传入所有 Encoder 特征
        bottleneck_feat = self.bottleneck_conv(curr)
        # 将 enc_outs 和当前 bottleneck_feat 组合成多尺度列表
        ms_feat_list = enc_outs + [bottleneck_feat]
        curr = self.lpt(bottleneck_feat, ms_feat_list)

        ds_outs = []
        for i in range(self.n_stages - 1):
            curr = self.upsamples[i](curr)
            skip = enc_outs[-(i + 1)]
            curr = torch.cat([skip, curr], dim=1)
            curr = self.decoder[i](curr)
            if getattr(self, 'deep_supervision', False) and i < self.n_stages - 2:
                ds_outs.append(self.seg_heads[-(i + 1)](curr))

        out = self.final_conv(curr)

        # === 核心修复逻辑 ===
        # 1. 只有在训练模式（self.training=True）且开启了深监督时，才返回 List
        if self.training and getattr(self, 'deep_supervision', False):
            return [out] + ds_outs[::-1] if ds_outs else [out]

        # 2. 在验证（Validation）或推理（Predict）阶段，必须只返回主输出 Tensor
        return out

    # 将现有的多尺度模型重命名或指向 Trainer 期待的名字

# 将现有的多尺度模型重命名或指向 Trainer 期待的名字
class PANet_MSDeformableLPT_CA_NoAFFM(PANet_MSDeformableLPT_NoAFFM):
    def __init__(self, num_classes, input_channels=1, **kwargs):
        super().__init__(num_classes, input_channels, **kwargs)

class MultiScaleSnakeAttention(nn.Module):
    def __init__(self, query_channels, key_channels_list, heads=8, n_points=9): # 建议增至9点以体现蛇形连续性
        super().__init__()
        self.heads = heads
        self.n_points = n_points
        self.n_levels = len(key_channels_list)
        self.dim_head = query_channels // heads

        self.value_projs = nn.ModuleList([
            nn.Conv2d(c, query_channels, kernel_size=1) for c in key_channels_list
        ])

        # 预测序列偏移：不再是独立的 x,y，而是迭代的增量 delta
        self.offset_conv = nn.Conv2d(query_channels, heads * self.n_levels * n_points, kernel_size=3, padding=1)
        self.mask_conv = nn.Conv2d(query_channels, heads * self.n_levels * n_points, kernel_size=3, padding=1)
        self.attn_weights = nn.Conv2d(query_channels, heads * self.n_levels * n_points, kernel_size=3, padding=1)
        self.to_out = nn.Conv2d(query_channels, query_channels, kernel_size=1)

    def forward(self, x, feat_list):
        b, c, h, w = x.shape
        
        # 1. 预测与整理
        delta_offsets = torch.tanh(self.offset_conv(x)) * 0.1 
        mask = torch.sigmoid(self.mask_conv(x)).reshape(b, self.heads, self.n_levels, self.n_points, h, w)
        attn = torch.softmax(self.attn_weights(x).reshape(b, self.heads, -1, h, w), dim=2).reshape(b, self.heads, self.n_levels, self.n_points, h, w)

        # 2. 构造蛇形轨迹
        grid_y, grid_x = torch.meshgrid(
            torch.linspace(-1, 1, h, device=x.device, dtype=x.dtype),
            torch.linspace(-1, 1, w, device=x.device, dtype=x.dtype),
            indexing='ij'
        )
        base_grid = torch.stack([grid_x, grid_y], dim=-1).unsqueeze(0) # [1, H, W, 2]

        delta_offsets = delta_offsets.reshape(b, self.heads, self.n_levels, self.n_points, h, w)
        cum_offsets_y = torch.cumsum(delta_offsets, dim=3) 
        # 修正：确保类型一致
        cum_offsets_x = torch.arange(self.n_points, device=x.device, dtype=x.dtype).view(1, 1, 1, self.n_points, 1, 1) * (2.0 / w)

        aggregated_feat = 0
        for i, feat in enumerate(feat_list):
            v = self.value_projs[i](feat)
            _, _, v_h, v_w = v.shape
            
            # === 修正维度不匹配的核心位置 ===
            # 切片后为 5 维，对应的 permute 索引应为 (0, 3, 4, 1, 2)
            level_off_y = cum_offsets_y[:, :, i].permute(0, 3, 4, 1, 2) # (B, H, W, heads, points)
            level_off_x = cum_offsets_x.expand(b, self.heads, self.n_levels, self.n_points, h, w)[:, :, i].permute(0, 3, 4, 1, 2)
            
            sampling_locs = base_grid.view(1, h, w, 1, 1, 2) + torch.stack([level_off_x, level_off_y], dim=-1)
            
            # 3. 采样与权重聚合
            v_grouped = v.reshape(b * self.heads, self.dim_head, v_h, v_w).contiguous()
            locs_grouped = sampling_locs.reshape(b * self.heads, h * w, self.n_points, 2).contiguous()
            sampled = F.grid_sample(v_grouped, locs_grouped, mode='bilinear', padding_mode='zeros', align_corners=False)
            
            # 对应修正权重张量的维度
            m_attn = (attn[:, :, i] * mask[:, :, i]).permute(0, 1, 3, 4, 2).reshape(b * self.heads, h * w, 1, self.n_points)
            sampled = sampled.permute(0, 2, 3, 1).contiguous()
            
            aggregated_feat += torch.matmul(m_attn, sampled).reshape(b, self.heads, h, w, self.dim_head).permute(0, 1, 4, 2, 3).reshape(b, c, h, w)

        return self.to_out(aggregated_feat)
    
# 在 MultiScaleSnakeAttention 类定义之后添加
class EPA_MSDSConv(nn.Module):
    def __init__(self, query_channels, key_channels_list):
        super().__init__()
        # 使用你定义的蛇形版本
        self.ms_snake_attn = MultiScaleSnakeAttention(query_channels, key_channels_list)
        self.dw_conv = nn.Conv2d(query_channels, query_channels, kernel_size=3, padding=1, groups=query_channels)
        self.gelu = nn.GELU()

    def forward(self, x, feat_list):
        # 并行分支融合：蛇形注意力捕捉拓扑 + DW-Conv 捕捉局部细节
        attn_out = self.ms_snake_attn(x, feat_list)
        return self.gelu(attn_out + self.dw_conv(x)) + x

class LPT_MSDSConv_CA(nn.Module):
    def __init__(self, query_channels, key_channels_list):
        super().__init__()
        self.ca = CoordAtt(query_channels, query_channels) # 保留之前表现优异的 CA
        self.lfau = LFAU(query_channels)
        self.epa = EPA_MSDSConv(query_channels, key_channels_list) # 使用蛇形版本
        self.cffn = CFFN(query_channels)

    def forward(self, x, feat_list):
        x = self.ca(x)
        return self.cffn(self.epa(self.lfau(x), feat_list))

class PANet_MSDSConvLPT_CA_NoAFFM(PANet_MSDeformableLPT_CA_NoAFFM):
    def __init__(self, num_classes, input_channels=1, **kwargs):
        super().__init__(num_classes, input_channels, **kwargs)
        features = kwargs.get('features_per_stage', [32, 64, 128, 256])
        # 替换为蛇形 LPT
        self.lpt = LPT_MSDSConv_CA(features[-1], features)


