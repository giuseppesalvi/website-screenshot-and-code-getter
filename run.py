from genericpath import isfile
from htmldom import htmldom
import os
from html.parser import HTMLParser
from collections import defaultdict
from pprint import pprint
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def get_screenshot(website, domain):
    # Set webdriver options
    options = webdriver.ChromeOptions()
    options.headless = True
    # Set window size
    options.add_argument("--window-size=1280,1024")

    # Start web browser
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    # Launch URL
    driver.get(website)

    # Get window size
    s = driver.get_window_size()
    # Obtain browser height and width
    w = driver.execute_script('return document.body.parentNode.scrollWidth')
    h = driver.execute_script('return document.body.parentNode.scrollHeight')
    # Set to new window size
    driver.set_window_size(w, h)
    # Obtain screenshot of page within body tag
    driver.find_element(By.TAG_NAME, "body").screenshot(
        "results/" + domain + ".png")
    driver.set_window_size(s['width'], s['height'])

    # Close web driver
    driver.close()


def get_code(website, domain):
    print("\nGenerating the code ...")

    # Start web driver 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Launch URL 
    driver.get(website)

    # Get source code
    html = driver.page_source

    # Write html source code to file
    with open("results/" + domain + ".html", "w") as f:
        f.write(html)

    # Close web driver 
    driver.close()


class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.count = defaultdict(int)
        super().__init__()

    def handle_starttag(self, tag, attrs):
        self.count[tag] += 1

    def handle_startendtag(self, tag, attrs):
        self.count[tag] += 1


def get_log(domain):
    print("\nCounting the number of nodes ...")
    filename = "results/" + domain

    with open(filename + ".html", "r") as f:
        # Read html code and pass it to parser
        html = f.read()
        parser = MyHTMLParser()
        parser.feed(html)

    # Extract some statistics
    n_nodes = sum(parser.count.values())
    n_elements = (len(parser.count))

    print("\nNumber of nodes: ", n_nodes, "\n\n")

    # Save info in the log file
    with open(filename + ".log", "w") as f:
        print("Number of nodes: ", n_nodes, file=f)
        print("Number of different elements: ", n_elements, file=f)
        print("Divided per element: ", file=f)
        pprint(parser.count, f)

    # Save number of nodes for the given website in the summary file
    with open("results/nodes.log", "a") as f:
        print(domain + " " + str(n_nodes), file=f)


def sort_websites_by_nodes(filepath):
    websites = []
    # Read list of websites and nodes from file
    with open(filepath, "r") as f:
        for line in f:
            websites.append(
                (line.strip().split(" ")[0], int(line.strip().split(" ")[1])))

    # Write the list of websites and nodes sorted by number of nodes
    websites.sort(key=lambda tup: tup[1])
    with open(filepath, "w") as f:
        for website in websites:
            f.write(website[0] + " " + str(website[1]) + "\n")


if __name__ == "__main__":
    website_list = []

    parser = argparse.ArgumentParser(description="get screenshot and code for a website",
                                     usage="python3 run.py [--website {website_url} | --website_list {file_path}]")
    parser.add_argument("--website", help="website url")
    parser.add_argument(
        "--website_list", help="file path with list of website urls")
    parser.add_argument("--just_new", action='store_true',
                        help="process only the websites not already present")
    parser.add_argument("--task", help="task of the script: get screenshot, get code or both, sort statistics",
                        default="all", choices=["all", "screenshot", "code", "stats"])

    args = parser.parse_args()
    if args.website:
        website_list.append(args.website)
    elif args.website_list:
        with open(args.website_list, "r") as f:
            for line in f:
                website_list.append(line.strip())
    else:
        parser.print_usage()

    for i, website in enumerate(website_list):
        if website.startswith(" ") or website.startswith("#"):
            continue
        if "//www." in website:
            domain = website.split("//www.")[-1].split("/")[0]
        else:
            domain = website.split("//")[-1].split("/")[0]
        print("[%d/%d] %s" % (i + 1, len(website_list), domain))

        if args.just_new and isfile("results/" + domain + ".html"):
            print("Already present\n")
            continue

        if args.task in ["all", "screenshot"]:
            get_screenshot(website, domain)
        if args.task in ["all", "code"]:
            get_code(website, domain)
            get_log(domain)
        if args.task in ["all", "stats"]:
            sort_websites_by_nodes("results/nodes.log")
