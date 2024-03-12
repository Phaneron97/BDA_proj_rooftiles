import os
import shutil
from sklearn.model_selection import train_test_split

def stratified_split(files, train_ratio=0.7, random_state=42):
    if len(files) < 2:
        print("Not enough samples for stratified split. Using regular split.")
        train_files, test_files = train_test_split(files, random_state=random_state, train_size=train_ratio)
    else:
        train_files, test_files = train_test_split(files, random_state=random_state, train_size=train_ratio)
    return train_files, test_files

def organize_folders(source_folder, train_ratio=0.7):
    for class_folder in ["b", "o"]:
        class_path = os.path.join(source_folder, class_folder)
        train_folder = os.path.join(source_folder, "train", class_folder)
        test_folder = os.path.join(source_folder, "test", class_folder)

        # Clear existing train and test folders
        if os.path.exists(train_folder):
            shutil.rmtree(train_folder)
        os.makedirs(train_folder)

        if os.path.exists(test_folder):
            shutil.rmtree(test_folder)
        os.makedirs(test_folder)

        for subdir, _, files in os.walk(class_path):
            if files:
                train_files, test_files = stratified_split(files, train_ratio)

                for file in train_files:
                    source_path = os.path.join(subdir, file)
                    destination_path = os.path.join(train_folder, os.path.basename(subdir), file)
                    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                    shutil.copy(source_path, destination_path)
                    print(f"Copied '{file}' from '{class_folder}' to 'train/{class_folder}/{os.path.basename(subdir)}'")

                for file in test_files:
                    source_path = os.path.join(subdir, file)
                    destination_path = os.path.join(test_folder, os.path.basename(subdir), file)
                    os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                    shutil.copy(source_path, destination_path)
                    print(f"Copied '{file}' from '{class_folder}' to 'test/{class_folder}/{os.path.basename(subdir)}'")

if __name__ == "__main__":
    source_folder = "code/data_analysis/dataset/dataset_mini"  # Update with the actual path to your source folder
    train_ratio = 0.7  # Change this to adjust the training ratio

    organize_folders(source_folder, train_ratio)
