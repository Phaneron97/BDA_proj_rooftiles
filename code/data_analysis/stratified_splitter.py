import os
import shutil
from sklearn.model_selection import train_test_split

<<<<<<< HEAD
def stratified_split(source_folder, class_folder, train_ratio=0.7):
    class_path = os.path.join(source_folder, class_folder)
    
    folders = os.listdir(class_path)
    if len(folders) < 2:
        print(f"Not enough samples in '{class_folder}' for stratified split. Using regular split.")
        train_folders, test_folders = train_test_split(folders, train_size=train_ratio, random_state=42)
    else:
        train_folders, test_folders = train_test_split(folders, train_size=train_ratio, stratify=folders, random_state=42)

    return train_folders, test_folders

def organize_folders(source_folder, train_ratio=0.7):
    folder_b = os.path.join(source_folder, "b")
    folder_o = os.path.join(source_folder, "o")

    if not os.path.exists(folder_b):
        os.makedirs(folder_b)

    if not os.path.exists(folder_o):
        os.makedirs(folder_o)

    for class_folder in ["b", "o"]:
        train_folders, test_folders = stratified_split(source_folder, class_folder, train_ratio)

        for folder in train_folders:
            source_path = os.path.join(source_folder, class_folder, folder)
            destination_path = os.path.join(source_folder, "train", class_folder, folder)
            shutil.move(source_path, destination_path)
            print(f"Moved '{folder}' from '{class_folder}' to 'train/{class_folder}'")

        for folder in test_folders:
            source_path = os.path.join(source_folder, class_folder, folder)
            destination_path = os.path.join(source_folder, "test", class_folder, folder)
            shutil.move(source_path, destination_path)
            print(f"Moved '{folder}' from '{class_folder}' to 'test/{class_folder}'")

if __name__ == "__main__":
    source_folder = "code/data_analysis/dataset/dataset_mini"  # Update with the actual path to your source folder
    train_ratio = 0.7  # Change this to adjust the training ratio

    train_folder = os.path.join(source_folder, "train")
    test_folder = os.path.join(source_folder, "test")

    if not os.path.exists(train_folder):
        os.makedirs(train_folder)

    if not os.path.exists(test_folder):
        os.makedirs(test_folder)

=======

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

>>>>>>> 2431d67a9047998c250e6cc3458cc54ba36da22f
    organize_folders(source_folder, train_ratio)
