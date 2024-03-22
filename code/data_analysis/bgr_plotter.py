import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

def calculate_average_histogram(folder_path):
    # List all image files (including subdirectories) in the folder
    image_files = [os.path.join(root, f) for root, dirs, files in os.walk(folder_path) for f in files if f.lower().endswith('.png')]

    if not image_files:
        print("No PNG files found in the specified folder and its subdirectories.")
        return

    # Initialize variables to accumulate histograms
    total_hist_blue = np.zeros((256, 1))
    total_hist_green = np.zeros((256, 1))
    total_hist_red = np.zeros((256, 1))

    # Calculate total histograms
    for image_file in image_files:
        print("current image_file", image_file)
        img = cv2.imread(image_file)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        hist_blue = cv2.calcHist([img_rgb], [0], None, [256], [0, 256])
        hist_green = cv2.calcHist([img_rgb], [1], None, [256], [0, 256])
        hist_red = cv2.calcHist([img_rgb], [2], None, [256], [0, 256])

        total_hist_blue += hist_blue
        total_hist_green += hist_green
        total_hist_red += hist_red

    # Calculate average histograms
    avg_hist_blue = total_hist_blue / len(image_files)
    avg_hist_green = total_hist_green / len(image_files)
    avg_hist_red = total_hist_red / len(image_files)

    # Plot average histograms on the same axes
    plt.figure(figsize=(8, 5))

    plt.plot(avg_hist_blue, color='blue', label='Blue Channel')
    plt.plot(avg_hist_green, color='green', label='Green Channel')
    plt.plot(avg_hist_red, color='red', label='Red Channel')

    plt.title('Average Color Histograms for All Images')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Normalized Frequency')
    plt.legend()
    plt.show()

# Replace "/path/to/your/folder" with the actual path to your image folder
folder_path = "dataset_mini"
calculate_average_histogram(folder_path)
