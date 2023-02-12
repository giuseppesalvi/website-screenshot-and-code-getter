from genericpath import isfile
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from PIL import Image
from utils import *
from os import path
import subprocess
import requests
from css_parser import parse_css
from html_parser import MyHTMLParser
import re
from pprint import pprint
from stats import print_stats

WAIT_SCREENSHOT = 1

def accept_cookies(driver):
    """ Click to dismiss Cookies popup """

    list_strings = ["I Accept", "Accept",
                    "Accetta", "Accetta tutti", "Ok", "Agree", "Accept All", "Accept Cookies", "Accept All Cookies", "No", "No, Thanks"]
    lowercase = [str.lower() for str in list_strings]
    uppercase = [str.upper() for str in list_strings]
    capitalized = [str.capitalize() for str in list_strings]

    for string in set(list_strings + lowercase + uppercase + capitalized):
        # Look for elements with text inside
        try:
            driver.find_element(
                By.XPATH, '//*[self::a|self::button|self::div|self.span][normalize-space()="' + string + '"]').click()
        except NoSuchElementException:
            pass
        except ElementNotInteractableException:
            pass
        except Exception as e:
            # Print and try to go on anyway
            print("Exception raised inside accept_cookies by", website_url)
            print(e, end="\n\n") 
            with open("errors.txt", "a") as f:
                print("Exception raised inside accept_cookies by", website_url, file=f)
                print(e, end="\n\n", file=f)


def get_screenshot(website_dict, file_local, suffix=""):
    """ Get Screenshot of website URL passed as argument, and save it """

    print("\nGenerating the screenshot ...")
    # Set webdriver options
    options = webdriver.ChromeOptions()
    options.headless = True
    # Set window size
    options.add_argument("--window-size=1280,1024")

    # Start web browser
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    # Launch URL
    if file_local:
        driver.get("file://" + path.abspath(website_dict["filename"] + website_dict["suffix"] + suffix + ".html"))
    else:
        driver.get(website_dict["website_url"])

    # Wait some time to allow popups to show
    driver.implicitly_wait(WAIT_SCREENSHOT)

    # Accept Cookies to hide popup
    accept_cookies(driver)

    # Get window size
    #s = driver.get_window_size()

    # Obtain browser height and width
    w = driver.execute_script('return document.body.parentNode.scrollWidth')
    h = driver.execute_script('return document.body.parentNode.scrollHeight')

    # Set to new window size
    driver.set_window_size(w, h)

    # Obtain screenshot of page within body tag
    driver.find_element(By.TAG_NAME, "body").screenshot(website_dict["filename"] + website_dict["suffix"] + suffix + ".png")

    # Close web driver
    driver.close()
    print("Screenshot obtained!\n")


#def get_code(website_dict):
    #""" Get HTML code of Website URL passed as argument, and save it """

    #parser = get_html(website_dict)

    #website_dict["html_tags"] = list(parser.tags.keys())
    #website_dict["html_classes"] = parser.attributes["class"]
    #website_dict["css_urls"] = list(filter(lambda url: bool(re.search(r"\.css(\?.*)?$", url)), parser.attributes["href"]))

    #get_css(website_dict)


def get_html(website_dict):
    print("\nGenerating HTML code ...")

    # Start web driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Launch URL
    driver.get(website_dict["website_url"])

    # Get source code
    html = driver.page_source

    # Write html source code to file
    with open(website_dict["filename"]+ website_dict["suffix"] + ".html", "w") as f:
        f.write(html)

    # Close web driver
    driver.close()
    print("HTML code obtained!\n")

    parser = MyHTMLParser()
    parser.feed(html)

    # Save website info in the dictionary
    website_dict["n_html_nodes"] = sum(parser.tags.values())
    website_dict["html_tags"] = list(parser.tags.keys())
    website_dict["html_classes"] = parser.attributes["class"]
    website_dict["css_urls"] = list(filter(lambda url: bool(re.search(r"\.css(\?.*)?$", url)), parser.attributes["href"]))

    return 

def get_css(website_dict):
    print("\nGenerating CSS code ...")
    # Download CSS files
    website_dict["css_classes"] = [] 
    website_dict["css_properties"] = [] 
    website_dict["css_classes_skipped"] = [] 
    website_dict["css_properties_skipped"] = [] 
    for i, url in enumerate(website_dict["css_urls"]):
        with open(filename + suffix + "_" + str(i) + ".css", "w") as f:
            try: 
                response = requests.get(url)
            except Exception as e:
                # internal url
                response = requests.get(website_dict["website_url"] + url)

            css_classes, css_properties, css_classes_skipped, css_properties_skipped = parse_css(response.content, website_dict["html_tags"], website_dict["html_classes"], file=f)
            website_dict["css_classes"].append(css_classes)
            website_dict["css_properties"].append(css_properties)
            website_dict["css_classes_skipped"].append(css_classes_skipped)
            website_dict["css_properties_skipped"].append(css_properties_skipped)
            

    print("CSS code obtained!\n")


def sanitize(domain, test_name):
    print("Sanitizing Html Code")

    # Run command for sanitizing the code
    if not test_name:
        test_name = "sanitize"  # As default output will have sanitize suffix
    #subprocess.run("node sanitize_html.js " + domain +
                   #" " + test_name, shell=True, check=True)
    result = subprocess.run(
        "node sanitize_html.js " + domain + " " + test_name,
        shell=True,
        check=True,
        stdout=subprocess.PIPE,
    )
    html = result.stdout.decode("utf-8")

    # Run command for cleaning the white spaces and formatting the html file
    subprocess.run("clean-html results/" + domain + "_" +
                   test_name + ".html --in-place", shell=True, check=True)


    # Update website info in the dictionary
    parser = MyHTMLParser()
    parser.feed(html)

    website_dict["n_html_nodes_before_sanitizing"] = website_dict["n_html_nodes"] 
    website_dict["html_tags_before_sanitizing"] = website_dict["html_tags"]
    website_dict["html_classes_before_sanitizing"] = website_dict["html_classes"] 
    website_dict["css_urls_before_sanitizing"] = website_dict["css_urls"]
    
    website_dict["n_html_nodes"] = sum(parser.tags.values())
    website_dict["html_tags"] = list(parser.tags.keys())
    website_dict["html_classes"] = parser.attributes["class"]
    website_dict["css_urls"] = list(filter(lambda url: bool(re.search(r"\.css(\?.*)?$", url)), parser.attributes["href"]))

    return

def replace_css_urls(website_dict):
    # Replace all css_urls inside html file with local css filenames
    with open(website_dict["filename"] + "_sanitize.html") as f:
        content = f.read()

    replace_dict = {url: website_dict["domain"] + "_" + str(index) + ".css" for index, url in enumerate(website_dict["css_urls"])}
    
    # Replace all the matches with their corresponding values
    for key, value in replace_dict.items():
        content = content.replace(key, value)


    with open(website_dict["filename"] + "_sanitize.html", 'w') as f:
        f.write(content)


def init_args_parser():
    """ Initialize args parser with arguments """

    parser = argparse.ArgumentParser(description="get screenshot and code for a website",
                                     usage="python3 run.py [--website {website_url} | --website_list {file_path}]")
    parser.add_argument("--website", help="website url")
    parser.add_argument(
        "--website_list", help="file path with list of website urls")
    parser.add_argument("--just_new", action='store_true',
                        help="process only the websites not already present")
    parser.add_argument("--task", help="task of the script: get screenshot, get code, sort statistics, get log",
                        default="all", choices=["all", "screenshot", "code", "stats", "log", "sanitize"])
    parser.add_argument(
        "--test_name", help="name of the test when running log task, will be used as output name concatenated with the website domain", default=None)
    parser.add_argument("--batch", type=int,
                        help="max number of websites processed", default=10)
    parser.add_argument(
        "--file_local", help="use the local html file for the screenshot instead of the url", default=False, type=bool)

    return parser


if __name__ == "__main__":
    website_list = []

    # Initialize args parser
    parser = init_args_parser()
    args = parser.parse_args()

    # Single website
    if args.website:
        website_list.append(args.website)

    # List of Websites
    elif args.website_list:
        with open(args.website_list, "r") as f:
            for line in f:
                website_list.append(line.strip())
    else:
        if args.task != "stats":
            parser.print_usage()
        else:
            website_list.append("")

    BATCH_SIZE = args.batch
    batch = 0

    # Process each website in the list
    for i, website_url in enumerate(website_list):

        try:
            domain = website2domain(website_url)
            filename = "results/" + domain
            suffix = "_" + args.test_name if args.test_name else ""

            website_dict = {}
            website_dict["website_url"] = website_url
            website_dict["domain"] = website2domain(website_url)
            website_dict["filename"] = filename
            website_dict["suffix"] = suffix


            # For DBG: lines that start with space or # are discarded
            if website_url.startswith(" ") or website_url.startswith("#"):
                continue

            if args.task != "stats":
                print("[%d/%d] %s" %(i + 1, len(website_list), domain))

            # If just_new option, process only new websites
            if args.just_new and ((args.task in ["all", "code"] and isfile(filename + ".html")) or args.task in ["stats", "log"] and isfile(filename + ".log") or args.task == "screenshot" and isfile(filename + ".png")):
                print("Already present\n")
                continue

            # Get code of the website
            if args.task in ["all", "code"]:
                get_html(website_dict)
                sanitize(website_dict["domain"], test_name=args.test_name)
                get_css(website_dict)
                replace_css_urls(website_dict)

            # Sanitize Html code
            if args.task in ["sanitize"]:
                sanitize(website_dict["domain"], test_name=args.test_name)

            # Get website screenshot
            if args.task in ["all", "screenshot"]:
                get_screenshot(website_dict, file_local=args.file_local)
                # DBG: Get both the non sanitized and the sanitized version screenshot
                # TODO: FIX THIS
                get_screenshot(website_dict, file_local=True, suffix="_sanitize")

            # Sort and save statistics
            if args.task in ["all", "stats"]:
                #pprint(website_dict)
                print_stats(website_dict)

            batch += 1
            if batch >= BATCH_SIZE:
                break
            print("\n")
        except Exception as e:
            print("Exception raised by", website_url)
            print(e, end="\n\n")
            with open("errors.txt", "a") as f:
                print("Exception raised by", website_url, file=f)
                print(e, end="\n\n", file=f)

