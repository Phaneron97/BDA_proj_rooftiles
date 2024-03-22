import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def calculate_aspect_ratio(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        aspect_ratio = width / height
    return aspect_ratio

def find_closest_aspect_ratio(target_ratio, ratios_list):
    return min(ratios_list, key=lambda x: abs(x - target_ratio))

def visualize_aspect_ratios(folder_path, target_ratios=[1, 4/3, 3/2, 16/9]):
    aspect_ratios = []

    # Recursively iterate through all image files in the folder and its subfolders
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):  # Add more extensions if needed
                image_path = os.path.join(root, filename)
                aspect_ratio = calculate_aspect_ratio(image_path)
                closest_aspect_ratio = find_closest_aspect_ratio(aspect_ratio, target_ratios)
                aspect_ratios.append(closest_aspect_ratio)

    # Count occurrences of each closest aspect ratio
    unique_ratios, counts = np.unique(aspect_ratios, return_counts=True)

    # Bar plot with thinner bars
    plt.figure(figsize=(10, 6))
    plt.bar(unique_ratios, counts, color='blue', alpha=0.7, width=0.15)  # Adjust the width parameter
    plt.title('Closest Aspect Ratios Bar Plot in {}'.format(folder_path))
    plt.xlabel('Closest Aspect Ratio')
    plt.ylabel('Frequency')
    plt.xticks(unique_ratios, labels=['{:.2f}'.format(ratio) for ratio in unique_ratios])
    plt.grid(axis='y')
    plt.show()


if __name__ == "__main__":
    # Replace 'your_dataset_folder_path' with the actual path to your dataset folder
    dataset_folder_path = 'dataset/'
    
    visualize_aspect_ratios(dataset_folder_path)
