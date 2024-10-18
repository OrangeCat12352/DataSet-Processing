# --------------------------------------------------------#
#   该文件用于给图片添加雾气
# --------------------------------------------------------#
import os
from PIL import Image, ImageEnhance, ImageFilter


def add_fog_to_image(image, fog_density=0.5):
    """
    Add a fog effect to an image.

    :param image: PIL.Image object
    :param fog_density: float, level of fog to add (0 to 1)
    :return: PIL.Image object with fog effect
    """
    # Create a white image with the same size as the input image
    fog = Image.new('RGBA', image.size, (255, 255, 255, int(255 * fog_density)))

    # Composite the original image with the fog
    foggy_image = Image.alpha_composite(image.convert('RGBA'), fog)

    # Enhance the image to simulate a foggy effect
    enhancer = ImageEnhance.Brightness(foggy_image)
    foggy_image = enhancer.enhance(0.7)  # Adjust brightness to simulate fog

    return foggy_image.convert('RGB')


def batch_add_fog(input_folder, output_folder, fog_density=0.5):
    """
    Add fog effect to all images in a folder and save them to another folder.

    :param input_folder: str, path to the input folder containing images
    :param output_folder: str, path to the output folder to save foggy images
    :param fog_density: float, level of fog to add (0 to 1)
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            image_path = os.path.join(input_folder, filename)
            image = Image.open(image_path)

            foggy_image = add_fog_to_image(image, fog_density)

            output_path = os.path.join(output_folder, filename)
            foggy_image.save(output_path)
            print(f"Saved foggy image: {output_path}")





if __name__ == '__main__':
    batch_add_fog(r'D:\DevTools\Matlab\workspace\DataProcess\test', r'D:\DevTools\Matlab\workspace\DataProcess\test',fog_density=0.4)

