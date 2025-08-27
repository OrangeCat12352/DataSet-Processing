import os
from PIL import Image

def batch_process_images(input_folder, output_folder, target_ext, convert=False):
    """
    批量处理图片：只改后缀或转换格式
    :param input_folder: 输入图片文件夹路径
    :param output_folder: 输出图片文件夹路径
    :param target_ext: 目标后缀名（如 'jpg' 或 'png'）
    :param convert: 是否需要真正转换图片格式（True/False）
    """
    target_ext = target_ext.lower().lstrip('.')  # 格式化
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        old_path = os.path.join(input_folder, filename)
        if os.path.isfile(old_path):
            name, ext = os.path.splitext(filename)
            if ext.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']:
                new_filename = f"{name}.{target_ext}"
                new_path = os.path.join(output_folder, new_filename)

                if convert:
                    # 读取并转换格式
                    try:
                        with Image.open(old_path) as img:
                            # 对于jpg需要转换为RGB
                            if target_ext in ['jpg', 'jpeg'] and img.mode != 'RGB':
                                img = img.convert('RGB')
                            img.save(new_path)
                            print(f"已转换并保存: {new_filename}")
                    except Exception as e:
                        print(f"转换失败: {filename}, 错误: {e}")
                else:
                    # 只修改后缀名并复制
                    try:
                        with open(old_path, 'rb') as src, open(new_path, 'wb') as dst:
                            dst.write(src.read())
                        print(f"已复制并改后缀: {new_filename}")
                    except Exception as e:
                        print(f"复制失败: {filename}, 错误: {e}")

# ===== 使用示例 =====
input_dir = r"D:\images"        # 输入文件夹
output_dir = r"D:\output_images" # 输出文件夹
target_extension = "png"        # 目标后缀 'jpg' 或 'png'
need_convert = True             # True=转换格式，False=只改后缀

batch_process_images(input_dir, output_dir, target_extension, need_convert)
