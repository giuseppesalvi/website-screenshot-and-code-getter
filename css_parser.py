import tinycss2
import sys
from types import SimpleNamespace
from pprint import pprint

CSS_INDENTATION = "    "

css_classes_skipped = set()
css_classes = {}

css_forbidden_properties = ["font-style", "text-transform", "letter-spacing", "word-spacing", "line-height", "text-shadow", "box-shadow", "background-image", "background-repeat", "background-position"]
#"font-weight" ,"font-family" ,"color" ,"opacity","word-wrap","hyphens","overflow-wrap","text-indent","text-overflow","white-space","word-break","border-radius","border-style","border-color","border-width"
css_properties = {}
css_properties_skipped = set()

def parse_css(css, allowed_tags, allowed_classes, file):
    # Parse the stylesheet
    rules, encoding = tinycss2.parse_stylesheet_bytes(css, skip_comments=True, skip_whitespace=True)
    for rule in rules:
        # tinycss2.parse_declaration_list(rule.content)
        type = rule.type  # ex: "qualified-rule"
        # qualified-rule: <prelude> '{' <content> '}'
        # at-rule:        @<at-keyword> <prelude> '{' <content> '}'
        #                 @<at-rule> <prelude> ';'
        output_file = file 
        # output_file = sys.stdout # DBG
        if type == "qualified-rule":
            print(process_qualified_rule(rule, allowed_tags=allowed_tags, allowed_classes=allowed_classes), end="", file=output_file)
        elif type == "at-rule":
            print(process_at_rule(rule, allowed_tags=allowed_tags, allowed_classes=allowed_classes), end="", file=output_file)
        else:
            print(type, file=file)
            break

    return css_classes, css_properties, css_classes_skipped, css_properties_skipped


def process_qualified_rule(rule, allowed_tags, allowed_classes, indentation=""):
    buffer = ""
    prelude = rule.prelude
    content = rule.content

    prelude_buffer = process_prelude(prelude, allowed_tags, allowed_classes, indentation=indentation)
    if prelude_buffer and not prelude_buffer.isspace() and content:
        content_buffer = process_content(content, indentation=indentation)
        if content_buffer != "" and not content_buffer.isspace():
            buffer += prelude_buffer
            buffer += "{\n" + CSS_INDENTATION + indentation
            buffer += content_buffer
            buffer += "\n" + indentation + "}\n\n"
    return buffer


def process_at_rule(rule, allowed_tags, allowed_classes, indentation=""):
    buffer = ""
    prelude = rule.prelude
    content = rule.content

    prelude_buffer = process_prelude(prelude, allowed_tags, allowed_classes)

    if prelude_buffer and not prelude_buffer.isspace():
        at_keyword = "@" + rule.at_keyword
        at_keyword.replace(" ", "")
        if content:
            buffer_content_at = process_content_at_rule(content, allowed_tags, allowed_classes, indentation=indentation)
            if buffer_content_at:
                buffer += indentation + at_keyword
                buffer += prelude_buffer
                buffer += "{\n"
                buffer += buffer_content_at
                buffer += indentation + "}\n\n"
        else:
            buffer += indentation + at_keyword
            buffer += prelude_buffer
            buffer += ";\n\n"
    return buffer

def process_prelude(prelude, allowed_tags, allowed_classes, indentation="", filter_classes=True):
    result_buffer = ""
    buffer = ""  # Keep ident and whitespace to see if the next literal must be kept

    result_buffer += indentation

    skip = False
    buffer_comma = ""

    for token in prelude:
        printable = token.serialize()
        if token.type == "ident":
            # Check if ident is in the list of allowed classes and tags
            if filter_classes and printable not in allowed_classes and printable not in allowed_tags:
                buffer = ""
                skip = True
                css_classes_skipped.add(printable)
            else:
                buffer += printable

                # add ident to css_classes
                if printable not in css_classes:
                    css_classes[printable] = 1
                else:
                    css_classes[printable] += 1

        else:
            if printable == ",":
                if not skip:
                    result_buffer += buffer_comma + buffer + " "
                    buffer = ""
                    buffer_comma = ","
                else:
                    skip = False
            else:
                if not skip:
                    buffer += printable
                else:
                    buffer = ""

    if buffer: 
        if not skip:
            result_buffer += buffer_comma + buffer + " "
            buffer = ""

    return result_buffer


def process_content(content, indentation=""):
    result_buffer=""
    is_property = True 
    for token in content:
        printable = token.serialize()
        if token.serialize() == ";":
            result_buffer += printable + "\n" + CSS_INDENTATION + indentation
            is_property = True
        elif token.serialize() == ":":
            result_buffer += printable + " "
        else:
            result_buffer += printable
            if is_property:
                if printable not in css_properties:
                    css_properties[printable] = 1
                else:
                    css_properties[printable] += 1

            is_property = False
    return result_buffer


def process_content_at_rule(content, allowed_tags, allowed_classes, indentation=""):
    buffer = ""
    qualified_rule_prelude = []
    skip = 0
    skipped_prelude = True 
    for idx, node in enumerate(content):
        if skip > 0:
            skip -= 1
            continue
        if node.type == 'at-keyword':
            nested_rule = SimpleNamespace()
            nested_rule.at_keyword = content[idx].value
            nested_rule.prelude = [content[idx+1], content[idx+2]]
            nested_rule.content = content[idx+3].content
            buffer += process_at_rule(nested_rule, allowed_tags, allowed_classes,indentation=indentation+CSS_INDENTATION)
            skip = 3
        elif node.type != "{} block":
            qualified_rule_prelude.append(node)
        else:
            if len(qualified_rule_prelude) == 0:
                if not skipped_prelude:
                    buffer += process_content_at_rule(node.content, allowed_tags, allowed_classes, indentation=indentation)
            else:
                prelude_buffer = process_prelude(qualified_rule_prelude, allowed_tags, allowed_classes, indentation=indentation+CSS_INDENTATION)
                if prelude_buffer and not prelude_buffer.isspace():
                    buffer += prelude_buffer
                    buffer_content = process_content(node.content, indentation=indentation+CSS_INDENTATION)
                    if buffer_content != "" and not buffer_content.isspace():
                        buffer += prelude_buffer
                        buffer += "{\n" + CSS_INDENTATION + indentation 
                        buffer +=  CSS_INDENTATION + buffer_content 
                        buffer += "\n" + CSS_INDENTATION + indentation + "}\n\n"
                    skipped_prelude = False 
                else:
                    skipped_prelude = True
                qualified_rule_prelude = []
    return buffer
