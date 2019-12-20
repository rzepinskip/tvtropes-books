from tvtropes.parser import SpoilerParser
import os
import bz2
from lxml import html
from tvtropes.scraper import TVTropesScraper
import base64

dir = "data/scraper/cache/20190502"


def _build_encoded_url(url):
    encoded_url = base64.b64encode(url.encode("utf-8")).decode("utf-8") + ".bz2"
    return encoded_url.replace("/", "_")


def decode_url(file_name):
    base = file_name.replace(".html.bz2", "")
    decoded = base64.b64decode(base)
    return decoded


def read(file_path):
    with open(file_path, "rb") as file:
        content = file.read()
    content = bz2.decompress(content)
    return content.decode("utf-8", errors="ignore")


LINK_SELECTOR_INSIDE_ARTICLE = "#main-article > ul > li"


# https://medium.com/contentsquare-engineering-blog/multithreading-vs-multiprocessing-in-python-ece023ad55a

subset = os.listdir(dir)
tagged_sentences = list()
parser = SpoilerParser()
expected_spoiler = 0

for page_file in subset[2:3]:
    content = read(os.path.join(dir, page_file))
    print(decode_url(page_file))
    tree = html.fromstring(content)
    listing = [
        html.tostring(element)
        for element in tree.cssselect(LINK_SELECTOR_INSIDE_ARTICLE)
    ]
    expected_spoiler += len(tree.cssselect("#main-article > ul > li .spoiler"))
    # print(content)
    for entry in listing[:]:
        tree = html.fromstring(entry)
        tagged_sentences += parser.parse(tree)

spoilers = [
    (tag, sentence)
    for review in tagged_sentences
    for tag, sentence in review
    if str(tag) == "TAG.SPOILER"
]
len(spoilers)
spoilers

# Blood Knight: The book contains three of these: Greven il-Vec, as it is said at one point that he only smiles when he is about to kill someone. Like all Keldon warriors, Maraxus of Keld is one of these. Crovax becomes one of these in the final chapter.
#  Greven il-Vec, as it is said at one point that he only smiles when he is about to kill someone.
#  Like all Keldon warriors, Maraxus of Keld is one of these.
#  Crovax becomes one of these in the final chapter.

