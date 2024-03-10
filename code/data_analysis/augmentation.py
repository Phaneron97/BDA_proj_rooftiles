import os
import cv2
import hashlib

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
            augmented_images[i] = cv2.flip(augmented_images[i], 1)  # Horizontal flip

        # Save augmented images under the same subdirectory as the original image
        output_subdirectory = os.path.join(output_directory, os.path.basename(os.path.dirname(image_file)))
        os.makedirs(output_subdirectory, exist_ok=True)

        for i, augmented_image in enumerate(augmented_images):
            output_file_path = os.path.join(output_subdirectory, f"{os.path.basename(image_file).split('.')[0]}.jpg")
            cv2.imwrite(output_file_path, augmented_image)

        # Add the processed image hash to the set
        processed_images.add(image_hash)

if __name__ == "__main__":
    input_directory = 'dataset_mini'
    output_directory = 'dataset_mini'
    num_samples_to_generate = 1

    try:
        perform_image_augmentation(input_directory, output_directory, num_samples_to_generate)
        print(f"Image augmentation completed successfully. Augmented images saved in '{output_directory}/augmented_images'.")
    except Exception as e:
        print(f"Error during image augmentation: {e}")