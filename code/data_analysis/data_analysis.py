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

dataset_dir = "dataset/"  # folder where the image dataset is present

# Check if the directory exists
if os.path.exists(dataset_dir):
    # Get a list of all files in the directory
    image_files = [f for f in os.listdir(dataset_dir) if os.path.isfile(os.path.join(dataset_dir, f))]

    # Ensure there are at least 10 images in the directory
    if len(image_files) >= 10:
        resolutions_original = []

        # Loop through the first 10 images
        for i in range(10):
            # Construct the full path to each image
            image_path = os.path.join(dataset_dir, image_files[i])

            # Detect the original resolution
            resolution_original = detect_resolution(image_path)
            resolutions_original.append(resolution_original)

            # Check if rescaling is needed (is the image is 4k, rescale it by 0.25)
            if resolution_original[0] > 3000 or resolution_original[1] > 3000:
                # Rescale the image by 0.25
                original_image = cv2.imread(image_path)
                rescaled_image = rescale_image(original_image, 0.25)

                # Save the rescaled image with the same filename
                cv2.imwrite(image_path, rescaled_image)

        # Visualize original and rescaled resolutions using a scatter plot
        plt.figure(figsize=(12, 6))

        # Scatter plot for original resolutions
        plt.subplot(1, 2, 1)
        resolutions_original = [(res[0], res[1]) for res in resolutions_original]
        plt.scatter([res[0] for res in resolutions_original], [res[1] for res in resolutions_original], marker='o')
        plt.title('Original Image Resolutions')
        plt.xlabel('Width')
        plt.ylabel('Height')

        # Scatter plot for rescaled resolutions
        plt.subplot(1, 2, 2)
        resolutions_rescaled = [(res[0]*0.25, res[1]*0.25) if res[0] > 3000 or res[1] > 3000 else res for res in resolutions_original]
        plt.scatter([res[0] for res in resolutions_rescaled], [res[1] for res in resolutions_rescaled], marker='o')
        plt.title('Rescaled Image Resolutions (if needed)')
        plt.xlabel('Width')
        plt.ylabel('Height')

        plt.tight_layout()
        plt.show()
    else:
        print("There are not enough images in the directory.")
else:
    print(f"The specified directory '{dataset_dir}' does not exist.")