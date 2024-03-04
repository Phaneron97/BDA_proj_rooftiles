import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_and_process_images(folder_path):
    """
    Load and process all images within a folder and its subfolders efficiently.

    Parameters:
    - folder_path: Path to the main folder.

    Returns:
    - List of flattened RGB arrays for each image.
    """
    rgb_values = []

    # Traverse through all subdirectories and their files
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Construct the full path to each image
            image_path = os.path.join(root, file)

            # Load image with the IMREAD_UNCHANGED flag to preserve alpha channel
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

            if image is not None:
                # Extract RGB values
                if image.shape[2] == 3:  # Check if image has 3 channels (RGB)
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    rgb_values.append(image_rgb.reshape(-1, 3))

    return np.vstack(rgb_values)

def plot_rgb_values(rgb_values):
    """
    Plot RGB values using matplotlib.

    Parameters:
    - rgb_values: List of RGB values.
    """
    plt.figure(figsize=(10, 6))

    # Scatter plot for RGB values
    plt.scatter(rgb_values[:, 0], rgb_values[:, 1], c=rgb_values / 255.0, marker='o', s=5)
    plt.title('RGB Values of Images')
    plt.xlabel('Red')
    plt.ylabel('Green')

    plt.show()

# Example usage:
main_folder_path = "dataset_mini/"
rgb_values = load_and_process_images(main_folder_path)
plot_rgb_values(rgb_values)