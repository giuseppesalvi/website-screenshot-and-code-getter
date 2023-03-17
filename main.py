from genericpath import isfile
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from utils import *
from os import path
from os import makedirs
import subprocess
import requests
from css_parser import parse_css
from html_parser import MyHTMLParser
import re
from stats import print_stats
import asyncio
from pyppeteer import launch
import logging
import datetime


RESULTS_FOLDER = "experiments/results_websites/"
WAIT_SCREENSHOT = 1
COLAB = False 

def accept_cookies(driver, website_url):
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
            logging.warning("Exception raised inside accept_cookies by " + website_url)
            logging.warning(e) 
            with open("experiments/errors.txt", "a") as f:
                print("Exception raised inside accept_cookies by", website_url, file=f)
                print(e, end="\n\n", file=f)


def get_screenshot(website_dict, file_local, suffix=""):
    """ Get Screenshot of website URL passed as argument, and save it """

    print("\nGenerating the screenshot ...")
    logging.info("Generating the screenshot ...")
    # Set webdriver options
    options = webdriver.ChromeOptions()
    options.headless = True
    if COLAB:
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

    # Set window size
    options.add_argument("--window-size=1280,1024")

    # Start web browser
    if COLAB:
        driver = webdriver.Chrome('chromedriver', options=options)
    else:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Launch URL
    if file_local:
        driver.get("file://" + path.abspath(website_dict["filename"] + website_dict["suffix"] + suffix + ".html"))
    else:
        driver.get(website_dict["website_url"])

    # Wait some time to allow popups to show
    driver.implicitly_wait(WAIT_SCREENSHOT)

    # Accept Cookies to hide popup
    accept_cookies(driver, website_dict["website_url"])

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
    logging.info("Screenshot obtained!\n")


async def get_rendered_html(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle0'})
    rendered_html = await page.content()
    await browser.close()
    return rendered_html

def get_html_pyppeteer(url):
    html = asyncio.get_event_loop().run_until_complete(get_rendered_html(url))
    return html

def get_html_selenium(url):
    # Set webdriver options
    options = webdriver.ChromeOptions()
    options.headless = True
    if COLAB:
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

    # Set window size
    options.add_argument("--window-size=1280,1024")

    # Start web browser
    if COLAB:
        driver = webdriver.Chrome('chromedriver', options=options)
    else:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Launch URL
    driver.get
    driver.get(url)

    # Get source code
    html = driver.page_source
    # Try to address js
    html = driver.execute_script('return document.documentElement.outerHTML')

    # Close web driver
    driver.close()
    return html

def check_website_framework(html, website_dict):
    frameworks_found = []

    # Check for React-specific code
    #if re.search(r'data-reactroot|data-reactid|React\.createElement|ReactDOM\.render', html):
    if re.search(r'data-reactid=".*?"|React\.createElement|ReactDOM\.render', html):
        print("Framework found: React")
        logging.info("Framework found: React")
        frameworks_found.append('React')

    # Check for Gatsby-specific code
    if re.search(r'gatsby-', html) or re.search(r'___gatsby|GATSBY_.*_POST', html):
        print("Framework found: Gatsby")
        logging.info("Framework found: Gatsby")
        ("Framework found: Gatsby")
        frameworks_found.append('Gatsby')

    # Check for Next.js-specific code
    if re.search(r'_app\.js|_document\.js|_error\.js|_documentSetup|_appContent', html) or re.search(r'__NEXT_DATA__', html):
        print("Framework found: Next")
        logging.info("Framework found: Next")
        frameworks_found.append('Next.js')

    # Check for Nuxt-specific code
    if re.search(r'nuxt-', html) or re.search(r'__NUXT__|fetch__|nuxt\.js', html):
        print("Framework found: Nuxt")
        logging.info("Framework found: Nuxt")
        frameworks_found.append('Nuxt')

    # Check for Backbone-specific code
    if re.search(r'backbone-', html) or re.search(r'backbone(\.min)?\.js', html):
        print("Framework found: Backbone")
        logging.info("Framework found: Backbone")
        frameworks_found.append('Backbone')

    # From experiments: Angular, Vue and Ember don't create problems
    # Check for Vue-specific code
    if re.search(r'vue-', html) or re.search(r'Vue(\.min)?\.js', html):
        print("Framework found: Vue")
        logging.info("Framework found: Vue")
        frameworks_found.append('Vue')

    # Check for Angular-specific code
    if re.search(r'ng-', html) and re.search(r'angular(\.min)?\.js', html):
        print("Framework found: Angular")
        logging.info("Framework found: Angular")
        frameworks_found.append('Angular')

    # Check for Ember-specific code
    if re.search(r'ember-', html) or re.search(r'ember(\.min)?\.js', html):
        print("Framework found: Ember")
        logging.info("Framework found: Ember")
        frameworks_found.append('Ember')


    # Check for Rocket Lazy Load script
    #if re.search(r'rocketLazyLoadScript|rocketlazyloadscript|', html):
        #print("Framework found: Rocket Lazy Load (WordPress)")
        #frameworks_found.append('Rocket Lazy Load')

    # Check for WordPress scripts that impact appearance/functionality when JS is disabled
    #if re.search(r'wp-block-[^"]*?"|wp-embed|has-js|no-js|js-focus-visible|wp-menu-arrow', html):
        #print("Framework found: WordPress")
        #frameworks_found.append('WordPress')

    if any(item in frameworks_found for item in ["React", "Gatsby", "Next", "Nuxt", "Backbone"]):
        website_dict["framework_problematic"] = True
        website_dict["excluded"] = True 
    else:
        website_dict["framework_problematic"] = False
    website_dict["frameworks_list"] = frameworks_found
    return


def get_html(website_dict):
    print("\nGenerating HTML code ...")
    logging.info("Generating HTML code ...")

    url = website_dict["website_url"]

    #html = get_html_pyppeteer(url)
    html = get_html_selenium(url)

    # Check for web frameworks
    check_website_framework(html, website_dict)

    # Write html source code to file
    with open(website_dict["filename"]+ website_dict["suffix"] + "_raw.html", "w") as f:
        f.write(html)

    print("HTML code obtained!\n")
    logging.info("HTML code obtained!\n")

    parser = MyHTMLParser()
    parser.feed(html)

    # Save website info in the dictionary
    website_dict["n_html_nodes_raw"] = sum(parser.tags.values())
    website_dict["html_tags_raw"] = list(parser.tags.keys())
    website_dict["html_classes_raw"] = parser.attributes["class"]
    website_dict["css_urls_raw"] = list(filter(lambda url: bool(re.search(r"\.css(\?.*)?$", url)), parser.attributes["href"]))

    return 

def add_dictionary(to_dict, from_dict):
    """ Add values from one dictionary to another"""
    for key in from_dict.keys():
        if key not in to_dict:
            to_dict[key] = from_dict[key]
        else:
            to_dict[key] += from_dict[key]
    
def get_css(website_dict, sanitize=True):
    print("\nGenerating CSS code ...")
    logging.info("Generating CSS code ...")
    sanitize_suffix = "_raw" if not sanitize else ""
    website_dict["css_classes" + sanitize_suffix] = {} 
    website_dict["css_properties" + sanitize_suffix] = {} 
    website_dict["css_classes_skipped" + sanitize_suffix] = {}
    website_dict["css_properties_skipped" + sanitize_suffix] = {} 
    # Download CSS files
    if not website_dict["css_urls"]:
        print("no CSS files found!\n")
        website_dict["excluded"] = True

    for i, url in enumerate(website_dict["css_urls"]):
        with open(filename + suffix + (sanitize_suffix if not sanitize else "") + ".css", "a") as f:
            try: 
                response = requests.get(url)
            except Exception as e:
                # internal url
                response = requests.get(website_dict["website_url"] + url)

            css_classes, css_properties, css_classes_skipped, css_properties_skipped = parse_css(response.content, website_dict["html_tags"], website_dict["html_classes"], file=f, sanitize=sanitize)
            add_dictionary(website_dict["css_classes" + sanitize_suffix], css_classes)
            add_dictionary(website_dict["css_properties" + sanitize_suffix], css_properties)
            add_dictionary(website_dict["css_classes_skipped" + sanitize_suffix], css_classes_skipped)
            add_dictionary(website_dict["css_properties_skipped" + sanitize_suffix], css_properties_skipped)
            

    print("CSS code obtained!\n")


def sanitize(domain, test_name):
    print("Sanitizing Html Code")
    logging.info("Sanitizing Html Code")

    # Run command for sanitizing the code
    result = subprocess.run(
        "node sanitize_html.js " + domain + " " + RESULTS_FOLDER,
        shell=True,
        check=True,
        stdout=subprocess.PIPE,
    )
    html = result.stdout.decode("utf-8")

    # Run command for cleaning the white spaces and formatting the html file
    subprocess.run("clean-html " + RESULTS_FOLDER + "/" + domain + ".html --in-place", shell=True, check=True)


    # Update website info in the dictionary
    parser = MyHTMLParser()
    parser.feed(html)

    website_dict["n_html_nodes"] = sum(parser.tags.values())
    website_dict["html_tags"] = list(parser.tags.keys())
    website_dict["html_classes"] = parser.attributes["class"]
    website_dict["css_urls"] = list(filter(lambda url: bool(re.search(r"\.css(\?.*)?$", url)), parser.attributes["href"]))

    return

def replace_css_urls(website_dict):
    # Replace all css_urls inside html file with local css filename
    with open(website_dict["filename"] + ".html") as f:
        content = f.read()

    replace_dict = {url: website_dict["domain"] + ".css" for index, url in enumerate(website_dict["css_urls"])}
    
    # Replace all the matches with their corresponding values
    for key, value in replace_dict.items():
        content = content.replace(key, value)


    with open(website_dict["filename"] + ".html", 'w') as f:
        f.write(content)


def init_args_parser():
    """ Initialize args parser with arguments """

    parser = argparse.ArgumentParser(description="get screenshot and code for a website",
                                     usage="python3 main.py [--website {website_url} | --website_list {file_path}]")
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
    logging.basicConfig(filename='experiments/logs/websites.log', level=logging.INFO)

    # Log start date and time
    start = datetime.datetime.now()
    logging.info("Start date and time: {}".format(start.strftime("%Y-%m-%d %H:%M:%S")))


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

    # make results folder if not present
    if args.website_list:
        results_folder = "results/results_" + args.website_list.split(".txt")[0]
        if not path.exists(results_folder):
            makedirs(results_folder)
    else:
        results_folder = "results/results_websites"

    RESULTS_FOLDER = results_folder 

    BATCH_SIZE = args.batch
    batch = 0

    # Process each website in the list
    for i, website in enumerate(website_list):

        try:
            domain = website2domain(website)
            #try:
            website_url = get_website_url(domain) 
            #except Exception as e:  
                # Using default one
                #website_url = "https://www." + domain

                #print("Exception raised by ", website, " in get_website_url, using default url")
                #print(e, end="\n\n")
                #logging.warning("Exception raised by " + website +  " in get_website_url, using default url")
                #logging.exception(e)
            
            filename = results_folder + "/" + domain
            suffix = "_" + args.test_name if args.test_name else ""

            website_dict = {}
            website_dict["website_url"] = website_url
            website_dict["domain"] = domain 
            website_dict["filename"] = filename
            website_dict["suffix"] = suffix
            website_dict["excluded"] = False 


            # For DBG: lines that start with space or # are discarded
            if website.startswith(" ") or website.startswith("#"):
                continue

            if args.task != "stats":
                print("[%d/%d] %s" %(i + 1, len(website_list), domain))
                logging.info("[%d/%d] %s" %(i + 1, len(website_list), domain))

            # If just_new option, process only new websites
            if args.just_new and ((args.task in ["all", "code"] and (isfile(filename + "_raw.html") or isfile(filename + ".html"))) or args.task in ["stats", "log"] and isfile(filename + ".log") or args.task == "screenshot" and isfile(filename + ".png")):
                print("Already present\n")
                logging.info("Already present")
                continue

            # Get code of the website
            if args.task in ["all", "code"]:
                get_html(website_dict)
                sanitize(website_dict["domain"], test_name=args.test_name)
                get_css(website_dict)
                # DBG: Get both the non sanitized and the sanitized version css 
                get_css(website_dict, sanitize=False)
                replace_css_urls(website_dict)

            # Sanitize Html code
            if args.task in ["sanitize"]:
                sanitize(website_dict["domain"], test_name=args.test_name)

            # Get website screenshot
            if args.task in ["all", "screenshot"]:
                get_screenshot(website_dict, file_local=True)
                # DBG: Get both the non sanitized and the sanitized version screenshot
                # TODO: FIX THIS
                #get_screenshot(website_dict, file_local=args.file_local, suffix="_raw")

            # Sort and save statistics
            if args.task in ["all", "stats"]:
                #pprint(website_dict)
                print_stats(website_dict)

            batch += 1
            if batch >= BATCH_SIZE:
                break
            print("\n")
        except Exception as e:
            print("Exception raised by ", website)
            print(e, end="\n\n")
            logging.warning("Exception raised by " + website)
            logging.exception(e)
            with open("experiments/errors.txt", "a") as f:
                print("Exception raised by ", website, file=f)
                print(e, end="\n\n", file=f)
            with open("experiments/errors_" + RESULTS_FOLDER + ".txt", "a") as f:
                print(website, file=f)
            #break # DEBUG

    # Log end date and time elapsed time from start
    end = datetime.datetime.now()
    elapsed_time = (end - start).seconds
    logging.info("End date and time: {}, elapsed time  : {:02d}:{:02d}:{:02d}".format(end.strftime("%Y-%m-%d %H:%M:%S"), elapsed_time//3600, (elapsed_time%3600)//60, elapsed_time%60))
