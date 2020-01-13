import os
import base64
import bz2

from enum import Enum
from lxml import html, etree
from lxml.html.clean import Cleaner
from typing import List, Tuple, Dict, Any
from tvtropes.base_script import BaseScript
import spacy
from spacy.lang.en import English
import en_core_web_sm


class SpoilerStatus(Enum):
    OPEN = 1
    CLOSED_NOTUSED = 2
    CLOSED = 4


class SpoilerParser(BaseScript):
    DEFAULT_ENCODING = "utf-8"

    def __init__(self):
        BaseScript.__init__(self, dict())
        self.before_cleaner = Cleaner(
            allow_tags=["span", "div"], remove_unknown_tags=False, kill_tags=[]
        )
        self._nlp = en_core_web_sm.load(disable=["parser", "ner"])
        self._nlp.add_pipe(self._nlp.create_pipe("sentencizer"))

    def parse_dir(self, dir: str) -> List[Dict[str, Any]]:
        def decode_url(file_name):
            base = file_name.replace(".html.bz2", "")
            decoded = base64.b64decode(base).decode(self.DEFAULT_ENCODING)
            return decoded

        def read(file_path):
            with open(file_path, "rb") as file:
                content = file.read()
            content = bz2.decompress(content)
            return content.decode(self.DEFAULT_ENCODING, errors="ignore")

        subset = os.listdir(dir)
        expected_spoiler = 0

        results: List[Dict[str, Any]] = list()
        for idx, page_file in enumerate(subset[:]):
            url = decode_url(page_file)
            self._track_message(f"{idx+1}/{len(subset)} - {url}")

            content = read(os.path.join(dir, page_file))
            tree = html.fromstring(content)
            listing = [
                html.tostring(element, encoding="unicode")
                for element in tree.cssselect("#main-article > ul > li")
            ]
            for entry in listing:
                trope, sentences = self.parse(entry)
                results += [{"page": url, "trope": trope, "sentences": sentences,}]

        self._finish_and_summary()
        return results

    def _split_into_sentences(self, text: str):
        doc = self._nlp(text)
        output = []
        for sentence in doc.sents:
            if len(sentence) == 0:
                continue

            for token in sentence:
                if token.pos_ == "VERB" or token.pos_ == "AUX":
                    output.append(sentence.string.strip())
                    break

        return output

    def parse(self, raw_data: str) -> Tuple[str, List[Tuple[bool, str]]]:
        raw_data = Cleaner(kill_tags=["div"]).clean_html(raw_data)
        cleaned_data = self.before_cleaner.clean_html(f"<div>{raw_data}</div>")
        colon_idx = cleaned_data.find(":")
        trope = cleaned_data[:colon_idx]
        cleaned_data = cleaned_data[colon_idx + 1 :]
        data = (
            cleaned_data.replace("</div>", "")
            .replace("...", ".")
            .replace("◊", "")
            .replace(".</span>", "</span>.")
        )

        sentences = self._split_into_sentences(data)
        data = "|".join(sentences)

        tagged_sentences = list()
        i, start = 0, 0
        status = SpoilerStatus.CLOSED
        while i < len(data):
            if data[i] == "<":
                if data[i + 1] == "/":
                    i = i + len("""</span>""")
                    status = SpoilerStatus.CLOSED_NOTUSED
                else:
                    i = i + len("""<span class="spoiler" title="x">""")
                    status = SpoilerStatus.OPEN
                continue

            if data[i] == "|" or i == len(data) - 1:
                if status is SpoilerStatus.CLOSED:
                    tag = False
                elif status is SpoilerStatus.OPEN:
                    tag = True
                elif status is SpoilerStatus.CLOSED_NOTUSED:
                    tag = True
                    status = SpoilerStatus.CLOSED
                tagged_sentences.append((tag, data[start : i + 1]))
                start = i + 1

            i += 1

        def clean_all(sentence):
            element = html.fromstring(sentence)
            str_repr = etree.tostring(element, method="text", encoding="unicode")
            return " ".join(str_repr.split()).strip()

        return (
            clean_all(trope),
            [(tag, clean_all(sentence)) for tag, sentence in tagged_sentences],
        )

