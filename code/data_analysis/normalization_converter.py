import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import random

### Normalize image (leave empty for default settings):
# alpha (norm value to normalize to or the lower range boundary)
# beta (upper range boundary )
# normtype (normalization algorithm used)
def normalize_image(img, alpha=0, beta=200, normType=cv2.NORM_MINMAX):
    # Normalize the image
    normalized_img = cv2.normalize(img, None, alpha, beta, normType)
    return normalized_img

def plot_all_images_with_histogram(imgs):
    # Select 3 random images
    sample_images = random.sample(range(len(imgs)), 3)

    # Plot the original and normalized images
    plt.figure(figsize=(15, 5))

    for i, idx in enumerate(sample_images, 1):
        # Plot original image
        plt.subplot(3, 4, 4*i-3)
        plt.imshow(cv2.cvtColor(imgs[idx], cv2.COLOR_BGR2RGB))
        plt.title('Original {}'.format(idx+1))
        plt.axis('off')

        # Plot histogram of the original image
        plt.subplot(3, 4, 4*i-2)
        plt.hist(imgs[idx].ravel(), 256, [0, 256])
        plt.title('Histogram {}'.format(idx+1))
        plt.axvline(x=np.mean(imgs[idx]), color='r', linestyle='dashed', linewidth=2)
        plt.xlabel('Intensity')
        plt.ylabel('Frequency')

        # Plot normalized image
        normalized_img = normalize_image(imgs[idx])
        plt.subplot(3, 4, 4*i-1)
        plt.imshow(normalized_img, cmap='gray')
        plt.title('Normalized {}'.format(idx+1))
        plt.axis('off')

        # Plot histogram of the normalized image
        plt.subplot(3, 4, 4*i)
        plt.hist(normalized_img.ravel(), 256, [0, 256])
        plt.title('Histogram {}'.format(idx+1))
        plt.axvline(x=np.mean(normalized_img), color='r', linestyle='dashed', linewidth=2)
        plt.xlabel('Intensity')
        plt.ylabel('Frequency')
    
    plt.show()

def get_images_in_folder(folder_path):
    image_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.png'):
                input_path = os.path.join(root, file)
                img = cv2.imread(input_path)
                image_files.append(img)
    return image_files

if __name__ == "__main__":
    folder_path = "code/data_analysis/dataset_mini"

    imgs = get_images_in_folder(folder_path)
    plot_all_images_with_histogram(imgs)
