import os
import shutil

def copy_related_files_by_sar_names(sar_dir, src_dir, dst_dir, suffixes=None):
    """
    根据 SAR 图像名，从 src_dir 中复制相关文件（如 .xml、.txt）到 dst_dir。

    参数:
        sar_dir: 包含 SAR 图像的目录（用于获取文件名）
        src_dir: 存放各种标注文件的目录
        dst_dir: 目标复制目录
        suffixes: 要复制的文件后缀
    """
    os.makedirs(dst_dir, exist_ok=True)

    if suffixes is None:
        suffixes = ['.xml', '.txt', '.json']

    # 获取 SAR 图像的基本文件名（不含扩展名）
    sar_names = [os.path.splitext(f)[0] for f in os.listdir(sar_dir)
                 if os.path.splitext(f)[1].lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff']]

    for name in sar_names:
        for suffix in suffixes:
            filename = name + suffix
            src_path = os.path.join(src_dir, filename)
            dst_path = os.path.join(dst_dir, filename)
            if os.path.exists(src_path):
                shutil.copy2(src_path, dst_path)
                print(f"✅ 已复制: {filename}")
            else:
                print(f"⚠️ 缺失: {filename}")

# 示例调用
copy_related_files_by_sar_names(
    sar_dir='./sar_resize',            # 提取SAR图像文件名
    
    src_dir='./1',      # 原始标签文件的位置
    dst_dir='./sar_resize',         # 要复制标注文件到的位置
    suffixes=['.jpg', '.txt']   # 需要的扩展名

    #src_dir='./image',     # 原始光学图片的位置
    #dst_dir='./OPT',          # 要复制光学图片到的位置
    #suffixes=['.jpg', '.png']
)
