import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def detect_resolution(image_path):
    """
    Detect the resolution of an image.

    Parameters:
    - image_path: Path to the image file.

    Returns:
    - Tuple representing the resolution (width, height).
    """
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Get the resolution of the image
    resolution = (image.shape[1], image.shape[0])

    return resolution

def resize_keep_ratio_images_in_folder(read_folder_path, target_size, write_folder_path, background_color='black'):
    """
    Process images within a folder and its subfolders. It resizes all images to the given size and write to the other folder.

    Parameters:
    - read_folder_path: Path to the main folder to read images.
    - target_size: resolution to change.
    - write_folder_path: path to the main folder to write images.
    - background_color: choose the background color. Only black works for now.

    Returns:
    - nothing
    """

    # Traverse through all subdirectories and their files
    for root, dirs, files in os.walk(read_folder_path):
        class_folder = root.split('/')[1]
        out_root = f'{write_folder_path}{class_folder}'
        # Check if the directory exists
        if not os.path.exists(out_root):
            # If the directory does not exist, create it
            os.makedirs(out_root)
            print(f"Directory '{out_root}' created successfully.")
        for index, file in enumerate(files, start=1):
            # Construct the full path to each image
            image_path = os.path.join(root, file)
            write_path = os.path.join(out_root, file)
            print(f'{image_path}\n{write_path}')

            resolution_original = detect_resolution(image_path)
            # Check if rescaling is needed
            if resolution_original[0] != target_size[0] or resolution_original[1] != target_size[1]:
                # Output the current image being processed
                print(f"Processing image: {image_path}")
                original_image = cv2.imread(image_path)

                # if image is verticl, rotate it so all images are horizontal.
                if resolution_original[0] < resolution_original[1]:
                    print(f'resolution was {resolution_original}, so rotated it')
                    original_image = cv2.rotate(original_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    resolution_original = (original_image.shape[1], original_image.shape[0])
                    
                desired_width = target_size[0]
                desired_height = target_size[1]
                width = resolution_original[0]
                height = resolution_original[1]
                ratio = min(desired_width / width, desired_height / height)

                # Resize the image with the calculated ratio
                resized_image = cv2.resize(original_image, (int(width * ratio), int(height * ratio)))

                # Create a black background canvas
                canvas = np.zeros((desired_height, desired_width, 3), dtype=np.uint8)

                # Calculate the position to paste the resized image on the canvas
                x_offset = (desired_width - resized_image.shape[1]) // 2
                y_offset = (desired_height - resized_image.shape[0]) // 2

                # Paste the resized image onto the canvas
                canvas[y_offset:y_offset+resized_image.shape[0], x_offset:x_offset+resized_image.shape[1]] = resized_image

                # Save the rescaled image with the new filename (in the new folder)
                cv2.imwrite(write_path, canvas)

main_folder_path = "dataset_rooftile_small/"
out_folder_path = "dataset_rooftile_keep_ratio_640/"
target_resolution = (640, 640)
resize_keep_ratio_images_in_folder(read_folder_path = main_folder_path, target_size = target_resolution, write_folder_path = out_folder_path)

