# --------------------------------------------------------#
#   该文件用于调整输入图片的后缀为png(jpeg)
# --------------------------------------------------------#
from PIL import Image
import os

import os
from PIL import Image


def convert_images(input_folder, output_folder, target_format='png'):
    """
    将输入文件夹中的所有图片文件转换为指定的格式，并保存到输出文件夹。

    :param input_folder: 输入文件夹路径
    :param output_folder: 输出文件夹路径
    :param target_format: 目标图片格式，默认为 'png'
    """

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 支持的图片格式
    valid_extensions = (".png", ".jpeg", ".jpg", ".bmp", ".gif", ".tif")

    # 判断目标格式是否是 'jpg'，如果是，需要使用 'JPEG' 格式
    target_format = 'jpeg' if target_format.lower() == 'jpg' else target_format.lower()

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(valid_extensions):  # 检查是否为支持的图片格式
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + f".{target_format.lower()}"
            output_path = os.path.join(output_folder, output_filename)

            # 跳过已是目标格式的文件
            if filename.lower().endswith(f".{target_format.lower()}"):
                print(f"Skipping {filename}, already in {target_format} format.")
                continue

            try:
                # 打开图像并转换为目标格式
                with Image.open(input_path) as img:
                    img = img.convert('RGB')  # 确保图像转换为RGB模式，避免错误
                    img.save(output_path, target_format.upper())  # 保存为目标格式
                    print(f"Converted {filename} to {output_filename}")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")


# 使用示例
input_folder = "./1"  # 输入文件夹路径
output_folder = "./convert"  # 输出文件夹路径
target_format = 'png'  # 目标格式，可选择 'png', 'jpg', 等

convert_images(input_folder, output_folder, target_format)
