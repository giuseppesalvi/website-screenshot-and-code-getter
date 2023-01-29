from html.parser import HTMLParser
from collections import defaultdict
import re

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

