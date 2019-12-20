from tvtropes.parser import SpoilerParser
import os
import bz2
from lxml import html, etree
import base64
import logging
import json

dir = "data/scraper/cache/20190502"


def _build_encoded_url(url):
    encoded_url = base64.b64encode(url.encode("utf-8")).decode("utf-8") + ".bz2"
    return encoded_url.replace("/", "_")


def decode_url(file_name):
    base = file_name.replace(".html.bz2", "")
    decoded = base64.b64decode(base).decode("utf-8")
    return decoded


def read(file_path):
    with open(file_path, "rb") as file:
        content = file.read()
    content = bz2.decompress(content)
    return content.decode("utf-8", errors="ignore")


LINK_SELECTOR_INSIDE_ARTICLE = "#main-article > ul > li"

subset = os.listdir(dir)
parser = SpoilerParser()
expected_spoiler = 0

results = list()
for idx, page_file in enumerate(subset[:10]):
    # print(f"{idx+1}/{len(subset)}")
    content = read(os.path.join(dir, page_file))
    # print(decode_url(page_file))
    tree = html.fromstring(content)
    listing = [
        html.tostring(element)
        for element in tree.cssselect(LINK_SELECTOR_INSIDE_ARTICLE)
    ]
    expected_spoiler += len(tree.cssselect("#main-article > ul > li .spoiler"))
    tagged_sentences = list()
    for entry in listing:
        tagged_sentences += [parser.parse(entry.decode("utf-8"))]
    results += [(decode_url(page_file), tagged_sentences)]

spoilers = [
    (tag, sentence)
    for _, reviews in results
    for review in reviews
    for tag, sentence in review
    if tag
]
len(spoilers)

# json.dumps(results)
# results
