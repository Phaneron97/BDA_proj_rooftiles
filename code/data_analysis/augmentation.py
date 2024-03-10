import os
import cv2
import hashlib
import numpy as np

def perform_image_augmentation(input_path, output_path):
    # Create the output directory if it doesn't exist
    output_directory = os.path.join(output_path, "augmented_images")
    os.makedirs(output_directory, exist_ok=True)

    # Get a list of all image files recursively in the input directory
    image_files = [os.path.join(root, f) for root, dirs, files in os.walk(input_path) for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # Keep track of processed images to avoid duplicates
    processed_images = set()

    # Loop through each image and perform augmentation
    for image_file in image_files:
        # Check if the image has already been processed
        image_hash = hashlib.md5(image_file.encode()).hexdigest()
        if image_hash in processed_images:
            continue

        # Read the input image using OpenCV
        original_image = cv2.imread(image_file)

        # Define augmentation operations with configurable parameters
        horizontal_flip_image = apply_horizontal_flip(original_image)
        vertical_flip_image = apply_vertical_flip(original_image)
        random_rotation_image = apply_random_rotation(original_image)
        random_zoom_image = apply_random_zoom(original_image)

        # Save augmented images under the same subdirectory as the original image
        output_subdirectory = os.path.join(output_directory, os.path.basename(os.path.dirname(image_file)))
        os.makedirs(output_subdirectory, exist_ok=True)

        # Save each augmented image separately
        output_file_path = os.path.join(output_subdirectory, f"{os.path.basename(image_file).split('.')[0]}_horizontal_flip.jpg")
        cv2.imwrite(output_file_path, horizontal_flip_image)

        output_file_path = os.path.join(output_subdirectory, f"{os.path.basename(image_file).split('.')[0]}_vertical_flip.jpg")
        cv2.imwrite(output_file_path, vertical_flip_image)

        output_file_path = os.path.join(output_subdirectory, f"{os.path.basename(image_file).split('.')[0]}_random_rotation.jpg")
        cv2.imwrite(output_file_path, random_rotation_image)

        output_file_path = os.path.join(output_subdirectory, f"{os.path.basename(image_file).split('.')[0]}_random_zoom.jpg")
        cv2.imwrite(output_file_path, random_zoom_image)

        # Add the processed image hash to the set
        processed_images.add(image_hash)

def apply_horizontal_flip(image):
    flipped_image = cv2.flip(image, 1)  # Horizontal flip
    return flipped_image

def apply_vertical_flip(image):
    flipped_image = cv2.flip(image, 0)  # Vertical flip
    return flipped_image

def apply_random_rotation(image, max_angle=270):
    angle = np.random.choice([90, 270])
    rows, cols, _ = image.shape
    rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))
    return rotated_image

def apply_random_zoom(image, zoom_range=(1.1, 1.3)):
    zoom_factor = np.random.uniform(low=zoom_range[0], high=zoom_range[1])
    rows, cols, _ = image.shape
    zoom_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), 0, zoom_factor)
    zoomed_image = cv2.warpAffine(image, zoom_matrix, (cols, rows))
    return zoomed_image

if __name__ == "__main__":
    input_directory = 'dataset_mini'
    output_directory = 'dataset_mini'

    try:
        perform_image_augmentation(input_directory, output_directory)
        print(f"Image augmentation completed successfully. Augmented images saved in '{output_directory}/augmented_images'.")
    except Exception as e:
        print(f"Error during image augmentation: {e}")