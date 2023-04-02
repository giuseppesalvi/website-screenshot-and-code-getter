import argparse
import os
import json
from os import path
from os import makedirs
import shutil
from genericpath import isfile
COPY = True
COMMON_FOLDER = True

def move_good_results(results_folder):
    source_folder = "experiments/" + results_folder
    destination_folder = "experiments/" + results_folder + "_good" if not COMMON_FOLDER else "experiments/" + "results_good"
    if not path.exists(destination_folder):
            makedirs(destination_folder)

    with open("experiments/good_images_" + results_folder + ".txt", "r") as f:
        for filename in f:
            filename_ = filename.rstrip()
            if isfile(source_folder + "/" + filename_ + ".png"):
                shutil.move(source_folder + "/" + filename_ + ".png", destination_folder + "/" + filename_ + ".png")
            if isfile(source_folder + "/" + filename_ + ".json"):
                shutil.move(source_folder + "/" + filename_ + ".json", destination_folder + "/"+ filename_ + ".json")
            if isfile(source_folder + "/" + filename_ + "_raw.css"):
                shutil.move(source_folder + "/" + filename_ + "_raw.css", destination_folder + "/"+ filename_ + "_raw.css")
            if isfile(source_folder + "/" + filename_ + "_raw.html"):
                shutil.move(source_folder + "/" + filename_ + "_raw.html", destination_folder + "/"+ filename_ + "_raw.html")
            if isfile(source_folder + "/" + filename_ + ".css"):
                shutil.move(source_folder + "/" + filename_ + ".css", destination_folder + "/"+ filename_ + ".css")
            if isfile(source_folder + "/" + filename_ + ".html"):
                shutil.move(source_folder + "/" + filename_ + ".html", destination_folder + "/"+ filename_ + ".html")
    return

if __name__ == "__main__":
    results_folder = "results_websites_majestic_million2"

    # Initialize args parser
    parser = argparse.ArgumentParser(description="move good results", usage="python3 move_good_results.py --results_folder {results_folder}")
    parser.add_argument("--results_folder", help="folder with websites json files")

    # Read args
    args = parser.parse_args()
    if args.results_folder:
        results_folder= args.results_folder
        
    move_good_results(results_folder)