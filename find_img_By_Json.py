
# --------------------------------------------------------#
#   该文件根据标签json文件找到对应图片
# --------------------------------------------------------#

# --------------------------------------------------------#
#   该文件通过json文件查找对应的图片
# --------------------------------------------------------#
import json
import os
import shutil

# 读取COCO数据集的json标签文件
with open(r'C:\Users\ChenXuHui\Desktop\cocoBuilding8366\annotations\instances_val2017.json', 'r') as f:
    data = json.load(f)

# 找到annotations部分，该部分包含了图片中检测目标的分类信息和位置信息
annotations = data['images']

# 找到annotations部分中image_id对应到images部分的id，使检测目标与图片关联起来
file_name = [ann['file_name'] for ann in annotations]

# 源文件夹路径
src_folder = r'C:\Users\ChenXuHui\Desktop\val\val\images'

# 目标文件夹路径
dst_folder = r'C:\Users\ChenXuHui\Desktop\cocoBuilding8366\val2017'


# 遍历源文件夹中的所有文件
for filename in os.listdir(src_folder):
    for image_name in file_name:
        # 如果文件名与已知图片名字相同，将其复制到目标文件夹中
        if filename == image_name:
            shutil.copy(os.path.join(src_folder, filename), dst_folder)
