# --------------------------------------------------------#
#   该文件用于将COCO数据集格式的json标签转换成mask的图片形态
# --------------------------------------------------------#

from pycocotools.coco import COCO  # pycocotools.coco 这是用于处理COCO数据集的Python工具库。
import os  # os：用于处理文件路径和文件夹操作。
from PIL import Image  # PIL.Image：用于图像的读取和处理。
import numpy as np  # numpy：用于数值计算。
from matplotlib import pyplot as plt  # matplotlib.pyplot：用于绘制图像。
import cv2  # cv2：OpenCV库，用于图像处理和保存。


def mask_generator(coco, width, height, anns_list):
    mask_pic = np.zeros((height, width))
    # 生成mask
    for single in anns_list:
        mask_single = coco.annToMask(single)
        mask_pic += mask_single
    # 转化为255
    for row in range(height):
        for col in range(width):
            if (mask_pic[row][col] > 0):
                mask_pic[row][col] = 255
    mask_pic = mask_pic.astype(int)
    imgs = np.zeros(shape=(height, width, 3), dtype=np.float32)
    imgs[:, :, 0] = mask_pic[:, :]
    imgs[:, :, 1] = mask_pic[:, :]
    imgs[:, :, 2] = mask_pic[:, :]
    imgs = imgs.astype(int)
    return imgs
    '''
    #转为三通道
    imgs = np.zeros(shape=(height, width, 3), dtype=np.float32)
    imgs[:, :, 0] = mask_pic[:, :]
    imgs[:, :, 1] = mask_pic[:, :]
    imgs[:, :, 2] = mask_pic[:, :]
    imgs = imgs.astype(int)
    '''
    # return mask_pic


def convert_coco2mask():
    catIds = coco.getCatIds()  # 从 coco 对象中获取所有物体类别的 catIds（类别标识）。
    imgIds = coco.getImgIds(catIds=1)  # 使用 coco 对象获取所有具有类别标识为 0 的图片的 imgIds（图片标识）。
    print("Total images:", len(imgIds))

    for image_id in imgIds:  # 对于每张图像，以下步骤将被执行：
        img = coco.imgs[image_id]  # 从 coco 对象中获取图像信息（包括文件名和ID）。
        # image = np.array(Image.open(os.path.join(img_dir, img['file_name'])))
        # 使用 PIL 打开图像文件，并将其转换为 numpy 数组。
        cat_ids = coco.getCatIds()
        anns_ids = coco.getAnnIds(imgIds=img['id'], catIds=cat_ids, iscrowd=None)
        # 获取图像中所有与类别标识相关联的注释标识（anns_ids）。
        anns = coco.loadAnns(anns_ids)
        # coco.showAnns(anns)  # 从 coco 中加载这些注释，并使用 coco.showAnns() 显示注释（可视化）。
        # mask = coco.annToMask(anns[0]) * 255
        # 255用来调节灰度，255全白
        # 将注释转换为二值掩码图像，其中 coco.annToMask() 将一个注释转换为与图像大小相同的掩码。
        mask_image = mask_generator(coco, img['width'], img['height'], anns)
        # 创建一个初始掩码 mask，并逐个将所有注释的掩码相加到这个初始掩码中。
        cv2.imwrite(os.path.join(save_dir, "{}".format(img['file_name'])), mask_image)
        # 使用 cv2.imwrite() 将最终的掩码保存为图像文件。


if __name__ == '__main__':
    Dataset_dir = ''      # 定义了 Dataset_dir 作为COCO数据集的根目录
    coco = COCO(os.path.join(Dataset_dir, 'instances_val2017.json'))

    # 创建 coco 对象，加载包含标注信息的 JSON 文件。
    img_dir = os.path.join(Dataset_dir, 'images')  # img_dir 作为图像文件夹路径,默认在该路径下的images文件夹中，所以要把图片放到该images文件夹
    save_dir = os.path.join(Dataset_dir, 'Mask')  # save_dir 作为保存掩码图像的文件夹路径。

    if not os.path.isdir(save_dir):  # 如果 save_dir 文件夹不存在，则创建它。
        os.makedirs(save_dir)  # 调用 convert_coco2mask() 函数进行实际的转换操作。
    convert_coco2mask()
