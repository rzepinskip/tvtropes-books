import base64
import bz2
import os
from enum import Enum
from typing import Any, Dict, List, Tuple

import en_core_web_sm
import spacy
from lxml import etree, html
from lxml.html.clean import Cleaner
from spacy.lang.en import English

from tvtropes.base_script import BaseScript


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

    def decode_url(self, file_name):
        base = os.path.basename(file_name).replace(".html.bz2", "")
        decoded = base64.urlsafe_b64decode(base).decode(self.DEFAULT_ENCODING)
        return decoded

    def read(self, file_path):
        with open(file_path, "rb") as file:
            content = file.read()
        content = bz2.decompress(content)
        return content.decode(self.DEFAULT_ENCODING, errors="ignore")

    def parse_file(self, page_file: str):
        url = self.decode_url(page_file)
        content = self.read(page_file)
        tree = html.fromstring(content)
        listing = [
            html.tostring(element, encoding="unicode")
            for element in tree.cssselect("#main-article > ul > li")
        ]

        results: List[Dict[str, Any]] = list()
        for entry in listing:
            trope, sentences = self.parse(entry)
            if len(sentences) > 0:
                has_spoiler = any([x[0] for x in sentences])
                results += [
                    {
                        "page": url,
                        "trope": trope,
                        "has_spoiler": has_spoiler,
                        "sentences": sentences,
                    }
                ]

        return results

    def parse_dir(self, directory: str) -> List[Dict[str, Any]]:
        listing = [
            os.path.join(directory, page_file) for page_file in os.listdir(directory)
        ]
        results: List[Dict[str, Any]] = list()

        for idx, page_file in enumerate(listing):
            try:
                self._track_message(
                    f"{idx+1}/{len(listing)} - {self.decode_url(page_file)}"
                )
                results += self.parse_file(page_file)
            except Exception as e:
                self._track_error(
                    f"Error for file: {page_file}:\n{getattr(e, 'message', repr(e))}"
                )

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
            .replace(".</span>", "</span>.")  # fix for spacy sentencizer
            .replace(
                """<span class="spoiler" title="you can set spoilers visible by default on your profile">""",
                "<s>",
            )
            .replace("""</span>""", "</s>")
        )

        sentences = self._split_into_sentences(data)
        data = "|".join(sentences)

        tagged_sentences = list()
        i, start = 0, 0
        status = SpoilerStatus.CLOSED
        while i < len(data):
            if data[i] == "<":
                if data[i + 1] == "/":
                    i = i + len("<s>")
                    status = SpoilerStatus.CLOSED_NOTUSED
                else:
                    i = i + len("</s>")
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

        def clean_output(sentence):
            return sentence.replace("<s>", "").replace("</s>", "").replace("|", "")

        x = (
            trope,
            [(tag, clean_output(sentence)) for tag, sentence in tagged_sentences],
        )
        return x
