import os
import cv2
import hashlib
import numpy as np

def perform_image_augmentation(input_path, output_path, horizontal_flip, vertical_flip, random_rotation, random_zoom):
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
        augmented_images = []
        if horizontal_flip:
            augmented_images.append(apply_mirroring(original_image, True))
        if vertical_flip:
            augmented_images.append(apply_mirroring(original_image, False))
        if random_rotation:
            augmented_images.append(apply_random_rotation(original_image))
        if random_zoom:
            augmented_images.append(apply_random_zoom(original_image))

        # Save augmented images under the same subdirectory as the original image
        output_subdirectory = os.path.join(output_directory, os.path.basename(os.path.dirname(image_file)))
        os.makedirs(output_subdirectory, exist_ok=True)

        # Save each augmented image separately
        for i, augmented_image in enumerate(augmented_images):
            output_file_path = os.path.join(output_subdirectory, f"{os.path.basename(image_file).split('.')[0]}_{i}.jpg")
            cv2.imwrite(output_file_path, augmented_image)

        # Add the processed image hash to the set
        processed_images.add(image_hash)

def apply_mirroring(image, horizontal):
    if horizontal:
        flipped_image = cv2.flip(image, 1)  # Horizontal flip if True
    else:
        flipped_image = cv2.flip(image, 0)  # Vertical flip if False
    return flipped_image

def apply_random_rotation(image):
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
    input_directory = 'dataset_mini' # dataset_mini is a folder used for testing
    output_directory = 'dataset_mini' 
    horizontal_flip = True 
    vertical_flip = True 
    random_rotation = True 
    random_zoom = True

    try:
        perform_image_augmentation(input_directory, output_directory, horizontal_flip, vertical_flip, random_rotation, random_zoom)
        print(f"Image augmentation completed successfully. Augmented images saved in '{output_directory}/augmented_images'.")
    except Exception as e:
        print(f"Error during image augmentation: {e}")
