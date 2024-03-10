import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import random

def convert_to_grayscale(img):
    # Convert the image to grayscale
    grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return grayscale_img

def plot_all_images_with_histogram(imgs, grayscale_imgs):
    # Select 3 random images
    sample_images = random.sample(range(len(imgs)), 3)

    # Plot the original and grayscale images
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

        # Plot grayscale image
        plt.subplot(3, 4, 4*i-1)
        plt.imshow(grayscale_imgs[idx], cmap='gray')
        plt.title('Grayscale {}'.format(idx+1))
        plt.axis('off')

        # Plot histogram of the grayscale image
        plt.subplot(3, 4, 4*i)
        plt.hist(grayscale_imgs[idx].ravel(), 256, [0, 256])
        plt.title('Histogram {}'.format(idx+1))
        plt.axvline(x=np.mean(grayscale_imgs[idx]), color='r', linestyle='dashed', linewidth=2)
        plt.xlabel('Intensity')
        plt.ylabel('Frequency')
    
    plt.show()

def convert_images_to_grayscale(folder_path):
    grayscale_imgs = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.png'):
                folder_path = os.path.join(root, file)
                img = cv2.imread(folder_path)

                # Convert the image to grayscale
                grayscale_img = convert_to_grayscale(img)
                grayscale_imgs.append(grayscale_img)

                # Save the grayscale image, overwriting the existing file
                cv2.imwrite(folder_path, grayscale_img)

                print(f"Converted: {folder_path} -> {folder_path}")
    return grayscale_imgs

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
    folder_path = "dataset_mini"

    imgs = get_images_in_folder(folder_path)
    grayscale_imgs = convert_images_to_grayscale(folder_path)
    plot_all_images_with_histogram(imgs, grayscale_imgs)
