import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

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

def resize_keep_ratio_images_in_folder(input_folder, target_width, target_height, make_horizontal=True):
    """
    Resizes all images in the folder while keeping the ratio.

    Parameters:
    - input_folder: Folder address
    - target_width: Width of the output image
    - target_height: Height of the output image
    - make_horizontal: If True, makes the vertical images horizontal

    Returns:
    - nothing
    """

    # Traverse through all subdirectories and their files
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            # Construct the full path to each image
            image_path = os.path.join(root, file)

            # Read the image using OpenCV
            image = cv2.imread(image_path)

            # Make the image horizontal if it is not
            if make_horizontal:
                image = make_image_horizontal(image)

            # Detect the original resolution
            original_width, original_height = detect_resolution_of_image(image)

            # Calculate the scale factor for resizing
            scale_factor_width = target_width / original_width
            scale_factor_height = target_height / original_height

            # Choose the smaller scale factor to keep the aspect ratio
            scale_factor = min(scale_factor_width, scale_factor_height)

            # Calculate the new resolution
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)

            # Create a canvas with the desired resolution
            canvas = canvas_creator(target_height, target_width, color='random')

            # Calculate the position to paste the resized image on the canvas
            x_offset, y_offset = calc_offset(target_width, target_height, new_width, new_height)

            # Resize the image
            resized_image = cv2.resize(image, (new_width, new_height))

            # Paste the resized image on the canvas
            canvas[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = resized_image

            # Save the resized image
            cv2.imwrite(image_path, canvas)


main_folder_path = "code\data_analysis\dataset\dataset"
out_folder_path = "code\data_analysis\dataset\dataset"
target_resolution = (640, 640)
# resize_keep_ratio_images_in_folder(read_folder_path = main_folder_path, target_size = target_resolution, write_folder_path = out_folder_path, make_horizental=False, background_color='random')
resize_keep_ratio_images_in_folder(main_folder_path, 640, 640)
