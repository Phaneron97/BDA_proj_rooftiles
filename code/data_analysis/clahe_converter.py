import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import random

def apply_clahe(img):
    # Convert the image to LAB color space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    # Split the LAB image into channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to the L-channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    
    # Merge the CLAHE-enhanced L-channel with the original A and B channels
    limg = cv2.merge((cl, a, b))
    
    # Convert the LAB image back to BGR color space
    clahe_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    return clahe_img

def plot_all_images_with_histogram(imgs, processed_imgs):
    # Select 3 random images
    sample_images = random.sample(range(len(imgs)), 3)

    # Plot the original and processed images
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

        # Plot processed image
        plt.subplot(3, 4, 4*i-1)
        plt.imshow(cv2.cvtColor(processed_imgs[idx], cv2.COLOR_BGR2RGB))
        plt.title('CLAHE Processed {}'.format(idx+1))
        plt.axis('off')

        # Plot histogram of the processed image
        plt.subplot(3, 4, 4*i)
        plt.hist(cv2.cvtColor(processed_imgs[idx], cv2.COLOR_BGR2GRAY).ravel(), 256, [0, 256])
        plt.title('Histogram {}'.format(idx+1))
        plt.axvline(x=np.mean(cv2.cvtColor(processed_imgs[idx], cv2.COLOR_BGR2GRAY)), color='r', linestyle='dashed', linewidth=2)
        plt.xlabel('Intensity')
        plt.ylabel('Frequency')
    
    plt.show()

def convert_images_to_clahe(folder_path):
    processed_imgs = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.png'):
                file_path = os.path.join(root, file)
                img = cv2.imread(file_path)

                # Apply CLAHE processing
                processed_img = apply_clahe(img)
                processed_imgs.append(processed_img)

                # Save the processed image
                cv2.imwrite(file_path, processed_img)

                print(f"Processed: {file_path} -> {file_path}")

    return processed_imgs

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
    processed_imgs = convert_images_to_clahe(folder_path)
    plot_all_images_with_histogram(imgs, processed_imgs)
