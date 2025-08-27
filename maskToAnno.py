# --------------------------------------------------------#
#   该文件用于将mask图片类型的标签转成coco格式的json文件（单一类别）
# --------------------------------------------------------#

import json
import numpy as np
from pycocotools import mask
import cv2
import os
import sys

if sys.version_info[0] >= 3:
    unicode = str
# __author__ = 'hcaesar'

import io

# 实例的id，每个图像有多个物体每个物体的唯一id
global segmentation_id
segmentation_id = 0


# annotations部分的实现
def maskToAnno(ground_truth_binary_mask, ann_count, category_id):
    contours, _ = cv2.findContours(ground_truth_binary_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # 根据二值图找轮廓
    # contours, _ = cv2.findContours(ground_truth_binary_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)
    cv_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= 0:  # 轮廓过滤
            cv_contours.append(contour)

    annotations = []  # 一幅图片所有的annotatons
    global segmentation_id
    # print(ann_count)
    # 对每个实例进行处理
    for i in range(len(cv_contours)):
        # print(i)
        # 生成二值的黑色图片
        x = np.zeros((512, 512))  # 当轮廓过多，x太小时会报错
        cv2.drawContours(x, cv_contours, i, (1, 1, 1), -1)  # 将单个mask表示为二值图的形式
        ground_truth_binary_mask_id = np.array(x).astype(np.uint8)
        fortran_ground_truth_binary_mask = np.asfortranarray(ground_truth_binary_mask_id)
        # 求每个mask的面积和框
        encoded_ground_truth = mask.encode(fortran_ground_truth_binary_mask)
        ground_truth_area = mask.area(encoded_ground_truth)
        ground_truth_bounding_box = mask.toBbox(encoded_ground_truth)
        contour, _ = cv2.findContours(ground_truth_binary_mask_id, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # contours, _ = cv2.findContours(ground_truth_binary_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)
        # contour = measure.find_contours(ground_truth_binary_mask_id, 0.5)
        # print(contour)
        annotation = {
            "id": segmentation_id,
            "image_id": ann_count,
            "segmentation": [],
            "area": ground_truth_area.tolist(),
            "bbox": ground_truth_bounding_box.tolist(),
            "category_id": category_id,
            "iscrowd": 0
        }
        #  print(contour)
        # 求segmentation部分

        contour = np.flip(contour, axis=1)

        segmentation = contour.ravel().tolist()
        if len(segmentation) <= 4:
            continue
        annotation["segmentation"].append(segmentation)
        annotations.append(annotation)
        segmentation_id = segmentation_id + 1
    return annotations


# mask图像路径
# block_mask_path = r"C:\Users\ChenXuHui\Desktop\train\train\Mask_8366"
block_mask_path = r"C:\Users\ChenXuHui\Desktop\val\val\Mask_8000/"
block_mask_image_files = os.listdir(block_mask_path)
# coco json保存的位置
jsonPath = "val_coco.json"
annCount = 0
imageCount = 0
# 原图像的路径， 原图像和mask图像的名称是一致的。
path = r"C:\Users\ChenXuHui\Desktop\val\val\Mask_8000/"
rgb_image_files = os.listdir(path)
with io.open(jsonPath, 'w', encoding='utf8') as output:
    # 那就全部写在一个文件夹好了
    # 先写images的信息
    output.write(unicode('{\n'))
    output.write(unicode('"images": [\n'))
    for image in rgb_image_files:
        img_path = os.path.join(path, image)
        img = cv2.imread(img_path)
        h, w = img.shape[:-1]
        output.write(unicode('{'))
        annotation = {
            "id": imageCount,
            "file_name": image,
            "width": w,
            "height": h
        }
        str_ = json.dumps(annotation, indent=4)
        str_ = str_[1:-1]
        if len(str_) > 0:
            output.write(unicode(str_))
            imageCount = imageCount + 1
        if image == rgb_image_files[-1]:
            output.write(unicode('}\n'))
        else:
            output.write(unicode('},\n'))
    output.write(unicode('],\n'))
    # 接下来写cate
    output.write(unicode('"categories": [\n'))
    output.write(unicode('{\n'))
    categories = {
        "supercategory": "building",
        "id": 1,
        "name": "building"
    }
    str_ = json.dumps(categories, indent=4)
    str_ = str_[1:-1]
    if len(str_) > 0:
        output.write(unicode(str_))
    output.write(unicode('}\n'))
    output.write(unicode('],\n'))
    # 写annotations
    output.write(unicode('"annotations": [\n'))
    for i in range(len(block_mask_image_files)):

        block_image = block_mask_image_files[i]
        label_path = os.path.join(block_mask_path, block_image)
        #       print(block_image)
        # 读取二值图像
        block_im = cv2.imread(os.path.join(block_mask_path, block_image), 0)
        _, block_im = cv2.threshold(block_im, 100, 1, cv2.THRESH_BINARY)
        block_im = np.array(block_im).astype(np.uint8)
        try:
            block_anno = maskToAnno(block_im, annCount, 1)
        except:
            os.remove(label_path)
            print("Delete File: " + label_path)
        # block_anno = maskToAnno(block_im, annCount, 1)
        for b in block_anno:
            str_block = json.dumps(b, indent=4)
            str_block = str_block[1:-1]
            if len(str_block) > 0:
                output.write(unicode('{\n'))
                output.write(unicode(str_block))
                if block_image == rgb_image_files[-1] and b == block_anno[-1]:
                    output.write(unicode('}\n'))
                else:
                    output.write(unicode('},\n'))
        annCount = annCount + 1
    output.write(unicode(']\n'))
    output.write(unicode('}\n'))
