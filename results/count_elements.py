from html.parser import HTMLParser
from collections import defaultdict
from pprint import pprint
import sys

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.count = defaultdict(int)
        super().__init__()

    def handle_starttag(self, tag, attrs):
        self.count[tag] += 1

    def handle_startendtag(self, tag, attrs):
        self.count[tag] +=1


if __name__ == "__main__":
    args = sys.argv
    filename = args[1]   

    with open(filename, "r") as f:
        html = f.read()
        parser = MyHTMLParser()
        parser.feed(html)

    print("number of nodes: ", sum(parser.count.values()))
    print("divided per element: ")
    pprint(parser.count)

    with open(filename + "_log", "w") as f:
        print("number of nodes: ", sum(parser.count.values()), file=f)
        print("divided per element: ", file=f)
        pprint(parser.count, f)
