import cv2
import os
import matplotlib.pyplot as plt

def detect_resolution(image_path):
    """
    Detect the resolution of an image.

    Parameters:
    - image_path: Path to the image file.

    Returns:
    - Tuple representing the resolution (width, height).
    """
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Get the resolution of the image
    resolution = (image.shape[1], image.shape[0])

    return resolution

def rescale_image(image, scale_factor):
    """
    Rescale the image by the given scale factor.

    Parameters:
    - image: Input image
    - scale_factor: Factor by which to rescale the image

    Returns:
    - Rescaled image
    """
    return cv2.resize(image, (0, 0), fx=scale_factor, fy=scale_factor)

def process_images_in_folder(folder_path):
    """
    Process images within a folder and its subfolders.

    Parameters:
    - folder_path: Path to the main folder.

    Returns:
    - List of original resolutions
    - List of rescaled resolutions
    """
    resolutions_original = []
    resolutions_rescaled = []

    # Traverse through all subdirectories and their files
    for root, dirs, files in os.walk(folder_path):
        for file in enumerate(files, start=1):
            # Construct the full path to each image
            image_path = os.path.join(root, file)

            # Detect the original resolution
            resolution_original = detect_resolution(image_path)
            resolutions_original.append(resolution_original)

            # Check if rescaling is needed
            if resolution_original[0] > 3000 or resolution_original[1] > 3000:
                # Output the current image being processed
                print(f"Processing image: {image_path}")

                # Rescale the image by 0.25
                original_image = cv2.imread(image_path)
                rescaled_image = rescale_image(original_image, 0.25)

                # Save the rescaled image with the same filename
                cv2.imwrite(image_path, rescaled_image)

                # Record the rescaled resolution
                resolution_rescaled = (rescaled_image.shape[1], rescaled_image.shape[0])
                resolutions_rescaled.append(resolution_rescaled)
            else:
                # Use the original resolution if no rescaling is needed
                resolutions_rescaled.append(resolution_original)

    return resolutions_original, resolutions_rescaled

# Example usage:
main_folder_path = "dakpannen_dataset/"
original_resolutions, rescaled_resolutions = process_images_in_folder(main_folder_path)

# Visualize both original and rescaled resolutions using a scatter plot
plt.figure(figsize=(12, 6))

# Scatter plot for original resolutions
plt.subplot(1, 2, 1)
original_resolutions = [(res[0], res[1]) for res in original_resolutions]
plt.scatter([res[0] for res in original_resolutions], [res[1] for res in original_resolutions], marker='o')
plt.title('Original Image Resolutions')
plt.xlabel('Width')
plt.ylabel('Height')

# Scatter plot for rescaled resolutions
plt.subplot(1, 2, 2)
rescaled_resolutions = [(res[0], res[1]) for res in rescaled_resolutions]
plt.scatter([res[0] for res in rescaled_resolutions], [res[1] for res in rescaled_resolutions], marker='o')
plt.title('Rescaled Image Resolutions (if needed)')
plt.xlabel('Width')
plt.ylabel('Height')

plt.tight_layout()
plt.show()
