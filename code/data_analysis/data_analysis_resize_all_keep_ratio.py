import cv2
import numpy as np
import os
import matplotlib.pyplot as plt


def create_directory_if_not_exist(out_root):
    """
    Creates directory if it does not exist already

    Parameters:
    - out_root: Directory address

    Returns:
    - nothing
    """
    # Check if the directory exists
    if not os.path.exists(out_root):
        # If the directory does not exist, create it
        os.makedirs(out_root)

def detect_resolution_of_image(image):
    """
    Detect the resolution of an image.

    Parameters:
    - image: image data.

    Returns:
    - Tuple representing the resolution (width, height).
    """
    resolution = (image.shape[1], image.shape[0])
    return resolution

def make_image_horizontal(image):
    """
    Rotates image if it is vertical.

    Parameters:
    - image: image data.

    Returns:
    - horizontal image
    """
    width, height = detect_resolution_of_image(image)
    # if width is less that height, rotate it. Else, return the original image.
    if width < height:
        return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        return image

def calc_offset(desired_width, desired_height, original_width, original_height):
    """
    Calculates the offset (to but image in middle of square)

    Parameters:
    - desired and original width and height

    Returns:
    - Tuple offset x and offset y. One of them is zero.
    """
    # Calculate the position to paste the resized image on the canvas
    x_offset = (desired_width - original_width) // 2
    y_offset = (desired_height - original_height) // 2
    return x_offset, y_offset

def canvas_creator(height, width, color='black'):
    """
    Creates canvas with given size and color sring

    Parameters:
    - width of canvas to be created
    - height of canvas o be created
    - color of canvas

    Returns:
    - np.array for canvas
    """
    if color == "random":
        background_color = np.random.randint(0, 256, size=3, dtype=np.uint8)
        # Create a 3D array for the image with the random background color
        return np.full((height, width, 3), background_color, dtype=np.uint8)
    
    return np.zeros((height, width, 3), dtype=np.uint8)

def resize_keep_ratio_images_in_folder(read_folder_path, target_size, write_folder_path, make_horizental=True, background_color='black'):
    """
    Process images within a folder and its subfolders. It resizes all images to the given size and write to the other folder.
    Parameters:
    - read_folder_path: Path to the main folder to read images.
    - target_size: resolution to change.
    - write_folder_path: path to the main folder to write images.
    - make_horizental: if true, rotates vertical images to make them horizental.
    - background_color: choose the background color. Black or random.
    Returns:
    - nothing
    """
    for root, dirs, files in os.walk(read_folder_path):
        class_folder = root.split('/')[1]
        out_root = f'{write_folder_path}{class_folder}'
        create_directory_if_not_exist(out_root)
        for index, file in enumerate(files, start=1):
            image_path = os.path.join(root, file)
            write_path = os.path.join(out_root, file)
            original_image = cv2.imread(image_path)
            if make_horizental == True:
                original_image = make_image_horizontal(original_image)
           
            width, height = detect_resolution_of_image(original_image)

            desired_width, desired_height = target_size[0], target_size[1]
            ratio = min(desired_width / width, desired_height / height)

            # Resize the image with the calculated ratio
            resized_image = cv2.resize(original_image, (int(width * ratio), int(height * ratio)))

            # Create a black background canvas
            canvas = canvas_creator(desired_height, desired_width, background_color)

            x_offset, y_offset = calc_offset(desired_width, desired_height, resized_image.shape[1], resized_image.shape[0])

            # Paste the resized image onto the canvas
            canvas[y_offset:y_offset+resized_image.shape[0], x_offset:x_offset+resized_image.shape[1]] = resized_image

            # Save the rescaled image with the new filename (in the new folder)
            cv2.imwrite(write_path, canvas)

main_folder_path = "dataset_rooftile_small/"
out_folder_path = "dataset_rooftile_keep_ratio_640_random_back/"
target_resolution = (640, 640)
resize_keep_ratio_images_in_folder(read_folder_path = main_folder_path, target_size = target_resolution, write_folder_path = out_folder_path, make_horizental=False, background_color='random')

