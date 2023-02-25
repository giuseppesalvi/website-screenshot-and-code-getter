from html_parser import MyHTMLParser
from pprint import pprint
import re
from PIL import Image
import requests
from css_parser import parse_css
import json
from genericpath import isfile
import os
from statistics import mean

def print_stats(website_dict):

    # screenshot

    # Get screenshot dimensions
    img = Image.open(website_dict["filename"]+ ".png")
    height = img.height
    width = img.width
    website_dict["screenshot_dimensions"] = [width, height] 


    # add to the dictionary the size of all the lists
    sizes = {}
    for key, value in website_dict.items():
        if isinstance(value, list):
            sizes[key] = sum_of_dict_sizes(value)
    website_dict["sizes"] = sizes

    # add to the dictionary the number of lines of the html and css file
    number_of_lines = {}
    if isfile(website_dict["filename"] + ".css"):
        with open(website_dict["filename"] + ".css", "r") as file:
            number_of_lines[website_dict["filename"] + ".css"] = len(file.readlines())
    if isfile(website_dict["filename"] + "_raw.css"):
        with open(website_dict["filename"] + "_raw.css", "r") as file:
            number_of_lines[website_dict["filename"] + "_raw.css"] = len(file.readlines())
    if isfile(website_dict["filename"] + ".html"):
        with open(website_dict["filename"] + ".html", "r") as file:
            number_of_lines[website_dict["filename"] + ".html"] = len(file.readlines())
    if isfile(website_dict["filename"] + "_raw" + ".html"):
        with open(website_dict["filename"] + "_raw"+ ".html", "r") as file:
            number_of_lines[website_dict["filename"] + "_raw"+ ".html"] = len(file.readlines())
    website_dict["number_of_lines"] = number_of_lines 


    # Write stats in json file
    with open(website_dict["filename"]+ website_dict["suffix"] + ".json", "w") as f:
        json.dump(website_dict, f, sort_keys=True, indent=2)

    return


def sum_of_dict_sizes(lst):
    size = 0
    for element in lst:
        if isinstance(element, dict):
            size += len(element)
        else:
            return len(lst)
    return size


def stats_summary():
    summary = {}

    # Sizes
    summary["css_classes_raw"] = []
    summary["css_classes_skipped_raw"] = []
    summary["css_properties_raw"] = []
    summary["css_properties_skipped_raw"] = []
    summary["css_classes"] = []
    summary["css_classes_skipped"] = []
    summary["css_properties"] = []
    summary["css_properties_skipped"] = []
    summary["css_urls"] = []
    summary["css_urls_raw"] = []
    summary["html_classes"] = []
    summary["html_classes_raw"] = []
    summary["html_tags"] = []
    summary["html_tags_raw"] = []

    # Number of html nodes
    summary["n_html_nodes"] = [] 
    summary["n_html_nodes_raw"] = []

    # Number of lines
    summary["n_html_lines"] = []
    summary["n_html_lines_raw"] = []
    summary["n_css_lines"] = [] 

    # Screenshot photo dimensions
    summary["screenshot_width"] = []
    summary["screenshot_height"] = []

    for filename in os.listdir("results/"):
        if filename.endswith(".json"):
            with open("results/" + filename) as f:
                content = json.load(f)

                # Sizes
                summary["css_classes"].append(content["sizes"]["css_classes"])
                summary["css_classes_skipped"].append(content["sizes"]["css_classes_skipped"])
                summary["css_properties"].append(content["sizes"]["css_properties"])
                summary["css_properties_skipped"].append(content["sizes"]["css_properties_skipped"])
                summary["css_classes_raw"].append(content["sizes"]["css_classes_raw"])
                summary["css_classes_skipped_raw"].append(content["sizes"]["css_classes_skipped_raw"])
                summary["css_properties_raw"].append(content["sizes"]["css_properties_raw"])
                summary["css_properties_skipped_raw"].append(content["sizes"]["css_properties_skipped_raw"])
                summary["css_urls"].append(content["sizes"]["css_urls"])
                summary["css_urls_raw"].append(content["sizes"]["css_urls_raw"])
                summary["html_classes"].append(content["sizes"]["html_classes"])
                summary["html_classes_raw"].append(content["sizes"]["html_classes_raw"])
                summary["html_tags"].append(content["sizes"]["html_tags"])
                summary["html_tags_raw"].append(content["sizes"]["html_tags_raw"])

                # Number of html nodes
                summary["n_html_nodes"].append(content["n_html_nodes"])
                summary["n_html_nodes_raw"].append(content["n_html_nodes_raw"])

                # Number of lines
                for key, value in content["number_of_lines"].items():
                    if key.endswith("raw.html"):
                        summary["n_lines_html_raw"].append(value)
                    elif key.endswith(".html"):
                        summary["n_lines_html"].append(value)
                    elif key.endswith("raw.css"):
                        summary["n_lines_css_raw"].append(value)
                    elif key.endswith(".css"):
                        summary["n_lines_css"].append(value)
                

                # Screenshot photo dimensions
                summary["screenshot_width"].append(content["screenshot_dimensions"][0])
                summary["screenshot_height"].append(content["screenshot_dimensions"][1])

    # Sort Lists
    # Sizes
    summary["css_classes"].sort()
    summary["css_classes_skipped"].sort()
    summary["css_properties"].sort()
    summary["css_properties_skipped"].sort()
    summary["css_classes_raw"].sort()
    summary["css_classes_skipped_raw"].sort()
    summary["css_properties_raw"].sort()
    summary["css_properties_skipped_raw"].sort()
    summary["css_urls"].sort()
    summary["css_urls_raw"].sort()
    summary["html_classes"].sort()
    summary["html_classes_raw"].sort()
    summary["html_tags"].sort()
    summary["html_tags_raw"].sort()

    # Number of html nodes
    summary["n_html_nodes"].sort()
    summary["n_html_nodes_raw"].sort()

    # Number of lines
    summary["n_html_lines"].sort()
    summary["n_html_lines_raw"].sort()
    summary["n_css_lines"].sort()

    # Screenshot photo dimensions
    summary["screenshot_width"].sort()
    summary["screenshot_height"].sort()


    # Sizes
    # Do averages
    summary["avg_css_classes"] = mean(summary["css_classes"])
    summary["avg_css_classes_skipped"] = mean(summary["css_classes_skipped"])
    summary["avg_css_properties"] = mean(summary["css_properties"])
    summary["avg_css_properties_skipped"] = mean(summary["css_properties_skipped"])
    summary["avg_css_classes_raw"] = mean(summary["css_classes_raw"])
    summary["avg_css_classes_skipped_raw"] = mean(summary["css_classes_skipped_raw"])
    summary["avg_css_properties_raw"] = mean(summary["css_properties_raw"])
    summary["avg_css_properties_skipped_raw"] = mean(summary["css_properties_skipped_raw"])
    summary["avg_css_urls"] = mean(summary["css_urls"])
    summary["avg_css_urls_raw"] = mean(summary["css_urls_raw"])
    summary["avg_html_classes"] = mean(summary["html_classes"])
    summary["avg_html_classes_raw"] = mean(summary["html_classes_raw"])
    summary["avg_html_tags"] = mean(summary["html_tags"])
    summary["avg_html_tags_raw"] = mean(summary["html_tags_raw"])

    # Number of html nodes
    summary["avg_n_html_nodes"] = mean(summary["n_html_nodes"])
    summary["avg_n_html_nodes_raw"] = mean(summary["n_html_nodes_raw"])

    # Number of lines
    summary["avg_n_lines_html"] = mean(summary["n_lines_html"])
    summary["avg_n_lines_html_raw"] = mean(summary["n_lines_raw_html"])
    summary["avg_n_lines_css"] = mean(summary["n_lines_css"])
    summary["avg_n_lines_css_raw"] = mean(summary["n_lines_css_raw"])

    summary["n_websites"] = len(summary["n_html_nodes"])

    # Write summary in json file
    with open("summary.json", "w") as f:
        json.dump(summary, f, sort_keys=True, indent=2)
    return

if __name__ == "__main__":
    stats_summary()