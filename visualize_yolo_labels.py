# visualize_yolo_labels.py

import os
import cv2

def find_matching_image(image_dir, stem):
    for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tif']:
        path = os.path.join(image_dir, stem + ext)
        if os.path.exists(path):
            return path
    return None

def visualize_yolo_label(image_path, label_path, output_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ 图像读取失败: {image_path}")
        return

    h, w = image.shape[:2]
    if not os.path.exists(label_path):
        print(f"⚠️ 标签不存在: {label_path}")
        return

    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            cls, cx, cy, bw, bh = map(float, parts)
            x1 = int((cx - bw / 2) * w)
            y1 = int((cy - bh / 2) * h)
            x2 = int((cx + bw / 2) * w)
            y2 = int((cy + bh / 2) * h)
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, "aircraft", (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, image)


def visualize_yolo_labels(image_dir, label_dir, vis_dir):
    for name in os.listdir(label_dir):
        if not name.lower().endswith('.txt'):
            continue
        stem = os.path.splitext(name)[0]
        label_path = os.path.join(label_dir, name)
        image_path = find_matching_image(image_dir, stem)
        if image_path is None:
            print(f"⚠️ 未找到图像: {stem}")
            continue
        ext = os.path.splitext(image_path)[1]
        vis_path = os.path.join(vis_dir, stem + ext)
        visualize_yolo_label(image_path, label_path, vis_path)


if __name__ == "__main__":
    image_dir = "./OPT/"
    label_dir = "./label/"
    vis_dir = "./vis/"
    os.makedirs(vis_dir, exist_ok=True)
    visualize_yolo_labels(image_dir, label_dir, vis_dir)
