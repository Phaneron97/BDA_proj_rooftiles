import os
import shutil
from sklearn.model_selection import train_test_split

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

    organize_folders(source_folder, train_ratio)
