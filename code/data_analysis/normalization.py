import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import random

def normalize_image(img, factor=2.0):
    # Normalize the image by multiplying pixel values by a factor before applying normalization
    normalized_img = img * factor
    normalized_img = cv2.normalize(normalized_img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    return normalized_img

def plot_normalized_images(folder_path, num_examples=3, normalization_factor=2.0):
    # List all image files (including subdirectories) in the folder
    image_files = [os.path.join(root, f) for root, dirs, files in os.walk(folder_path) for f in files if f.lower().endswith('.png')]

    if not image_files:
        print("No PNG files found in the specified folder and its subdirectories.")
        return

    # Randomly select num_examples images
    sample_images = random.sample(image_files, num_examples)

    # Plot the original and normalized images
    plt.figure(figsize=(15, 5))

    for i, image_path in enumerate(sample_images, 1):
        # Read the original image
        original_img = cv2.imread(image_path)
        original_img_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)

        # Normalize the image
        normalized_img = normalize_image(original_img_rgb, factor=normalization_factor)

        # Plot original image
        plt.subplot(2, num_examples, i)
        plt.imshow(original_img_rgb)
        plt.title('Original {}'.format(i))
        plt.axis('off')

        # Plot normalized image
        plt.subplot(2, num_examples, i + num_examples)
        plt.imshow(normalized_img)
        plt.title('Normalized {}'.format(i))
        plt.axis('off')

    plt.show()
    
# Replace "/path/to/your/folder" with the actual path to your image folder
folder_path = "dataset_mini"
plot_normalized_images(folder_path)
