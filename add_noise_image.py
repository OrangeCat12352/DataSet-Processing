
# --------------------------------------------------------#
#   该文件用于给图片添加噪声
# --------------------------------------------------------#
import os
import numpy as np
from PIL import Image


def add_noise_to_image(image, noise_level=0.2):
    """
    Add random noise to an image.

    :param image: PIL.Image object
    :param noise_level: float, level of noise to add (0 to 1)
    :return: PIL.Image object with noise added
    """
    # Convert image to numpy array
    np_image = np.array(image)

    # Generate random noise
    noise = np.random.randn(*np_image.shape) * 255 * noise_level

    # Add noise to the image
    noisy_image = np_image + noise

    # Clip values to be in the valid range (0 to 255)
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)

    # Convert numpy array back to PIL image
    return Image.fromarray(noisy_image)


def batch_add_noise(input_folder, output_folder, noise_level=0.2):
    """
    Add noise to all images in a folder and save them to another folder.

    :param input_folder: str, path to the input folder containing images
    :param output_folder: str, path to the output folder to save noisy images
    :param noise_level: float, level of noise to add (0 to 1)
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(input_folder, filename)
            image = Image.open(image_path)

            noisy_image = add_noise_to_image(image, noise_level)

            output_path = os.path.join(output_folder, filename)
            noisy_image.save(output_path)
            print(f"Saved noisy image: {output_path}")


if __name__ == '__main__':
    batch_add_noise(r'D:\DevTools\Matlab\workspace\DataProcess\test', r'D:\DevTools\Matlab\workspace\DataProcess\test',
                    noise_level=0.1)
