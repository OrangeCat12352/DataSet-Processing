# generate_yolo_labels.py

import os
import cv2

def mask_to_yolo(mask_path, label_path, min_area=100):
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        print(f"❌ 无法读取掩码: {mask_path}")
        return
    h, w = mask.shape
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    label_lines = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area:
            continue
        x, y, bw, bh = cv2.boundingRect(cnt)
        cx = (x + bw / 2) / w
        cy = (y + bh / 2) / h
        nw = bw / w
        nh = bh / h
        label_lines.append(f"0 {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}")

    os.makedirs(os.path.dirname(label_path), exist_ok=True)
    with open(label_path, "w") as f:
        f.write("\n".join(label_lines))


def generate_yolo_labels_from_masks(mask_dir, label_dir, min_area=100):
    for name in os.listdir(mask_dir):
        if not name.lower().endswith(('.png', '.jpg', '.bmp')):
            continue
        stem = os.path.splitext(name)[0]
        mask_path = os.path.join(mask_dir, name)
        label_path = os.path.join(label_dir, stem + ".txt")
        mask_to_yolo(mask_path, label_path, min_area)


if __name__ == "__main__":
    mask_dir = "./2/"
    label_dir = "./3/"
    os.makedirs(label_dir, exist_ok=True)
    generate_yolo_labels_from_masks(mask_dir, label_dir, min_area=100)
