import os
import imgaug.augmenters as iaa
from PIL import Image
import numpy as np

def augment_image(image_path, num_copies):
    # Define augmentations you want to apply
    flipper = iaa.Fliplr(1.0)  # horizontal flips / Mirror
    rotator = iaa.Affine(rotate=(1, 359))  # rotation
    scaler = iaa.Affine(scale=(1.1, 1.3))  # zoom in
    noise = iaa.AdditiveGaussianNoise(scale=(0.02*255, 0.10*255))  # add Gaussian noise
    brightness_low = iaa.Multiply((0.5, 0.9)) # nice
    brightness_high = iaa.Multiply((1.1, 1.5))

   # Load image
    image = Image.open(image_path)
    image = np.array(image)  # Convert image to NumPy array

    # Define all augmentation effects with unique identifiers for filenames
    all_augmentations = {
        'flipper': flipper,
        'rotator': rotator,
        'scaler': scaler,
        'noise': noise,
        'brightness': np.random.choice([brightness_low, brightness_high]) # Random choice between low of high brightness
    }

    # Generate a list of augmentation effects for each copy
    copies_augmentations = []
    for _ in range(num_copies):
        # Shuffle the list of augmentation effects
        shuffled_augmentations = list(all_augmentations.values())
        np.random.shuffle(shuffled_augmentations)
        # Ensure each copy has a unique combination of effects with allowance for one similar effect
        unique_effects = np.random.choice(shuffled_augmentations, size=np.random.randint(1, len(shuffled_augmentations) + 1), replace=False)
        copies_augmentations.append(unique_effects)

    # Apply augmentations for each copy
    for idx, copy_augmentations in enumerate(copies_augmentations):
        if len(copy_augmentations) > 0:
            # Apply selected augmentations
            seq = iaa.Sequential(copy_augmentations)
            augmented_image = seq(images=[image])[0]  # Apply augmentation to the image array
            augmented_image = Image.fromarray(augmented_image)  # Convert augmented image array back to PIL Image

            # Generate a filename based on applied augmentation effects
            augmentation_names = '_'.join(name for name, augmentation in all_augmentations.items() if augmentation in copy_augmentations)
            filename = os.path.splitext(os.path.basename(image_path))[0] + f"_augmented_{augmentation_names}_{idx}.png"

            # Save augmented image
            augmented_image.save(os.path.join(os.path.dirname(image_path), filename), format="PNG")

def augment_images_in_directory(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.png'):
                image_path = os.path.join(root, file)
                
                # Randomly choose the number of copies to generate (between 1 and 3)
                num_copies = np.random.randint(1, 4)
                
                # Augment the image with the chosen number of copies
                augment_image(image_path, num_copies)

if __name__ == "__main__":
    root_directory = r"code\data_analysis\dataset\dataset_mini\train"  # Change this to your root directory containing images
    augment_images_in_directory(root_directory)