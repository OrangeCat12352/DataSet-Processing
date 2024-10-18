
# --------------------------------------------------------#
#   该文件用于调整图片大小
# --------------------------------------------------------#

import os
from PIL import Image


def resize1(input_folder, output_folder, scale_factor):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):  # 添加你需要处理的图像格式
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # 打开图像
            original_image = Image.open(input_path)

            # 计算新的大小
            width, height = original_image.size
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)

            # 调整大小
            resized_image = original_image.resize((new_width, new_height))

            # 保存调整大小后的图像
            resized_image.save(output_path)


def resize2(input_folder, output_folder, max_size):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            original_image = Image.open(input_path)
            original_image.thumbnail((max_size, max_size))
            original_image = original_image.convert('RGB')
            original_image.save(output_path)


def resize_images(input_folder, output_folder, target_size):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # 打开图像文件
        with Image.open(input_path) as img:
            # 调整图像尺寸
            resized_img = img.resize(target_size)

            # 保存调整后的图像到输出文件夹
            resized_img.save(output_path)


# 例子
input_folder_path = r"C:\Users\Chen Xuhui\Desktop\SAR数据集\SAR图片\ship\SAR-Ship-Dataset"  # 替换成你的输入文件夹路径
output_folder_path = r"C:\Users\Chen Xuhui\Desktop\SAR图片\ship\SAR-Ship-Dataset"  # 替换成你的输出文件夹路径

# factor = 0.5  # 替换成你希望的调整大小的比例
# factor = 512/3072  # 替换成你希望的调整大小的比例
# resize1(input_folder_path, output_folder_path, factor)

# max_size = 1176  # 设置目标大小，保持宽高比,可以根据需要调整
# resize2(input_folder_path, output_folder_path, max_size)

target_size = (1024, 1024)  # 替换为你想要的尺寸
resize_images(input_folder_path, output_folder_path, target_size)

print("resize 完成！")
