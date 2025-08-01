from PIL import Image
import os

def save_individual_images(image_dir, image_list, resize_to=(256, 256)):
    saved_paths = []
    for img_name in image_list:
        path = os.path.join(image_dir, img_name)
        if os.path.exists(path):
            img = Image.open(path).resize(resize_to)
            resized_name = f"resized_{img_name}"
            output_path = os.path.join(image_dir, resized_name)
            img.save(output_path)
            saved_paths.append(output_path)
    return saved_paths
