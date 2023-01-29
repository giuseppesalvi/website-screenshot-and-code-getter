import tinycss2
import sys
from types import SimpleNamespace
from pprint import pprint

CSS_INDENTATION = "    "
skipped = set()


def parse_css(css, different_tags, different_classes, file):
    # Parse the stylesheet
    rules, encoding = tinycss2.parse_stylesheet_bytes(
        css, skip_comments=True, skip_whitespace=True)
    for rule in rules:
        # tinycss2.parse_declaration_list(rule.content)
        type = rule.type  # ex: "qualified-rule"
        # qualified-rule: <prelude> '{' <content> '}'
        # at-rule:        @<at-keyword> <prelude> '{' <content> '}'
        #                 @<at-rule> <prelude> ';'
        output_file = file 
        #output_file = sys.stdout 
        # output_file = sys.stdout # DBG
        if type == "qualified-rule":
            res = process_qualified_rule(rule, different_tags=different_tags, different_classes=different_classes)
            print(res, end="", file=output_file)
        elif type == "at-rule":
            res = process_at_rule(rule, different_tags=different_tags, different_classes=different_classes)
            print(res, end="", file=output_file)
        else:
            print(type, file=file)
            break

    # skipped classes
    print("skipped")
    pprint(skipped)


def process_qualified_rule(rule, different_tags, different_classes, indentation=""):
    buffer = ""
    prelude = rule.prelude
    content = rule.content

    prelude_buffer = process_prelude(prelude, different_tags, different_classes, indentation=indentation)
    if prelude_buffer and not prelude_buffer.isspace() and content:
        buffer += prelude_buffer
        content_buffer = process_content(content, indentation=indentation)
        buffer += content_buffer
    return buffer


def process_at_rule(rule, different_tags, different_classes, indentation=""):
    buffer = ""
    prelude = rule.prelude
    content = rule.content

    prelude_buffer = process_prelude(prelude, different_tags, different_classes)

    if prelude_buffer and not prelude_buffer.isspace():
        at_keyword = "@" + rule.at_keyword
        at_keyword.replace(" ", "")
        if content:
            buffer_content_at = process_content_at_rule(content, different_tags, different_classes, indentation=indentation)
            if buffer_content_at:
                buffer += indentation + at_keyword
                buffer += prelude_buffer
                buffer += "{\n"
                buffer += buffer_content_at
                buffer += indentation + "}\n\n"
            else:
                print("skipped at rule")
        else:
            buffer += indentation + at_keyword
            buffer += prelude_buffer
            buffer += ";\n\n"
    return buffer

def process_prelude(prelude, different_tags, different_classes, indentation=""):
    # Print prelude
    result_buffer = ""
    buffer = ""  # Keep ident and whitespace to see if the next literal must be kept

    result_buffer += indentation

    skip = False
    buffer_comma = ""

    # TEST: filter classes or not
    filter_classes = True

    for token in prelude:
        printable = token.serialize()
        if token.type == "ident":
            # Check if ident is in the list of classes
            if filter_classes and printable not in different_classes and printable not in different_tags:
                buffer = ""
                skip = True
                skipped.add(printable)
            else:
                buffer += printable

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

    if buffer:  # if buffer is not empty
        if not skip:
            result_buffer += buffer_comma + buffer + " "
            buffer = ""

    return result_buffer


def process_content(content, indentation=""):
    result_buffer=""
    for idx, token in enumerate(content):
        printable = token.serialize()
        if idx == 0:
            if printable == " ":
                result_buffer += "{\n" + CSS_INDENTATION + indentation
            else:
                result_buffer += "{\n" + CSS_INDENTATION + indentation + printable

        elif idx == len(content) - 1:
            if token.serialize != ";":
                result_buffer += printable + ";\n" + indentation + "}\n\n"
            else:
                result_buffer += printable + "\n" + indentation + "}\n\n"

        elif token.serialize() == ";":
            result_buffer += printable + "\n" + CSS_INDENTATION + indentation
        elif token.serialize() == ":":
            result_buffer += printable + " "
        else:
            result_buffer += printable
    return result_buffer


def process_content_at_rule(content, different_tags, different_classes, indentation=""):
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
            buffer += process_at_rule(nested_rule, different_tags, different_classes,indentation=indentation+CSS_INDENTATION)
            skip = 3
        elif node.type != "{} block":
            qualified_rule_prelude.append(node)
        else:
            if len(qualified_rule_prelude) == 0:
                if not skipped_prelude:
                    buffer += process_content_at_rule(node.content, different_tags, different_classes, indentation=indentation)
            else:
                prelude_buffer = process_prelude(qualified_rule_prelude, different_tags, different_classes, indentation=indentation+CSS_INDENTATION)
                if prelude_buffer and not prelude_buffer.isspace():
                    buffer += prelude_buffer
                    buffer_content = process_content(node.content, indentation=indentation+CSS_INDENTATION)
                    buffer += buffer_content
                    skipped_prelude = False 
                else:
                    skipped_prelude = True
                qualified_rule_prelude = []
    return buffer
