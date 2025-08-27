# --------------------------------------------------------#
#  该文件用于将单通道灰度图转换成三通道RGB，为每个像素分配不同的颜色
# --------------------------------------------------------#

import os
import cv2
import numpy as np


def gray_to_color_mapping(gray_value):
    mapping = {
        1: (64, 0, 127),  # purple
        2: (64, 64, 0),  # Green
        3: (0, 127, 192),  # Blue
        4: (0, 0, 192),  # Yellow
        5: (127, 127, 0),  # Cyan
        6: (64, 64, 127),  # Magenta
        7: (112, 74, 74),  # Orange
        8: (192, 64, 0)  # Purple
    }
    return mapping.get(gray_value, (0, 0, 0))  # Default to black if not in mapping


def convert_gray_to_color_image(gray_image):
    # Create an empty color image
    color_image = np.zeros((gray_image.shape[0], gray_image.shape[1], 3), dtype=np.uint8)

    # Map each pixel to its corresponding color
    for i in range(gray_image.shape[0]):
        for j in range(gray_image.shape[1]):
            color_image[i, j] = gray_to_color_mapping(gray_image[i, j])

    return color_image


def process_images_in_folder(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            gray_image_path = os.path.join(input_folder, filename)
            color_image_path = os.path.join(output_folder, filename)

            # Read the gray image
            gray_image = cv2.imread(gray_image_path, cv2.IMREAD_GRAYSCALE)

            if gray_image is not None:
                # Convert to color image
                color_image = convert_gray_to_color_image(gray_image)

                # Save the color image
                cv2.imwrite(color_image_path, color_image)


# Example usage
input_folder = ''  # 输入文件夹
output_folder = '' # 输出文件夹
process_images_in_folder(input_folder, output_folder)
