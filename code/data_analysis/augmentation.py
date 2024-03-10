import cv2
import os
import Augmentor

# The method / function for perfoming Image augmentation. The num_samples is the amount of samples it'll make. 
def perform_image_augmentation(input_path, output_path, num_samples=5):
    # Create an Augmentor Pipeline
    image = Augmentor.Pipeline(input_path, output_directory=output_path)

    # Define augmentation operations with configurable parameters
    image.flip_left_right(probability=0.5)
    # image.black_and_white(probability=0.1)
    image.rotate(probability=0.3, max_left_rotation=10, max_right_rotation=10)
    # image.skew(probability=0.4, magnitude=0.5)
    image.zoom(probability=0.2, min_factor=1.1, max_factor=1.5)

    # Add a resize operation to ensure a fixed ratio of 640x640
    image.resize(1, width=640, height=640)

    # Perform augmentation and generate sample images.
    image.sample(num_samples)

if __name__ == "__main__":
    input_directory = 'dataset_mini' # I'm using the mini dataset for testing.
    output_directory = 'augmented_dataset' # This will be the folder name of where the sample images are saved.
    num_samples_to_generate = 5 # Amount of Sample Images. 

    try:
        perform_image_augmentation(input_directory, output_directory, num_samples_to_generate)
        print(f"Image augmentation completed successfully. Augmented images saved in '{output_directory}'.")
    except Exception as e:
        print(f"Error during image augmentation: {e}")