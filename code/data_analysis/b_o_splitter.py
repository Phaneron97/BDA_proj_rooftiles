import os
import shutil

def organize_folders(source_folder):
    folder_b = os.path.join(source_folder, "b")
    folder_o = os.path.join(source_folder, "o")

    if not os.path.exists(folder_b):
        os.makedirs(folder_b)

    if not os.path.exists(folder_o):
        os.makedirs(folder_o)

    for root, dirs, files in os.walk(source_folder):
        for folder in dirs:
            if "_b_" in folder:
                source_path = os.path.join(root, folder)
                destination_path = os.path.join(folder_b, folder)
                shutil.move(source_path, destination_path)
                print(f"Moved '{folder}' to 'b'")
            elif "_o_" in folder:
                source_path = os.path.join(root, folder)
                destination_path = os.path.join(folder_o, folder)
                shutil.move(source_path, destination_path)
                print(f"Moved '{folder}' to 'o'")

if __name__ == "__main__":
    source_folder = "code/data_analysis/dataset/dataset_mini"  # Update with the actual path to your source folder

    organize_folders(source_folder)
