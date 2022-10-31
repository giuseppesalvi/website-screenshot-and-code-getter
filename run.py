from genericpath import isfile
from htmldom import htmldom
import os
from html.parser import HTMLParser
from collections import defaultdict
from pprint import pprint
import argparse

def get_screenshot(website, domain):
    print("Generating the screenshot ...")
    output_option = " --filename='results/" + domain + "'"
    os.system("pageres " + website + output_option)
    
def get_code(website, domain):
    print("\nGenerating the code ...")

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


def get_log(domain):
    print("\nCounting the number of nodes ...")
    filename = "results/" + domain

    with open(filename + ".html", "r") as f:
        html = f.read()
        parser = MyHTMLParser()
        parser.feed(html)

    n_nodes = sum(parser.count.values())
    n_elements = (len(parser.count))

    print("\nNumber of nodes: ", n_nodes, "\n\n")

    # Save info in the log file
    with open(filename + ".log", "w") as f:
        print("Number of nodes: ", n_nodes, file=f)
        print("Number of different elements: ", n_elements , file=f)
        print("Divided per element: ", file=f)
        pprint(parser.count, f)

    # Save number of nodes for the given website in the summary file
    with open("results/nodes.log", "a") as f:
        print(domain + " " + str(n_nodes), file=f)


if __name__ == "__main__":
    website_list = []

    parser = argparse.ArgumentParser(description="get screenshot and code for a website", usage="python3 run.py [--website {website_url} | --website_list {file_path}]")
    parser.add_argument("--website", help="website url")
    parser.add_argument("--website_list", help="file path with list of website urls")
    parser.add_argument("--just_new", action='store_true',  help="process only the websites not already present")

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
        domain = website.split("//www.")[-1].split("/")[0]
        print("[%d/%d] %s" %(i + 1, len(website_list), domain))

        if args.just_new and isfile("results/" + domain + ".html"):
            print("Already present\n")
            continue

        get_screenshot(website, domain)
        get_code(website, domain)
        get_log(domain)
       

