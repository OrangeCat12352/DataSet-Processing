import os
import json

def convert_coco_to_yolo(coco_json_path, output_dir, image_dir, plane_name='plane'):
    """
    将 COCO 格式的标签转换为 YOLO 格式。
    
    参数:
        coco_json_path: COCO 格式的标签路径
        output_dir: YOLO 标签输出目录
        image_dir: 包含图像的目录，用于获取图像宽高
        plane_name: 类别名称，默认为 "plane"
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(coco_json_path, 'r') as f:
        coco = json.load(f)

    # 找出 plane 类别 ID
    category_name_to_id = {cat['name']: cat['id'] for cat in coco['categories']}
    plane_id = category_name_to_id.get(plane_name)
    if plane_id is None:
        raise ValueError(f"类别 '{plane_name}' 不在 COCO 的 categories 中")

    # 图像 ID -> 文件名、宽高
    image_info = {img['id']: img for img in coco['images']}

    # 处理标注
    annotations_per_image = {}
    for ann in coco['annotations']:
        if ann['category_id'] != plane_id:
            continue  # 只保留 plane 类别

        img_id = ann['image_id']
        bbox = ann['bbox']  # COCO: [x_min, y_min, width, height]

        image = image_info[img_id]
        img_w, img_h = image['width'], image['height']
        file_name = os.path.splitext(image['file_name'])[0]

        # 转换为 YOLO 格式
        x, y, w, h = bbox
        cx = (x + w / 2) / img_w
        cy = (y + h / 2) / img_h
        nw = w / img_w
        nh = h / img_h

        line = f"0 {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}"

        annotations_per_image.setdefault(file_name, []).append(line)

    # 写入 .txt 文件
    for file_name, lines in annotations_per_image.items():
        label_path = os.path.join(output_dir, f"{file_name}.txt")
        with open(label_path, 'w') as f:
            f.write("\n".join(lines))
        print(f"✅ 已写入: {label_path}")

    print("🚀 COCO → YOLO 格式转换完成")

# 示例用法
convert_coco_to_yolo(
    coco_json_path='./instances_plane.json',
    output_dir='./yolo_labels',
    image_dir='./OPT',  # 只用于获取图像宽高信息
    plane_name='plane'     # 确保和 COCO 中定义一致
)
