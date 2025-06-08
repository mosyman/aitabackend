import os
import h5py
import numpy as np
import torch
from torch.utils.data import Dataset
import random
from scipy.ndimage import rotate, zoom


def random_rot_flip(image, label):
    """随机旋转90度的倍数并翻转图像和标签"""
    k = np.random.randint(0, 4)  # 随机选择旋转90度的次数
    image = np.rot90(image, k)  # 旋转图像
    label = np.rot90(label, k)  # 同步旋转标签

    axis = np.random.randint(0, 2)  # 随机选择翻转轴
    image = np.flip(image, axis=axis).copy()  # 翻转图像并复制以确保内存连续性
    label = np.flip(label, axis=axis).copy()  # 同步翻转标签
    return image, label


def random_rotate(image, label):
    """随机旋转图像和标签（-20到20度之间）"""
    angle = np.random.randint(-20, 20)  # 随机选择旋转角度
    # 使用三次样条插值旋转图像（保持图像质量）
    image = rotate(image, angle, reshape=False, order=3)
    # 使用最近邻插值旋转标签（保持标签离散值）
    label = rotate(label, angle, reshape=False, order=0)
    return image, label

class RandomGenerator(object):
    """随机应用数据增强并调整图像大小"""
    def __init__(self, output_size):
        self.output_size = output_size  # 目标输出尺寸

    def __call__(self, sample):
        image, label = sample['image'], sample['label']

        # 以50%概率应用旋转翻转或随机旋转
        if random.random() > 0.5:
            image, label = random_rot_flip(image, label)
        elif random.random() > 0.5:
            image, label = random_rotate(image, label)

        # 调整图像和标签大小到目标尺寸
        x, y = image.shape
        if x != self.output_size[0] or y != self.output_size[1]:
            # 使用三次样条插值调整图像大小
            image = zoom(image, (self.output_size[0] / x, self.output_size[1] / y), order=3)
            # 使用最近邻插值调整标签大小（保持离散值）
            label = zoom(label, (self.output_size[0] / x, self.output_size[1] / y), order=0)

        # 转换为PyTorch张量并调整维度
        image = torch.from_numpy(image.astype(np.float32)).unsqueeze(0)  # 添加通道维度
        label = torch.from_numpy(label.astype(np.uint8))
        sample = {'image': image, 'label': label.long()}
        return sample


class ACDC_SliceDataset(Dataset):
    """用于ACDC数据集的医学图像分割数据集类"""

    def __init__(self, slice_dir, list_file, transform=None):
        self.slice_dir = slice_dir  # 切片数据目录
        self.transform = transform  # 数据预处理转换

        # 读取样本列表文件
        with open(list_file, 'r') as f:
            self.sample_list = [line.strip() for line in f.readlines() if line.strip() != '']

    def __len__(self):
        return len(self.sample_list)  # 返回数据集大小

    def __getitem__(self, idx):
        sample_name = self.sample_list[idx]
        path = os.path.join(self.slice_dir, sample_name)

        # 从HDF5文件读取图像和标签
        with h5py.File(path, 'r') as f:
            image = f['image'][:]
            label = f['label'][:]

        # 构建样本字典
        sample = {
            'image': image,
            'label': label,
            'case_name': os.path.splitext(sample_name)[0]  # 保留病例名称
        }

        # 应用数据预处理转换
        if self.transform:
            sample = self.transform(sample)
            # 确保转换后仍保留病例名称
            sample['case_name'] = os.path.splitext(sample_name)[0]

        return sample