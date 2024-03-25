import cv2
import os

def apply_clahe_to_images(directory):
    # Create CLAHE object with specified settings
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    
    # Iterate through all subdirectories and files
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if file is a PNG image
            if file.endswith('.png'):
                # Read image
                image_path = os.path.join(root, file)
                img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                
                # Apply CLAHE
                clahe_img = clahe.apply(img)
                
                # Write CLAHE-enhanced image
                cv2.imwrite(image_path, clahe_img)
                print(f"CLAHE applied to: {file} in {root}")

# Specify the directory containing images
directory = 'code\data_analysis\dataset\dataset'

# Apply CLAHE to images in the specified directory
apply_clahe_to_images(directory)
