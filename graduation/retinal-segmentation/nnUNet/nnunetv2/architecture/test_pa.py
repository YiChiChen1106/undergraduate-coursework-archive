import torch
import torch.nn as nn

# 假设你已经把 pa_net.py 放在同级目录下
try:
    from pa_net import PANet
except ImportError:
    print("请确保 pa_net.py 在当前目录下")


def test_forward():
    print("开始测试 PA-Net 正向传播...")

    # 模拟 nnU-Net 传入的参数
    num_classes = 3
    input_channels = 1
    kwargs = {
        'n_stages': 4,
        'features_per_stage': [32, 64, 128, 256],
        'deep_supervision': True
    }

    try:
        # 实例化模型
        model = PANet(num_classes=num_classes, input_channels=input_channels, **kwargs)
        model.eval()

        # 创建一个 dummy input (Batch, Channel, H, W)
        # 注意：nnU-Net 2D 通常是 128x128 或更大
        dummy_input = torch.randn(1, input_channels, 128, 128)

        # 前向传播
        outputs = model(dummy_input)

        if kwargs['deep_supervision']:
            print(f"成功！检测到深监督开启，输出列表长度: {len(outputs)}")
            for i, out in enumerate(outputs):
                print(f"  - 输出层 {i} 尺寸: {out.shape}")
        else:
            print(f"成功！输出尺寸: {outputs.shape}")

    except Exception as e:
        print("\n[！！！测试失败！！！]")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {e}")
        print("\n提示：这通常是由于 Decoder 卷积层的输入通道计算错误导致的。")


if __name__ == "__main__":
    test_forward()