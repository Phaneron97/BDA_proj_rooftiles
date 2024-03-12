import os
import shutil
from sklearn.model_selection import train_test_split


"""NOTE:

New test and train data will ALWAYS be put in the same folder. Old data will be kept. 

"""

# Clear existing train and test folder (if there are any) and create a new one 
def clear_existing_train_test_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)


# Copy file from original folder to destination
def copy_to_train_test_folder(source_files, destination_folder, original_folder, subdir):
    """Copies files from source to destination."""
    for file in source_files:
        source_path = os.path.join(subdir, file)
        destination_path = os.path.join(destination_folder, os.path.basename(subdir), file)
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.copy(source_path, destination_path)
        print(f"Copied '{file}' from '{original_folder}' to '{os.path.basename(destination_folder)}/{original_folder}/{os.path.basename(subdir)}'")


# Stratified split (keep ratio between all rooftile types), use seed 42 (answer to everything)
def stratified_split(files, train_ratio=0.7, random_state=42):
    if len(files) < 2:
        print("Not enough samples for stratified split. Using regular split.")
        train_files, test_files = train_test_split(files, random_state=random_state, train_size=train_ratio)
    else:
        train_files, test_files = train_test_split(files, random_state=random_state, train_size=train_ratio)
    return train_files, test_files


# if folder "b"/"o", put in train/test set "b"/"o"
def organize_folders(source_folder, train_ratio=0.7):
    for original_folder in ["b", "o"]:
        original_path = os.path.join(source_folder, original_folder)
        train_folder = os.path.join(source_folder, "train", original_folder)
        test_folder = os.path.join(source_folder, "test", original_folder)

        # Clear existing train and test folders
        clear_existing_train_test_folder(train_folder)
        clear_existing_train_test_folder(test_folder)

        for subdir, _, files in os.walk(original_path):
            if files:
                train_files, test_files = stratified_split(files, train_ratio)

                # Copy files to train folder
                copy_to_train_test_folder(train_files, train_folder, original_folder, subdir)

                # Copy files to test folder
                copy_to_train_test_folder(test_files, test_folder, original_folder, subdir)

if __name__ == "__main__":
    source_folder = "code/data_analysis/dataset/dataset_mini"  # Update with source folder of which to create testdata from
    train_ratio = 0.7  # Change this to adjust the training ratio

    organize_folders(source_folder, train_ratio)
