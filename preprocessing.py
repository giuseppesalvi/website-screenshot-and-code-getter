import time
from pathlib import Path
import re
from bs4 import BeautifulSoup
import multiprocessing
from tqdm import tqdm


# Lists of known inline and block tags for reference
INLINE_TAGS = ['a', 'abbr', 'acronym', 'area', 'b', 'base', 'bdo', 'big', 'br', 'button', 'cite', 'code', 'data', 'datalist', 'dfn', 'em', 'i', 'img', 'input', 'kbd', 'label', 'map', 'mark',
               'meter', 'object', 'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'select', 'small', 'span', 'strong', 'sub', 'sup', 'svg', 'textarea', 'time', 'tt', 'u', 'var', 'wbr']
BLOCK_TAGS = ['address', 'article', 'aside', 'blockquote', 'canvas', 'dd', 'div', 'dl', 'dt', 'fieldset', 'figcaption', 'figure', 'footer', 'orm', 'h1', 'h2',
              'h3', 'h4', 'h5', 'h6', 'header', 'hgroup', 'hr', 'li', 'main', 'nav', 'noscript', 'ol', 'output', 'p', 'pre', 'section', 'table', 'tfoot', 'ul''video']
VALID_TAGS = ['div', 'a', 'span', 'li', 'img', 'p', 'ul', 'i', 'link', 'option', 'input', 'td', 'h2', 'br', 'h3', 'button', 'label', 'source', 'article', 'section', 'strong', 'h4', 'tr', 'picture', 'b', 'time', 'figure', 'header', 'style', 'nav', 'h1', 'h5', 'form', 'em', 'footer', 'hr', 'table', 'tbody', 'title', 'small', 'body', 'html', 'head', 'h6', 'th', 'dd', 'aside', 'select', 'figcaption', 'dt', 'main', 'dl', 'sup', 'ins', 'fieldset', 'blockquote', 'video', 'legend', 'template', 'code', 'area', 'u', 'textarea', 'thead', 'abbr', 'canvas', 'cite', 'bdi', 'address', 'pre', 'rs-mask-wrap',
              'object', 'optgroup', 'summary', 'details', 'del', 'mark', 'rs-slide', 'col', 'base', 'audio', 'sub', 'hgroup', 'map', 'var', 'caption', 'q', 'kbd', 'wbr', 'param', 'data', 'text', 'dfn', 'strike', 'menu', 'rs-module-wrap', 'rs-module', 'colgroup', 'progress', 'tfoot', 'c', 'icon', 'dialog', 'embed', 'xmp', 'output', 'rt', 'bdo', 'content', 'slot', 'swiper-slide', 'meter', 'none', 'row', 'devsite-header', 'devsite-book-nav', 'noframes', 'dir', 'noembed', 't', 'right', 'close', 'applet', 'n-footer-new-design', 'message', 'container', 'dropdown-menu', 'bgsound', 'dropdown-toggle']


def round_floats_in_text(text, precision=0):
    # Match float numbers with 2 or more decimal places in the text
    pattern = r"\b\d+\.\d{2,}\b"

    # Reduce their precision
    def replace(match):
        float_number = float(match.group())
        return f"{float_number:.{precision}f}"

    text = re.sub(pattern, replace, text)
    return text


def remove_html_comments(text):
    # Match html comments
    pattern = r"<!--.*?-->"

    text = re.sub(pattern, '', text, flags=re.DOTALL)
    return text


def remove_css_comments(text):
    # Match css comments
    pattern = r"/\*.*?\*/"

    text = re.sub(pattern, '', text, flags=re.DOTALL)
    return text


def remove_spaces_and_break_lines(text):
    # Remove multiple spaces, tabs and newlines
    without_new_line = text.replace('\n', ' ').replace('\t', ' ')
    with_single_space = ' '.join([string_ for string_ in (
        without_new_line.split(' ')) if string_ != ''])
    return with_single_space


def replace_http_links(text, placeholder_url="https://example.com"):
    # Match urls starting with http or https
    url_pattern = re.compile(r'(?<=[\'"])https?://.*?(?=[\'"])')

    # Replace all URLs with the placeholder URL
    return url_pattern.sub(placeholder_url, text)


def replace_local_hrefs(text, special_url, special_image_url="../../images/default_img.jpeg", placeholder_url="ref.placeholder"):
    # Regular expression pattern to match local href references that are not the special URLs.
    # The pattern ensures href values that don't start with a protocol are matched.
    local_ref_pattern = re.compile(
        r'href=["\'](?!http|https|ftp|file|mailto:|{}|{})([^"\']+)["\']'.format(
            re.escape(special_url),
            re.escape(special_image_url)))

    # Replace local references with the default local reference
    return local_ref_pattern.sub(r'href="{}"'.format(placeholder_url), text)


def replace_css_urls(text, placeholder_url="ref.placeholder"):
    pattern = re.compile(r'url\((["\']?)([^"\'\)]+)\1\)')
    return pattern.sub(lambda m: f'url({placeholder_url})', text)


def decide_replacement(tag):
    # Check the content of the non-standard tag to determine whether it's a block or inline tag
    if any(child.name in BLOCK_TAGS for child in tag.children):
        return 'div'
    elif any(child.name in INLINE_TAGS for child in tag.children) or tag.string:
        return 'span'
    return 'div'  # default


def replace_unknown_tags(text):
    # Replace non-standard tags with default ones
    soup = BeautifulSoup(text, 'html.parser')

    for tag in soup.find_all():
        if tag.name not in VALID_TAGS:
            tag.name = decide_replacement(tag)

    return str(soup)


def process_html_file(content, filename):
    text_without_comments = remove_html_comments(content)
    text_without_floats = round_floats_in_text(text_without_comments)
    text_without_multiple_spaces = remove_spaces_and_break_lines(
        text_without_floats)
    text_without_http_urls = replace_http_links(text_without_multiple_spaces)
    text_without_local_links = replace_local_hrefs(
        text_without_http_urls, f"{filename}.css")
    text_without_unknown_tags = replace_unknown_tags(text_without_local_links)
    return text_without_unknown_tags


def process_css_file(content):
    text_without_comments = remove_css_comments(content)
    text_without_floats = round_floats_in_text(text_without_comments)
    text_without_multiple_spaces = remove_spaces_and_break_lines(
        text_without_floats)
    text_without_urls = replace_css_urls(text_without_multiple_spaces)

    return text_without_urls


def save_processed_file(html_processed, css_processed, filename, destination_folder):
    delimeter = " /* START CSS */ "
    composed_file = html_processed + delimeter + css_processed

    with open(destination_folder / f"{filename}.txt", "w") as f:
        f.write(composed_file)

    return


def process_file(filename, source_folder, destination_folder):
    html_filename = source_folder / f"{filename}.html"
    css_filename = source_folder / f"{filename}.css"

    with open(html_filename, "r") as f:
        html_processed = process_html_file(f.read(), filename)

    with open(css_filename, "r") as f:
        css_processed = process_css_file(f.read())

    save_processed_file(html_processed, css_processed, filename, destination_folder)
    return


def preprocessing(filenames, source_folder, destination_folder):
    destination_folder = Path(destination_folder)
    source_folder = Path(source_folder)

    if not destination_folder.exists():
        destination_folder.mkdir(parents=True)

    pool_size = multiprocessing.cpu_count()

    with multiprocessing.Pool(processes=pool_size) as pool:
        tqdm(pool.starmap(process_file, [(filename, source_folder, destination_folder) for filename in filenames]), total=len(filenames))
    return


if __name__ == "__main__":
    filenames_file = "experiments/results_good.txt"
    source_folder = "experiments/results_good/"
    destination_folder = "preprocessed_files/"
    start = time.time()

    with open(filenames_file, "r") as f:
        filenames = [filename.rstrip() for filename in f]

    preprocessing(filenames, source_folder, destination_folder)
    print(time.time() - start)
