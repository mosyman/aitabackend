import os
import torch
import h5py
import numpy as np
import matplotlib.pyplot as plt

from model.networks.vit_seg_modeling import VisionTransformer as ViT_seg
from model.networks.vit_seg_modeling import CONFIGS as CONFIGS_ViT_seg
from model.datasets.dataset_ACDC import RandomGenerator


def load_model():
    # 1. 配置ViT模型参数
    config_vit = CONFIGS_ViT_seg['R50-ViT-B_16']  # 加载ResNet50骨干的ViT-Base模型配置
    config_vit.n_classes = 4  # 设置分割类别数（如背景+3种组织）
    config_vit.n_skip = 3  # 跳过特征融合的层数（用于U-Net风格的解码器）
    config_vit.patches.size = (16, 16)  # 图像patch大小，将224x224图像分割为14x14个patch
    config_vit.patches.grid = (14, 14)  # patch网格大小（224 / 16 = 14）

    # 2. 初始化模型并移至GPU
    # model = ViT_seg(config_vit, img_size=224, num_classes=config_vit.n_classes).cuda()
    # 2. 初始化模型（移除.cuda()调用）
    model = ViT_seg(config_vit, img_size=224, num_classes=config_vit.n_classes)

    # 3. 加载预训练权重
    # weights = torch.load("saved_weights/epoch_149.pth", map_location='cuda')  # 从第149轮训练保存的权重
    # 3. 加载预训练权重（修改map_location为cpu）
    weights = torch.load("model/saved_weights/epoch_149.pth", map_location='cpu')  # 从CPU加载权重
    model.load_state_dict(weights)  # 将权重加载到模型中

    # 4. 设置模型为评估模式
    model.eval()  # 关闭训练相关的层（如Dropout、BatchNorm）

    return model  # 返回加载好的模型


def run_inference_on_h5(h5_path, output_path):
    # 1. 加载预训练模型（见上一个代码块的解释）
    model = load_model()

    # 2. 从H5文件中读取图像数据
    with h5py.File(h5_path, 'r') as f:
        image = f['image'][:]  # 读取名为'image'的数据集

    # 3. 处理不同维度的输入图像
    if image.ndim == 3:  # 3D体积数据（如CT/MRI序列）
        slice_np = image[image.shape[0] // 2]  # 取中间切片
    elif image.ndim == 2:  # 2D单张图像
        slice_np = image
    else:
        raise ValueError(f"Unsupported image shape: {image.shape}")

    # 4. 数据预处理与增强
    sample = {"image": slice_np, "label": np.zeros_like(slice_np)}  # 创建样本字典（包含虚拟标签）
    transform = RandomGenerator(output_size=(224, 224))  # 初始化图像变换器，输出224×224大小
    processed = transform(sample)  # 应用变换（如归一化、裁剪、旋转等）

    # 5. 准备模型输入
    # input_tensor = processed['image'].unsqueeze(0).cuda()  # 添加批次维度并移至GPU
    # 5. 准备模型输入（移除.cuda()调用）
    input_tensor = processed['image'].unsqueeze(0)  # 添加批次维度
    # 输入张量形状：[1, 1, 224, 224]（批次大小=1，通道数=1，高度=224，宽度=224）

    # 6. 模型推理（禁用梯度计算以加速）
    with torch.no_grad():
        output = model(input_tensor)  # 模型输出形状：[1, 4, 224, 224]（4个类别）
        # 计算每个像素的类别概率并取最大值作为预测结果
        pred = torch.argmax(torch.softmax(output, dim=1), dim=1).squeeze(0).cpu().numpy()
        # 预测结果形状：[224, 224]（每个像素对应一个类别索引）

    # 7. 保存结果图像
    plt.imsave(output_path, pred, cmap='jet')  # 保存彩色分割图

    return "true"