from htmldom import htmldom
import sys
import os
from html.parser import HTMLParser
from collections import defaultdict
from pprint import pprint
import argparse

def get_screenshot(website):
    print("Generating the screenshot for: " + website + " ...")
    os.system("pageres " + website)
    
def get_code(website):
    print("\nGenerating the code ...")
    domain = website.split("//www.")[-1].split("/")[0]

    dom = htmldom.HtmlDom(website)
    dom = dom.createDom()

    with open("results/" + domain + ".html", "w") as f:
        all = dom.find("*")
        for node in all:
    	    f.write(node.html())
	
class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.count = defaultdict(int)
        super().__init__()

    def handle_starttag(self, tag, attrs):
        self.count[tag] += 1

    def handle_startendtag(self, tag, attrs):
        self.count[tag] +=1


def get_log(website):
    print("\nCounting the number of nodes ...")
    domain = website.split("//www.")[-1].split("/")[0]
    filename = "results/" + domain + ".html"

    with open(filename, "r") as f:
        html = f.read()
        parser = MyHTMLParser()
        parser.feed(html)

    print("\nNumber of nodes: ", sum(parser.count.values()))

    with open(filename + "_log", "w") as f:
        print("Number of nodes: ", sum(parser.count.values()), file=f)
        print("Number of different elements: ", (len(parser.count)), file=f)
        print("Divided per element: ", file=f)
        pprint(parser.count, f)


if __name__ == "__main__":
    website_list = []

    parser = argparse.ArgumentParser(description="get screenshot and code for a website", usage="python3 run.py [--website {website_url} | --website_list {file_path}]")
    parser.add_argument("--website", help="website url")
    parser.add_argument("--website-list", help="file path with list of website urls")

    args = parser.parse_args()
    if args.website:
        website_list.append(args.website)
    elif args.website_list:
        with open(args.website_list, "r") as f:
            for website_url in f.readlines():
                website_list.append(website_url)
    else:
        parser.print_usage()


    for website in website_list:
        get_screenshot(website)
        get_code(website)
        get_log(website)
       

