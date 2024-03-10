import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import random

def get_images_in_folder(folder_path):
    image_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.png'):
                input_path = os.path.join(root, file)
                image_files.append(input_path)
    return image_files

def select_random_images(folder_path, num_images=3):
    image_files = get_images_in_folder(folder_path)

    if len(image_files) < num_images:
        print(f"Insufficient number of images ({num_images}) in the specified folder and its subdirectories.")
        return []

    selected_images = random.sample(image_files, num_images)
    return selected_images

def calculate_histograms(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    hist_blue = cv2.calcHist([img_rgb], [0], None, [256], [0, 256])
    hist_green = cv2.calcHist([img_rgb], [1], None, [256], [0, 256])
    hist_red = cv2.calcHist([img_rgb], [2], None, [256], [0, 256])

    return hist_blue, hist_green, hist_red

def show_images_with_histograms(image_files):
    num_images = len(image_files)
    fig, axes = plt.subplots(num_images, 2, figsize=(12, 5*num_images))

    for i, image_file in enumerate(image_files):
        img = cv2.imread(image_file)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        axes[i, 0].imshow(img_rgb)
        axes[i, 0].axis('off')
        axes[i, 0].set_title(f'Image {i+1}')

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
    selected_images = select_random_images(folder_path, num_images)
    show_images_with_histograms(selected_images)

folder_path = "code/data_analysis/dataset_mini"
show_random_images_with_histograms(folder_path)
