import tinycss2
from types import SimpleNamespace

CSS_INDENTATION = "    "


css_forbidden_properties_1= ["font-style", "text-transform", "letter-spacing", "word-spacing", "line-height", "text-shadow", "box-shadow", "background-image", "background-repeat", "background-position", "hyphens", "border-radius","border-style","border-color","border-width"]
#LIST 1 css_forbidden_properties = ["font-style", "text-transform", "letter-spacing", "word-spacing", "line-height", "text-shadow", "box-shadow", "background-image", "background-repeat", "background-position"]
#LIST 2 "font-weight" ,"font-family" ,"color" ,"opacity","word-wrap","hyphens","overflow-wrap","text-indent","text-overflow","white-space","word-break","border-radius","border-style","border-color","border-width"
css_my_forbidden_properties = ["moz-osx-font-smoothing","-webkit-font-smoothing", "-ms-user-select","-moz-user-select", "-moz-transform", "-moz-transform-origin", "-moz-columns", "-moz-osx-font-smoothing", "-moz-column-break-inside"]

css_mozilla_properties = [ "-moz-appearance", "-moz-binding", "-moz-border-bottom-colors", "-moz-border-left-colors", "-moz-border-right-colors", "-moz-border-top-colors", "-moz-box-align", "-moz-box-direction", "-moz-box-flex", "-moz-box-ordinal-group", "-moz-box-orient", "-moz-box-pack", "-moz-box-shadow", "-moz-box-sizing", "-moz-column-count", "-moz-column-gap", "-moz-column-rule-color", "-moz-column-rule-style", "-moz-column-rule-width", "-moz-column-width", "-moz-float-edge", "-moz-font-feature-settings", "-moz-font-language-override", "-moz-force-broken-image-icon", "-moz-hyphens", "-moz-image-region", "-moz-margin-end", "-moz-margin-start", "-moz-outline-radius-bottomleft", "-moz-outline-radius-bottomright", "-moz-outline-radius-topleft", "-moz-outline-radius-topright", "-moz-padding-end", "-moz-padding-start", "-moz-text-align-last", "-moz-text-blink", "-moz-text-decoration-color", "-moz-text-decoration-line", "-moz-text-decoration-style", "-moz-text-size-adjust", "-moz-user-focus", "-moz-user-input", "-moz-user-modify", "-moz-user-select", "-moz-window-shadow"]
css_ie_properties = [ "-ms-accelerator", "-ms-behavior", "-ms-block-progression", "-ms-content-zooming", "-ms-filter", "-ms-flex", "-ms-flex-align", "-ms-flex-direction", "-ms-flex-item-align", "-ms-flex-line-pack", "-ms-flex-order", "-ms-flex-pack", "-ms-flex-wrap", "-ms-grid-column", "-ms-grid-column-align", "-ms-grid-column-span", "-ms-grid-columns", "-ms-grid-layer", "-ms-grid-row", "-ms-grid-row-align", "-ms-grid-row-span", "-ms-grid-rows", "-ms-high-contrast-adjust", "-ms-hyphenate-limit-chars", "-ms-hyphenate-limit-lines", "-ms-hyphenate-limit-zone", "-ms-ime-align", "-ms-line-break", "-ms-overflow-style", "-ms-scrollbar-3dlight-color", "-ms-scrollbar-arrow-color", "-ms-scrollbar-base-color", "-ms-scrollbar-darkshadow-color", "-ms-scrollbar-face-color", "-ms-scrollbar-highlight-color", "-ms-scrollbar-shadow-color", "-ms-scrollbar-track-color", "-ms-text-autospace", "-ms-text-combine-horizontal", "-ms-text-justify", "-ms-text-kashida-space", "-ms-text-overflow", "-ms-text-size-adjust", "-ms-text-underline-position", "-ms-touch-select", "-ms-transform", "-ms-transform-origin", "-ms-transition", "-ms-transition-delay", "-ms-transition-duration", "-ms-transition-property", "-ms-transition-timing-function", "-ms-user-select", "-ms-word-break", "-ms-wrap-flow", "-ms-wrap-margin", "-ms-wrap-through", "-ms-writing-mode"]
css_dynamic_properties = [ "transition", "transition-delay", "transition-duration", "transition-property", "transition-timing-function", "animation", "animation-delay", "animation-direction", "animation-duration", "animation-fill-mode", "animation-iteration-count", "animation-name", "animation-play-state", "animation-timing-function"]

css_forbidden_properties =css_forbidden_properties_1 + css_my_forbidden_properties + css_mozilla_properties + css_ie_properties + css_dynamic_properties

def parse_css(css, allowed_tags, allowed_classes, file, sanitize):
    css_dict = {}
    css_dict["allowed_tags"] = allowed_tags
    css_dict["allowed_classes"] = allowed_classes
    css_dict["css_classes"] = {}
    css_dict["css_classes_skipped"] = {} 
    css_dict["css_properties"] = {}
    css_dict["css_properties_skipped"] = {}
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
            print(process_qualified_rule(rule, css_dict, sanitize), end="", file=output_file)
        elif type == "at-rule":
            print(process_at_rule(rule, css_dict, sanitize), end="", file=output_file)
        else:
            print(type, file=file)
            break

    return css_dict["css_classes"], css_dict["css_properties"], css_dict["css_classes_skipped"], css_dict["css_properties_skipped"]


def process_qualified_rule(rule, css_dict, sanitize, indentation=""):
    buffer = ""
    prelude = rule.prelude
    #content = rule.content TODO
    content = get_content(rule) 

    prelude_buffer = process_prelude(prelude, css_dict, sanitize, indentation=indentation)
    if prelude_buffer and not prelude_buffer.isspace() and content:
        content_buffer = process_content(content, css_dict, sanitize, indentation=indentation)
        if content_buffer and not content_buffer.isspace():
            buffer += prelude_buffer
            buffer += "{\n" + CSS_INDENTATION + indentation
            buffer += content_buffer
            buffer += "\n" + indentation + "}\n\n"
    return buffer


def process_at_rule(rule, css_dict, sanitize, indentation=""):
    buffer = ""
    prelude = rule.prelude
    #content = rule.content TODO
    content = get_content(rule) 

    prelude_buffer = process_prelude(prelude, css_dict, sanitize)

    if prelude_buffer and not prelude_buffer.isspace():
        at_keyword = "@" + rule.at_keyword
        at_keyword.replace(" ", "")
        if content:
            buffer_content_at = process_content_at_rule(content, css_dict, sanitize, indentation=indentation)
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

def process_prelude(prelude, css_dict, sanitize, indentation=""):
    result_buffer = ""
    buffer = ""  # Keep ident and whitespace to see if the next literal must be kept

    result_buffer += indentation

    skip = False
    buffer_comma = ""

    for token in prelude:
        printable = token.serialize()
        if token.type == "ident":
            # Check if ident is in the list of allowed classes and tags
            if sanitize and printable not in css_dict["allowed_classes"] and printable not in css_dict["allowed_tags"]:
                buffer = ""
                skip = True
                if printable not in css_dict["css_classes_skipped"]:
                    css_dict["css_classes_skipped"][printable] = 1
                else:
                    css_dict["css_classes_skipped"][printable] += 1
            else:
                buffer += printable

                # add ident to css_classes
                if printable not in css_dict["css_classes"]:
                    css_dict["css_classes"][printable] = 1
                else:
                    css_dict["css_classes"][printable] += 1

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


def process_content(content, css_dict, sanitize, indentation=""):
    result_buffer=""
    is_property = True 
    skip = False
    if content is None:
        return result_buffer
    else:
        for token in content:
            printable = token.serialize()
            if token.serialize() == ";":
                if not skip:
                    result_buffer += printable + "\n" + CSS_INDENTATION + indentation
                is_property = True
                skip = False
            elif token.serialize() == ":":
                if not skip:
                    result_buffer += printable + " "
            else:
                if sanitize and printable in css_forbidden_properties:
                    skip = True
                    if printable not in css_dict["css_properties_skipped"]:
                        css_dict["css_properties_skipped"][printable] = 1
                    else:
                        css_dict["css_properties_skipped"][printable] += 1
                else: 
                    if not skip:
                        result_buffer += printable
                        if is_property:
                            if printable not in css_dict["css_properties"]:
                                css_dict["css_properties"][printable] = 1
                            else:
                                css_dict["css_properties"][printable] += 1

                is_property = False
        return result_buffer


def process_content_at_rule(content, css_dict, sanitize, indentation=""):
    buffer = ""
    qualified_rule_prelude = []
    skip = 0
    skipped_prelude = True 
    if content is None:
        return buffer
    else:
        for idx, node in enumerate(content):
            if skip > 0:
                skip -= 1
                continue
            if node.type == 'at-keyword':
                nested_rule = SimpleNamespace()
                nested_rule.at_keyword = content[idx].value
                nested_rule.prelude = [content[idx+1], content[idx+2]]
                #nested_rule.content = content[idx+3].content
                nested_rule.content = get_content(content[idx+3]) 
                buffer += process_at_rule(nested_rule, css_dict, sanitize, indentation=indentation+CSS_INDENTATION)
                skip = 3
            elif node.type != "{} block":
                qualified_rule_prelude.append(node)
            else:
                if len(qualified_rule_prelude) == 0:
                    if not skipped_prelude:
                        #buffer += process_content_at_rule(node.content, css_dict, sanitize, indentation=indentation)
                        buffer += process_content_at_rule(get_content(node.content), css_dict, sanitize, indentation=indentation)
                else:
                    prelude_buffer = process_prelude(qualified_rule_prelude, css_dict, sanitize, indentation=indentation+CSS_INDENTATION)
                    if prelude_buffer and not prelude_buffer.isspace():
                        #buffer_content = process_content(node.content, css_dict, sanitize, indentation=indentation+CSS_INDENTATION)
                        buffer_content = process_content(get_content(node.content), css_dict, sanitize, indentation=indentation+CSS_INDENTATION)
                        if buffer_content and not buffer_content.isspace():
                            buffer += prelude_buffer
                            buffer += "{\n" + CSS_INDENTATION + indentation 
                            buffer +=  CSS_INDENTATION + buffer_content 
                            buffer += "\n" + CSS_INDENTATION + indentation + "}\n\n"
                        skipped_prelude = False 
                    else:
                        skipped_prelude = True
                    qualified_rule_prelude = []
        return buffer

def get_content(element):
    try:
        content = element.content
    except Exception as e:
        content = None
    return content
