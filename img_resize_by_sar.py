import os
from PIL import Image

# 文件夹路径
sar_dir = 'SAR'
opt_dir = 'OPT'
output_dir = 'sar_resize'

# 创建输出文件夹
os.makedirs(output_dir, exist_ok=True)

# 获取SAR目录下的所有文件
for sar_filename in os.listdir(sar_dir):
    sar_path = os.path.join(sar_dir, sar_filename)

    # 提取文件名（不含扩展名），用于匹配opt目录
    name, _ = os.path.splitext(sar_filename)

    # 在opt目录中查找同名图片（支持常见扩展名）
    opt_path = None
    for ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tif']:
        candidate = os.path.join(opt_dir, name + ext)
        if os.path.exists(candidate):
            opt_path = candidate
            break

    if opt_path is None:
        print(f"[跳过] 未找到匹配的opt图像：{name}")
        continue

    try:
        # 加载图像
        sar_img = Image.open(sar_path)
        opt_img = Image.open(opt_path)

        # 获取opt图像的大小
        target_size = opt_img.size  # (width, height)

        # Resize SAR图像并保存
        resized_sar = sar_img.resize(target_size, Image.BILINEAR)
        resized_sar.save(os.path.join(output_dir, sar_filename))
        print(f"[成功] 调整：{sar_filename} -> 尺寸 {target_size}")

    except Exception as e:
        print(f"[错误] 处理 {sar_filename} 时发生错误：{e}")
