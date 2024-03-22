import extension_converter as ec
import data_analysis_hierarchy as dah
import grayscale_converter as gc
import normalization_converter as nc
import clahe_converter as cc
import data_analysis_resize_all_keep_ratio as darakr

def initiate_operation_data_clean(input_folder, target_width, target_height):
    print("Initiating data clean operation")

    print("Converting images to png")
    ec.convert_images_to_png(input_folder)
    print("Images converted to png")

    """
    Not necessary at the moment, has already been done
    print("Resizing images to 0.25 of the original size")
    dah.process_images_in_folder(input_folder)
    print("Images resized")
    """

    print("Converting images to grayscale")
    gc.convert_images_to_grayscale(input_folder)
    print("Images converted to grayscale")

    print("Normalizing images")
    nc.normalize_all_images_in_folder(input_folder)
    print("Images normalized")

    print("Applying CLAHE to images")
    cc.convert_images_to_clahe(input_folder)
    print("CLAHE applied to images")

    """
    print("Resizing images while keeping ratio")
    darakr.resize_keep_ratio_images_in_folder(input_folder, target_width, target_height)
    print("Images resized while keeping ratio")

    print("Data clean operation completed")
    """


if __name__ == "__main__":
    # The folder in which the dataset is located
    input_folder = 'your_folder_here'

    # The target width and height you want the cleaned images to end up as
    target_width = 640
    target_height = 640

    initiate_operation_data_clean(input_folder, target_width, target_height)
