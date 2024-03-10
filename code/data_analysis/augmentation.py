import os
import cv2
import hashlib
import numpy as np
from skimage import exposure, img_as_ubyte

def perform_image_augmentation(input_path, output_path, num_samples):
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
        augmented_images = [original_image.copy() for _ in range(num_samples)]
        for i in range(num_samples):
            # Add your augmentation operations here
            augmented_images[i] = apply_horizontal_flip(augmented_images[i], flip_prob=0.5)  # Horizontal flip
            augmented_images[i] = apply_random_rotation(augmented_images[i], rotation_prob=0.5)  # Random rotation (90 or 270 degrees)
            augmented_images[i] = apply_random_zoom(augmented_images[i], zoom_prob=0.5, zoom_range=(1.1, 1.5))  # Random zoom
            augmented_images[i] = apply_vertical_flip(augmented_images[i], flip_prob=0.5)  # Vertical flip

        # Save augmented images under the same subdirectory as the original image
        output_subdirectory = os.path.join(output_directory, os.path.basename(os.path.dirname(image_file)))
        os.makedirs(output_subdirectory, exist_ok=True)

        for i, augmented_image in enumerate(augmented_images):
            output_file_path = os.path.join(output_subdirectory, f"{os.path.basename(image_file).split('.')[0]}_{i}.jpg")
            cv2.imwrite(output_file_path, augmented_image)

        # Add the processed image hash to the set
        processed_images.add(image_hash)

def apply_horizontal_flip(image, flip_prob):
    if np.random.rand() < flip_prob:
        flipped_image = cv2.flip(image, 1)  # Horizontal flip
        return flipped_image
    else:
        return image

def apply_vertical_flip(image, flip_prob):
    if np.random.rand() < flip_prob:
        flipped_image = cv2.flip(image, 0)  # Vertical flip
        return flipped_image
    else:
        return image

def apply_random_rotation(image, rotation_prob, max_angle=270):
    if np.random.rand() < rotation_prob:
        angle = np.random.choice([90, 270])
        rows, cols, _ = image.shape
        rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
        rotated_image = cv2.warpAffine(image, rotation_matrix, (cols, rows))
        return rotated_image
    else:
        return image

def apply_random_zoom(image, zoom_prob, zoom_range=(0.8, 1.2)):
    if np.random.rand() < zoom_prob:
        zoom_factor = np.random.uniform(low=zoom_range[0], high=zoom_range[1])
        rows, cols, _ = image.shape
        zoom_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), 0, zoom_factor)
        zoomed_image = cv2.warpAffine(image, zoom_matrix, (cols, rows))
        return zoomed_image
    else:
        return image

if __name__ == "__main__":
    input_directory = 'dataset_mini'
    output_directory = 'dataset_mini'
    num_samples_to_generate = 4

    try:
        perform_image_augmentation(input_directory, output_directory, num_samples_to_generate)
        print(f"Image augmentation completed successfully. Augmented images saved in '{output_directory}/augmented_images'.")
    except Exception as e:
        print(f"Error during image augmentation: {e}")