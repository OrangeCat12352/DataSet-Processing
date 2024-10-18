# --------------------------------------------------------#
#   该文件用于调整输入图片的后缀为jpeg
# --------------------------------------------------------#
import os

from PIL import Image
from tqdm import tqdm

# --------------------------------------------------------#
#   Origin_JPEGImages_path   原始图片所在的路径
#   Out_JPEGImages_path      输出图片所在的路径
# --------------------------------------------------------#
Origin_JPEGImages_path = "./1"
Out_JPEGImages_path = "./convert"

if __name__ == "__main__":
    if not os.path.exists(Out_JPEGImages_path):
        os.makedirs(Out_JPEGImages_path)

    # ---------------------------#
    #   遍历标签并赋值
    # ---------------------------#
    image_names = os.listdir(Origin_JPEGImages_path)
    print("正在遍历全部图片。")
    for image_name in tqdm(image_names):
        image = Image.open(os.path.join(Origin_JPEGImages_path, image_name))
        image = image.convert('RGB')
        image.save(os.path.join(Out_JPEGImages_path, os.path.splitext(image_name)[0] + '.jpeg'))
