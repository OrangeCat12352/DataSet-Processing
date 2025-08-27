import os
import xml.etree.ElementTree as ET

def convert_voc_to_yolo(xml_dir, output_dir, class_name='airplane'):
    os.makedirs(output_dir, exist_ok=True)
    class_id = 0  # airplane 的类别 ID

    for filename in os.listdir(xml_dir):
        if not filename.endswith('.xml'):
            continue

        xml_path = os.path.join(xml_dir, filename)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 获取图像宽高
        size = root.find('size')
        if size is None:
            print(f"⚠️ 跳过（无尺寸信息）: {filename}")
            continue
        img_width = int(size.find('width').text)
        img_height = int(size.find('height').text)

        yolo_lines = []
        for obj in root.findall('object'):
            bndbox = obj.find('bndbox')
            if bndbox is None:
                continue
            xmin = float(bndbox.find('xmin').text)
            ymin = float(bndbox.find('ymin').text)
            xmax = float(bndbox.find('xmax').text)
            ymax = float(bndbox.find('ymax').text)

            # 转换为 YOLO 格式并归一化
            x_center = ((xmin + xmax) / 2.0) / img_width
            y_center = ((ymin + ymax) / 2.0) / img_height
            width = (xmax - xmin) / img_width
            height = (ymax - ymin) / img_height

            # YOLO格式：class_id x_center y_center width height
            yolo_line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
            yolo_lines.append(yolo_line)

        # 写入 .txt 文件
        out_filename = os.path.splitext(filename)[0] + ".txt"
        out_path = os.path.join(output_dir, out_filename)
        with open(out_path, "w") as f:
            f.write("\n".join(yolo_lines))
        
        print(f"✅ 转换完成: {out_filename}")

# 示例调用
convert_voc_to_yolo(
    xml_dir="./xml",         # 原始 VOC XML 路径
    output_dir="./yolo_txt"  # 输出 YOLO TXT 路径
)
