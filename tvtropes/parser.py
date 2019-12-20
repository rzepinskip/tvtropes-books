from enum import Enum
from lxml import html, etree
from lxml.html.clean import Cleaner
from typing import List, Tuple
import re


class SpoilerStatus(Enum):
    OPEN = 1
    CLOSED_NOTUSED = 2
    CLOSED = 4


class SpoilerParser:
    def __init__(self):
        self.before_cleaner = Cleaner(
            allow_tags=["span", "div"], remove_unknown_tags=False
        )

    def _clean(self, raw_data):
        cleaned_data = self.before_cleaner.clean_html(f"<div>{raw_data}</div>")
        colon_idx = cleaned_data.find(":")
        cleaned_data = cleaned_data[colon_idx + 1 :]
        data = cleaned_data.replace("</div>", "").strip()
        data = data.replace(".</span>", "</span>.")

        return data

    def parse(self, raw_data: str) -> List[Tuple[bool, str]]:
        data = self._clean(raw_data)

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

            if data[i] in [".", "?", "!"] or i == len(data) - 1:
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
            return re.sub("\s\s+", " ", str_repr).strip()

        return [(tag, clean_all(sentence)) for tag, sentence in tagged_sentences]
