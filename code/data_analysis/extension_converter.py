import os
import cv2

def convert_images_to_png(input_folder):
    # Loop through subfolders and convert images to .png
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            # Check if the file is either jpg or jpeg
            if file.lower().endswith(('.jpg', '.jpeg')):
                input_path = os.path.join(root, file)

                # Read the image using OpenCV
                image = cv2.imread(input_path)

                # Construct the output path by replacing the extension with .png
                output_path = os.path.splitext(input_path)[0] + '.png'

                # Save the image as .png, overwriting the existing file
                cv2.imwrite(output_path, image)

                print(f"Converted: {input_path} -> {output_path}")

                # Remove the old JPG image
                os.remove(input_path)

if __name__ == "__main__":
    input_folder = 'code/data_analysis/dataset_mini'

    convert_images_to_png(input_folder)
