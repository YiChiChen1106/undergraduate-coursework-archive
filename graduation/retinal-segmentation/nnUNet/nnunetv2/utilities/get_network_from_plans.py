# import pydoc
# import warnings
# from typing import Union
#
# from nnunetv2.utilities.find_class_by_name import recursive_find_python_class
# from batchgenerators.utilities.file_and_folder_operations import join
#
#
# def get_network_from_plans(arch_class_name, arch_kwargs, arch_kwargs_req_import, input_channels, output_channels,
#                            allow_init=True, deep_supervision: Union[bool, None] = None):
#     network_class = arch_class_name
#     architecture_kwargs = dict(**arch_kwargs)
#     for ri in arch_kwargs_req_import:
#         if architecture_kwargs[ri] is not None:
#             architecture_kwargs[ri] = pydoc.locate(architecture_kwargs[ri])
#
#     nw_class = pydoc.locate(network_class)
#     # sometimes things move around, this makes it so that we can at least recover some of that
#     if nw_class is None:
#         warnings.warn(f'Network class {network_class} not found. Attempting to locate it within '
#                       f'dynamic_network_architectures.architectures...')
#         import dynamic_network_architectures
#         nw_class = recursive_find_python_class(join(dynamic_network_architectures.__path__[0], "architectures"),
#                                                network_class.split(".")[-1],
#                                                'dynamic_network_architectures.architectures')
#         if nw_class is not None:
#             print(f'FOUND IT: {nw_class}')
#         else:
#             raise ImportError('Network class could not be found, please check/correct your plans file')
#
#     if deep_supervision is not None:
#         architecture_kwargs['deep_supervision'] = deep_supervision
#
#     network = nw_class(
#         input_channels=input_channels,
#         num_classes=output_channels,
#         **architecture_kwargs
#     )
#
#     if hasattr(network, 'initialize') and allow_init:
#         network.apply(network.initialize)
#
#     return network
import pydoc
import warnings
from typing import Union
from nnunetv2.utilities.find_class_by_name import recursive_find_python_class
from batchgenerators.utilities.file_and_folder_operations import join

# --- 关键修改：手动导入你的 PA-Net 架构 ---
# 假设你按照之前的建议将 pa_net.py 放在了 nnunetv2/architecture/ 目录下
try:
    from nnunetv2.architecture.pa_net import PANet
except ImportError:
    PANet = None


# ---------------------------------------

def get_network_from_plans(arch_class_name, arch_kwargs, arch_kwargs_req_import, input_channels, output_channels,
                           allow_init=True, deep_supervision: Union[bool, None] = None):
    network_class = arch_class_name
    architecture_kwargs = dict(**arch_kwargs)

    for ri in arch_kwargs_req_import:
        if architecture_kwargs[ri] is not None:
            architecture_kwargs[ri] = pydoc.locate(architecture_kwargs[ri])

    # --- 关键修改逻辑：优先匹配自定义的 PANet ---
    if network_class == "PANet" or network_class.endswith(".PANet"):
        if PANet is not None:
            nw_class = PANet
        else:
            raise ImportError("PANet class found in plans but could not be imported from nnunetv2.architecture.pa_net")
    else:
        # 原有的定位逻辑
        nw_class = pydoc.locate(network_class)

        if nw_class is None:
            warnings.warn(f'Network class {network_class} not found. Attempting to locate it within '
                          f'dynamic_network_architectures.architectures...')
            import dynamic_network_architectures
            nw_class = recursive_find_python_class(join(dynamic_network_architectures.__path__[0], "architectures"),
                                                   network_class.split(".")[-1],
                                                   'dynamic_network_architectures.architectures')
            if nw_class is not None:
                print(f'FOUND IT: {nw_class}')
            else:
                raise ImportError('Network class could not be found, please check/correct your plans file')
    # ------------------------------------------

    if deep_supervision is not None:
        architecture_kwargs['deep_supervision'] = deep_supervision

    # 实例化 PA-Net 或其他网络
    # 注意：PA-Net 论文提到使用 LPT 捕获远程依赖 [cite: 16, 17]
    # 并使用 AFFM 替代跳跃连接以增强微血管识别 [cite: 18, 107]
    network = nw_class(
        input_channels=input_channels,
        num_classes=output_channels,
        **architecture_kwargs
    )

    if hasattr(network, 'initialize') and allow_init:
        network.apply(network.initialize)

    return network

if __name__ == "__main__":
    import torch

    model = get_network_from_plans(
        arch_class_name="dynamic_network_architectures.architectures.unet.ResidualEncoderUNet",
        arch_kwargs={
            "n_stages": 7,
            "features_per_stage": [32, 64, 128, 256, 512, 512, 512],
            "conv_op": "torch.nn.modules.conv.Conv2d",
            "kernel_sizes": [[3, 3], [3, 3], [3, 3], [3, 3], [3, 3], [3, 3], [3, 3]],
            "strides": [[1, 1], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2], [2, 2]],
            "n_blocks_per_stage": [1, 3, 4, 6, 6, 6, 6],
            "n_conv_per_stage_decoder": [1, 1, 1, 1, 1, 1],
            "conv_bias": True,
            "norm_op": "torch.nn.modules.instancenorm.InstanceNorm2d",
            "norm_op_kwargs": {"eps": 1e-05, "affine": True},
            "dropout_op": None,
            "dropout_op_kwargs": None,
            "nonlin": "torch.nn.LeakyReLU",
            "nonlin_kwargs": {"inplace": True},
        },
        arch_kwargs_req_import=["conv_op", "norm_op", "dropout_op", "nonlin"],
        input_channels=1,
        output_channels=4,
        allow_init=True,
        deep_supervision=True,
    )
    data = torch.rand((8, 1, 256, 256))
    target = torch.rand(size=(8, 1, 256, 256))
    outputs = model(data) # this should be a list of torch.Tensor