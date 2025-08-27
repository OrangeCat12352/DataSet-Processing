batch_process_images.py            
批量处理图片名（只改后缀或转换格式）

coco2mask.py                       
用于将COCO数据集格式的json标签转换成mask掩码

Convert_SegmentationClass.py       
用于调整mask标签的格式，[0,255]->[0,1]

copy_by_sar.py                    
根据 SAR文件夹中 图像名，从 src_dir 中复制相关文件（如 .xml、.txt）到 dst_dir。

Eval_Origin.py                     
用于生成每张图片的SOD指标，便于Origin使用

find_img_By_Json.py                
根据标签json文件找到对应图片

generate_yolo_labels_by_json.py    
json格式的目标检测标签转换成yolo格式

generate_yolo_labels_by_mask.py    
mask掩码标签转换成yolo格式的目标检测框

generate_yolo_labels_by_xml.py     
xml格式的目标检测标签转换成yolo格式

gray_To_rgb.py                     
该文件用于将单通道灰度图转换成三通道RGB，为每个像素分配不同的颜色

image_crop.py                      
用于对原始遥感图像训练数据进行裁切，生成固定大小的patches,适用于HBB(Horizontal Bounding Box)

img_resize.py                      
用于调整图片大小

img_resize_by_sar.py               
根据OPT文件夹下的图片大小，resize SAR文件夹下同名文件的大小

imge_checkerboard.py               
用于将图片变成棋盘格形状

maskToAnno.py                      
该文件用于将mask图片类型的标签转成coco格式的json文件（单一类别）

model_efficiency_analysis.py       
用于模型的计算效率分析

rgb_To_gray.py                     
用于RGB转成灰度图

val_seg.py                         
该文件用于可视化json格式的标签（转成图片）

visualize_yolo_labels.py           
yolo标签可视化 

voc_annotation.py                  
该文件用于分割训练集和验证集（VOC格式）

Weight_Process.py                  
该文件用于处理权重文件，包括更改Key，删除key

