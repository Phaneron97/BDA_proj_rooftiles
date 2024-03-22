import cv2
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

def resize_images_in_folder(read_folder_path, target_size, write_folder_path):
    """
    Process images within a folder and its subfolders. It resizes all images to the given size and write to the other folder.

    Parameters:
    - read_folder_path: Path to the main folder to read images.
    - target_size: resolution to change.
    - write_folder_path: path to the main folder to write images.

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
                # resize image to target size.
                resized_image = cv2.resize(original_image, target_size)

                # Save the rescaled image with the new filename (in the new folder)
                cv2.imwrite(write_path, resized_image)

main_folder_path = "dataset_rooftile_small/"
out_folder_path = "dataset_rooftile_640/"
target_resolution = (640, 640)
resize_images_in_folder(read_folder_path = main_folder_path, target_size = target_resolution, write_folder_path = out_folder_path)

