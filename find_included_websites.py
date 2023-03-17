import argparse
import os
import json

def find_included_excluded(results_folder):
    # List of excluded websites
    excluded = []

    # List of included websites
    included = []
    for filename in os.listdir("experiments/" + results_folder + "/"):
        if filename.endswith(".json"):
            with open("experiments/" + results_folder + "/" + filename) as f:
                content = json.load(f)

                # If website is excluded, add it to the excluded list and skip it
                if content["excluded"] or len(content["css_classes"]) == 0:
                    excluded.append(content["domain"])
                else:
                    included.append(content["domain"])

     # Write list of included websites
    with open("experiments/included_" + results_folder + ".txt", "w") as f:
        for website in included:
            print(website, file=f)

    # Write list of excluded websites
    with open("experiments/excluded_" + results_folder + ".txt", "w") as f:
        for website in excluded:
            print(website, file=f)
    return

if __name__ == "__main__":
    results_folder = "results_websites_majestic_million2"

    # Initialize args parser
    parser = argparse.ArgumentParser(description="find included and excluded websites", usage="python3 find_included_websites.py --results_folder {results_folder}")
    parser.add_argument("--results_folder", help="folder with websites json files")

    # Read args
    args = parser.parse_args()
    if args.results_folder:
        results_folder= args.results_folder
        
    find_included_excluded(results_folder)