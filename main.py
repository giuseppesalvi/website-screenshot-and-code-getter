from genericpath import isfile
from html.parser import HTMLParser
from collections import defaultdict
from pprint import pprint
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
import re
import requests
import tinycss2
import sys
from types import SimpleNamespace

WAIT_SCREENSHOT = 1
CSS_INDENTATION = "    "


def accept_cookies(driver):
    """ Click to dismiss Cookies popup """

    list_strings = ["I Accept", "Accept",
                    "Accetta", "Ok", "Agree", "Accept All", "Accept Cookies", "Accept All Cookies", "No", "No, Thanks"]
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


def get_screenshot(website, file_local, test_name):
    """ Get Screenshot of website URL passed as argument, and save it """

    filename = "results/" + \
        website2domain(website) if not test_name else "results/" + \
        website2domain(website) + "_" + test_name

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
        driver.get("file://" + path.abspath(filename + ".html"))
    else:
        driver.get(website)

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
    driver.find_element(By.TAG_NAME, "body").screenshot(filename + ".png")

    # Close web driver
    driver.close()
    print("Screenshot obtained!\n")


def get_code(website):
    """ Get HTML code of Website URL passed as argument, and save it """

    print("\nGenerating the code ...")

    # Start web driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Launch URL
    driver.get(website)

    # Get source code
    html = driver.page_source

    # Write html source code to file
    with open("results/" + website2domain(website) + ".html", "w") as f:
        f.write(html)

    # Close web driver
    driver.close()
    print("Code obtained!\n")


class MyHTMLParser(HTMLParser):
    """ Parse HTML code to compute statistics """

    def __init__(self):
        self.tags = defaultdict(int)
        self.attributes = defaultdict(list)
        super().__init__()

    def handle_starttag(self, tag, attrs):
        """ Used to handle start tags such as <div ... >"""
        self.handle_tag(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        """ Used to handle self closing tags such as <img ... />, similar to handle_starttag"""
        self.handle_tag(tag, attrs)

    def handle_tag(self, tag, attrs):
        """ Used as common implementation for both start tags and self closing start tag"""
        self.tags[tag] += 1
        for attr in attrs:
            attr_name = attr[0]
            if attr_name not in ["title", "alt"]:
                attr_values = attr[1].split(" ")
            else:
                attr_values = [attr[1]]
            for v in attr_values:
                cleaned_v = re.sub("\n", "", re.sub(" +", " ", v))
                if cleaned_v and cleaned_v not in self.attributes[attr_name]:
                    self.attributes[attr_name].append(cleaned_v)


def get_log_and_css(domain, test_name):
    """ Save logging info for website, download related css file(s)"""

    print("\nCounting the number of nodes and attributes ...")
    suffix = "_" + test_name if test_name else ""
    filename = "results/" + domain

    with open(filename + suffix + ".html", "r") as f:
        # Read html code and pass it to parser
        html = f.read()
        parser = MyHTMLParser()
        parser.feed(html)

    # Extract some statistics
    n_nodes = sum(parser.tags.values())
    n_different_tags = (len(parser.tags))
    n_different_attributes = (len(parser.attributes))
    different_classes = parser.attributes["class"]
    css_urls = filter(lambda url: url.endswith(".css"), parser.attributes["href"])

    # Get image dimensions
    img = Image.open(filename + ".png")
    height = img.height
    width = img.width

    # Save info in the log file
    with open(filename + suffix + ".log", "w") as f:
        print("Number of nodes: ", n_nodes, file=f)
        print("Number of different tags: ", n_different_tags, file=f)
        print("Divided per element: ", file=f)
        pprint(parser.tags, f)
        print("Number of different attributes: ",
              n_different_attributes, file=f)
        print("Number of different classes: ", len(different_classes), file=f)
        print("Attributes: ", file=f)
        pprint(parser.attributes, f)

        print("Image dimensions: %dx%d" % (width, height), file=f)

    # Print on stdout
    print("\nNumber of nodes: ", n_nodes, "\n")
    print("Image dimensions: %dx%d" % (width, height))

    # Save number of nodes for the given website in the summary file
    with open("results/summary/nodes.log", "a") as f:
        print(domain + suffix + " " + str(n_nodes), file=f)

    # Save image dimension for the given website in the summary file
    with open("results/summary/images_sizes.log", "a") as f:
        print("%s %dx%d %f" %
              (domain, width, height, float(width)/height), file=f)

    # Download CSS files
    for i, url in enumerate(css_urls):
        with open(filename + suffix + "_" + str(i) + ".css", "w") as f:
            response = requests.get(url)
            #f.write(response.content)

            css_classes = {}
            css_properties = {}


            # Parse the stylesheet
            rules, encoding = tinycss2.parse_stylesheet_bytes(response.content, skip_comments=True, skip_whitespace=True)

            for rule in rules:  
                #tinycss2.parse_declaration_list(rule.content)
                type = rule.type # ex: "qualified-rule"

                # qualified-rule: <prelude> '{' <content> '}'
                # at-rule:        @<at-keyword> <prelude> '{' <content> '}'
                #                 @<at-rule> <prelude> ';'

                if type == "qualified-rule":
                    process_qualified_rule(rule, file=f)
                elif type=="at-rule":
                    process_at_rule(rule, file=f)
                    pass
                else:
                    print(type, file=f) 
                    break
               


            # css_parser = tinycss2.parse_stylesheet('page3')
            # rules = tinycss2.parse_stylesheet_bytes(response.content)
            # for rule in rules:
                # tmp = ""
                # last_token = None
                # empty = False # True 

                # if rule.at_keyword:
                    # at_rule = tinycss2.css21.parse_at_rule(rule)
                # else:
                    # for token in rule.selector:
                        # if not token.is_container:
                            # if token._as_css in css_classes:
                                # css_classes[token._as_css] += 1
                            # else:
                                # css_classes[token._as_css] = 1
                            # #if token._as_css == "body":
                            # #    print("here")
                            # print(token._as_css, end="", file=f)
                        # else:
                            # print(token._css_start, end="", file=f)
                            # for c in token.content:
                                # print(c._as_css, end="", file=f)
                            # print(token._css_end, end="", file=f)
                    # if token.as_css in ["{","}"]:
                        # print("", file=f)


                    # # TODO: add this to remove rules not in the list
    # #                for token in rule.selector:
                        # #if not token.is_container:
                            # ## print(token._as_css, end="", file=f)
                            # #if token._as_css in [" ", ",", "{"]:
                                # ##if last_token in different_classes:
                                # #if True:
                                    # #if not empty:
                                        # #tmp = ", " + tmp
                                    # #print(tmp, end=" ", file=f)
                                    # #empty = False
                                # #tmp = ""
                                # #last_token = None
                            # #else:
                                # #last_token = token._as_css
                                # #tmp += last_token 
                        # #else:
                            # ##print(token._css_start, end="", file=f)
                            # ##for c in token.content:
                            # ##    print(c._as_css, end="", file=f)
                            # ##print(token._css_end, end="", file=f)
                            # #tmp += token._css_start
                            # #for c in token.content:
                                # #tmp += c._as_css
                            # #tmp += token._css_end


                    # if not empty:
                        # print("{", file=f)
                        # for declaration in rule.declarations:
                            # print("\t", declaration.name, end=": ", file=f)

                            # if declaration.name in css_properties:
                                # css_properties[declaration.name] += 1
                            # else:
                                # css_properties[declaration.name] = 1

                            # for token in declaration.value:
                                # if token.type != "FUNCTION":
                                    # print(token._as_css, end="", file=f)
                                # else:
                                    # print(token._css_start, end="", file=f)
                                    # for c in token.content:
                                        # if c.type != "FUNCTION":
                                            # print(c._as_css, end="", file=f)
                                        # else:
                                            # print(c._css_start, end="", file=f)
                                            # for d in c.content:
                                                # print(d._as_css, end="", file=f)
                                            # print(c._css_end, end="", file=f)
                                    # print(token._css_end, end="", file=f)
                            # if declaration.priority:
                                # if declaration.priority == "important":
                                    # print("!important", end="", file=f)
                                # else:
                                    # print(declaration, end="", file=f)


                            # print(";", file=f)
                        # print("}\n", file=f)


        # Print number of css classes TODO write in log file
        print("\nCSS classes: ")
        pprint(dict(sorted(css_classes.items(), reverse=True, key=lambda item: item[1])), sort_dicts=False)
        
    
        # Print number of css propertiers TODO write in log file
        print("\nCSS properties: ")
        pprint(dict(sorted(css_properties.items(), reverse=True, key=lambda item: item[1])), sort_dicts=False)
        
def process_prelude(prelude, indentation="", file=sys.stdout):
    # Print prelude
    buffer = ""  # Keep ident and whitespace to see if the next literal must be kept
    print(indentation, end="", file=file)
    for token in prelude:
        printable = token.serialize() 
        if token.type == "ident":
            buffer += printable 

            ## Check if ident is in the list of classes
        else:
            #buffer += output
            if printable == "," :
                print(buffer + printable, end=" ", file=file)
                buffer = ""
            else:
                buffer += printable

    if buffer:  # if buffer is not empty
        print(buffer, end=" ", file=file)
        buffer = ""

def process_content(content, indentation="", file=sys.stdout):
    for idx, token in enumerate(content):
        printable = token.serialize()
        if idx == 0:
            if printable == " ":
                print("{\n" + CSS_INDENTATION + indentation, end="", file=file)
            else:
                print("{\n" + CSS_INDENTATION + indentation + printable, end="", file=file)

        elif idx == len(content) - 1:
            if token.serialize != ";":
                print(printable, end=";\n" + indentation + "}\n\n", file=file)
            else:
                print(printable, end="\n" + indentation + "}\n\n", file=file)

        elif token.serialize() == ";":
            print(printable, end="\n" + CSS_INDENTATION + indentation, file=file)
        elif token.serialize() == ":":
            print(printable, end=" ", file=file)
        else:
            print(printable, end="", file=file)


def process_qualified_rule(rule, indentation="", file=sys.stdout):
    prelude = rule.prelude
    content = rule.content

    process_prelude(prelude, indentation=indentation, file=file)
    if content:
        process_content(content, indentation=indentation, file=file)

def process_content_at_rule(content, indentation="", file=sys.stdout):
    qualified_rule_prelude = [] 
    for node in content:
        if node.type != "{} block":
            qualified_rule_prelude.append(node)
        else:
            if len(qualified_rule_prelude) == 0:
                #process_content_at_rule(node.content, indentation=CSS_INDENTATION+indentation, file=file)
                process_content_at_rule(node.content, indentation=indentation, file=file)
            else:
                #process_prelude(qualified_rule_prelude, indentation=CSS_INDENTATION+indentation, file=file)
                #process_content(node.content, indentation=CSS_INDENTATION+indentation, file=file)
                process_prelude(qualified_rule_prelude, indentation=indentation+CSS_INDENTATION, file=file)
                process_content(node.content, indentation=indentation+CSS_INDENTATION, file=file)
                qualified_rule_prelude = [] 
    

def process_at_rule(rule, indentation="", file=sys.stdout):
    prelude = rule.prelude 
    content = rule.content

    at_keyword = "@" + rule.at_keyword
    at_keyword.replace(" ", "")
    #if at_keyword == "@media" and  "min-width:1024" in "".join([tmp.serialize() for tmp in prelude]):
        #print("Here we are")
    print(indentation+at_keyword, end="", file=file)

    process_prelude(prelude, file=file)

    if content:
        print("{", file=file)

        # Check for nested at_rule
        if content[0].type == 'at-keyword':
            nested_rule = SimpleNamespace()
            nested_rule.at_keyword = content[0].value
            nested_rule.prelude = [content[1], content[2]]
            nested_rule.content = content[3:]
            process_at_rule(nested_rule, indentation=indentation+CSS_INDENTATION, file=file)
        else:
            process_content_at_rule(content, indentation=indentation, file=file)

        print(indentation+ "}\n", file=file)
    else:
        print(";", file=file)


def sanitize(domain, test_name):
    # Run command for sanitizing the code
    if not test_name:
        test_name = "sanitize"  # As default output will have sanitize suffix
    subprocess.run("node sanitize_html.js " + domain +
                   " " + test_name, shell=True, check=True)

    # Run command for cleaning the white spaces and formatting the html file
    subprocess.run("clean-html results/" + domain + "_" +
                   test_name + ".html --in-place", shell=True, check=True)
    return


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
    for i, website in enumerate(website_list):

        # For DBG: lines that start with space or # are discarded
        if website.startswith(" ") or website.startswith("#"):
            continue

        if args.task != "stats":
            print("[%d/%d] %s" %
                  (i + 1, len(website_list), website2domain(website)))

        # If just_new option, process only new websites
        if args.just_new and ((args.task in ["all", "code"] and isfile("results/" + website2domain(website) + ".html")) or args.task in ["stats", "log"] and isfile("results/" + website2domain(website) + ".log") or args.task == "screenshot" and isfile("results/" + website2domain(website) + ".png")):
            print("Already present\n")
            continue

        # Get code of the website
        if args.task in ["all", "code"]:
            get_code(website)

        # Sanitize Html code
        if args.task in ["all", "sanitize"]:
            sanitize(website2domain(website), test_name=args.test_name)

        # Get website screenshot
        if args.task in ["all", "screenshot"]:
            get_screenshot(website, file_local=args.file_local,
                           test_name=args.test_name)
            # DBG: Get both the non sanitized and the sanitized version screenshot
            get_screenshot(website, file_local=True,
                           test_name="sanitize")

        # Get code log and calculate statistics, save css files
        if args.task in ["all", "log"]:
            get_log_and_css(website2domain(website), args.test_name)


        # Sort and save statistics
        if args.task in ["all", "stats"]:
            sort_websites_by_nodes("results/summary/nodes.log")
            sort_websites_by_image_aspect_ratio(
                "results/summary/images_sizes.log")

        batch += 1
        if batch >= BATCH_SIZE:
            break
        print("\n")
