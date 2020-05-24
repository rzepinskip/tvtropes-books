import base64
import bz2
import os
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

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

        sentencizer = English()
        sentencizer.add_pipe(sentencizer.create_pipe("sentencizer"))
        self._sentencizer = sentencizer

        self._tagger = en_core_web_sm.load(disable=["parser", "ner"])

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

    def _is_valid_sentence(self, sentence: str) -> bool:
        tagged_sentence = self._tagger(sentence)

        for token in tagged_sentence:
            if token.pos_ == "VERB" or token.pos_ == "AUX":
                return True

        return False

    def _split_into_sentences(self, text: str) -> List[str]:
        doc = self._sentencizer(text)
        sentences = [sentence.string.strip() for sentence in doc.sents]
        return [sentence for sentence in sentences if len(sentence) > 0]

    def _tags_to_indices(
        self, sentence_words: List[str], word_tags: List[bool]
    ) -> List[Tuple[int, int]]:
        i = 0
        spoiler_start: Optional[int] = None
        indices: List[Tuple[int, int]] = list()
        for word_index, word_tag_pair in enumerate(zip(sentence_words, word_tags)):
            word, tag = word_tag_pair
            if tag is True and spoiler_start is None:
                spoiler_start = i
            elif tag is False and spoiler_start is not None:
                indices += [(spoiler_start, i - 1)]
                spoiler_start = None
            elif tag is True and word_index == len(word_tags) - 1:
                indices += [(spoiler_start, i + len(word))]
                spoiler_start = None

            i += len(word) + 1

        return indices

    def parse(
        self, raw_data: str
    ) -> Tuple[str, List[Tuple[bool, str, List[Tuple[int, int]]]]]:
        raw_data = Cleaner(kill_tags=["div"]).clean_html(raw_data)
        cleaned_data = self.before_cleaner.clean_html(f"<div>{raw_data}</div>")
        colon_idx = cleaned_data.find(":")
        trope = cleaned_data[:colon_idx].replace("<div>", "").strip()
        cleaned_data = cleaned_data[colon_idx + 1 :]
        data = (
            cleaned_data.replace("<div>", "")
            .replace("</div>", "")
            .replace("...", ".")
            .replace("◊", "")
            .replace(".</span>", "</span>.")  # fix for spacy sentencizer
            .replace(
                """<span class="spoiler" title="you can set spoilers visible by default on your profile">""",
                " <s> ",
            )
            .replace("""</span>""", " </s> ")
        )

        sentences = self._split_into_sentences(data)
        if len(sentences) == 0:
            return (trope, list())

        tagged_sentences = list()
        status = SpoilerStatus.CLOSED
        for sentence in sentences:
            words = [x.strip() for x in sentence.split()]
            word_tags: List[bool] = list()
            proper_words: List[str] = list()
            for word in words:
                if word == "</s>":
                    status = SpoilerStatus.CLOSED_NOTUSED
                elif word == "<s>":
                    status = SpoilerStatus.OPEN
                else:
                    proper_words += [word]
                    word_tags += [True if status == SpoilerStatus.OPEN else False]

            if status is SpoilerStatus.CLOSED:
                tag = False
            elif status is SpoilerStatus.OPEN:
                tag = True
            elif status is SpoilerStatus.CLOSED_NOTUSED:
                tag = True
                status = SpoilerStatus.CLOSED

            if len(proper_words) == 0:
                continue

            if proper_words[-1] == ".":
                proper_words = proper_words[:-1]
                proper_words[-1] = proper_words[-1] + "."
                word_tags = word_tags[:-1]

            sentence = " ".join(proper_words)

            if self._is_valid_sentence(sentence):
                spoiler_indices = self._tags_to_indices(proper_words, word_tags)
                tagged_sentences.append((tag, sentence, spoiler_indices))

        return (trope, tagged_sentences)
