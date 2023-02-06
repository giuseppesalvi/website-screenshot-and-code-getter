from html_parser import MyHTMLParser
from pprint import pprint
import re
from PIL import Image
import requests
from css_parser import parse_css

def get_statistics(domain, test_name):
    """ Save statistics for the website"""

    print("\nCounting the number of nodes and attributes ...")
    suffix = "_" + test_name if test_name else ""
    filename = "results/" + domain

    with open(filename + suffix + ".html", "r") as f:
        # Read html code and pass it to parser
        html = f.read()
        parser = MyHTMLParser()
        parser.feed(html)

    # Extract some statistics
    different_tags = list(parser.tags.keys())
    n_nodes = sum(parser.tags.values())
    n_different_tags = len(different_tags)
    n_different_attributes = (len(parser.attributes))
    different_classes = parser.attributes["class"]
    css_urls = filter(lambda url: bool(re.search(r"\.css(\?.*)?$", url)), parser.attributes["href"])


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
            # f.write(response.content)


            allowed_tags = different_tags
            allowed_classes = different_classes
            css_classes, css_properties, css_classes_skipped, css_properties_skipped = parse_css(response.content, allowed_tags, allowed_classes, file=f)
            

            # Print number of css classes TODO write in log file
            print("\nCSS classes: ")
            pprint(dict(sorted(css_classes.items(), reverse=True, key=lambda item: item[1])), sort_dicts=False)

            # Print number of css properties TODO write in log file
            print("\nCSS properties: ")
            pprint(dict(sorted(css_properties.items(), reverse=True, key=lambda item: item[1])), sort_dicts=False)

            # Print number of css classes skipped TODO write in log file
            print("\nCSS classes skipped: ")
            pprint(css_classes_skipped)

            # Print number of css properties skipped TODO write in log file
            print("\nCSS properties skipped: ")
            pprint(css_properties_skipped)


def print_statistics():
    return
