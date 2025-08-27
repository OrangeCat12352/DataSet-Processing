# --------------------------------------------------------#
#   该文件用于将图片变成棋盘格
# --------------------------------------------------------#
from PIL import Image, ImageDraw
def split_and_merge_image(input_path, output_path, n):
    # 打开图片
    original_image = Image.open(input_path)

    # 获取图片的宽度和高度
    width, height = original_image.size

    # 计算每个小块的宽度和高度
    block_width = width // n
    block_height = height // n

    # 创建一个新的图片对象，白色背景
    new_image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(new_image)

    # 分割和拼接图片
    for i in range(n):
        for j in range(n):
            # 计算当前小块的坐标
            x1 = j * block_width
            y1 = i * block_height
            x2 = x1 + block_width
            y2 = y1 + block_height

            # 裁剪小块
            block = original_image.crop((x1, y1, x2, y2))

            # 在新图片上粘贴小块
            new_image.paste(block, (x1, y1))

            # 在拼接处画白色线条
            draw.line([(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)], fill="white", width=20)

    # 保存结果图片
    new_image.save(output_path)


if __name__ == '__main__':
    path1 = 'area1_train_10.png'  # 输入图片路径
    path2 = 'area1_crop_10.png'  # 输出图片路径
    n = 3 #将图片分成多少份
    # 调用函数，传入输入图片路径和输出图片路径
    split_and_merge_image(path1, path2, n)
