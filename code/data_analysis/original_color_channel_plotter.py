import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import random

def select_random_images(folder_path, num_images=3):
    # List all image files (including subdirectories) in the folder
    image_files = [os.path.join(root, f) for root, dirs, files in os.walk(folder_path) for f in files if f.lower().endswith('.png')]

    if len(image_files) < num_images:
        print(f"Insufficient number of images ({num_images}) in the specified folder and its subdirectories.")
        return []

    # Select num_images random images
    selected_images = random.sample(image_files, num_images)
    
    return selected_images

def calculate_histograms(img):
    # Calculate histograms for the current image
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    hist_blue = cv2.calcHist([img_rgb], [0], None, [256], [0, 256])
    hist_green = cv2.calcHist([img_rgb], [1], None, [256], [0, 256])
    hist_red = cv2.calcHist([img_rgb], [2], None, [256], [0, 256])

    # Normalize histograms
    # hist_blue /= np.sum(hist_blue)
    # hist_green /= np.sum(hist_green)
    # hist_red /= np.sum(hist_red)

    return hist_blue, hist_green, hist_red

def show_images_with_histograms(image_files):
    # Create a single figure for all images and their histograms
    num_images = len(image_files)
    fig, axes = plt.subplots(num_images, 2, figsize=(12, 5*num_images))

    for i, image_file in enumerate(image_files):
        # Load the image
        img = cv2.imread(image_file)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Display the original image
        axes[i, 0].imshow(img_rgb)
        axes[i, 0].axis('off')
        axes[i, 0].set_title(f'Image {i+1}')

        # Calculate and plot histograms
        hist_blue, hist_green, hist_red = calculate_histograms(img)
        axes[i, 1].plot(hist_blue, color='blue', label='Blue Channel')
        axes[i, 1].plot(hist_green, color='green', label='Green Channel')
        axes[i, 1].plot(hist_red, color='red', label='Red Channel')
        axes[i, 1].set_title('')
        axes[i, 1].set_xlabel('Pixel Intensity')
        axes[i, 1].set_ylabel('Frequency')
        axes[i, 1].legend()

    plt.tight_layout()
    plt.show()

def show_random_images_with_histograms(folder_path, num_images=3):
    # Select num_images random images
    selected_images = select_random_images(folder_path, num_images)
    
    # Display the original images and their histograms in one figure
    show_images_with_histograms(selected_images)

# Replace "/path/to/your/folder" with the actual path to your image folder
folder_path = "code/data_analysis/dataset_mini"
show_random_images_with_histograms(folder_path)
