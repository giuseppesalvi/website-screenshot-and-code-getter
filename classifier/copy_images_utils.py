import os
import shutil

if __name__ == "__main__":
    # Input and output folders
    input_folder = "../results_websites_majestic_million_blog"
    output_folder = "original_images/good_images"

    # Get a list of all image files in the input folder
    list_images_to_copy = []
    with open("list_good_images.txt", "r") as f:
        for domain in f.readlines():
            file_name = domain.rstrip("\n")+ ".png"
            source_file = os.path.join(input_folder, file_name)
            destination_file = os.path.join(output_folder, file_name)
            shutil.copyfile(source_file, destination_file)
