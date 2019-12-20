from lxml import html, etree
from enum import Enum
import spacy
from lxml.html.clean import Cleaner
import en_core_web_sm
import re


class TAG(Enum):
    NONSPOILER = 0
    SPOILER = 1


class SpoilerParser:
    def __init__(self):
        self._nlp = en_core_web_sm.load()

    def parse(self, el):
        paragraph_text = etree.tostring(el, method="text", encoding="unicode")
        print(f"{paragraph_text[:15]}...{paragraph_text[-10:]}")
        if el.find("ul") is not None:
            childs = el.xpath("//li/ul/li")
            return [] + [self._parse_single(x) for x in childs]
        else:
            return [self._parse_single(el)]

    def _parse_single(self, el):
        etree.strip_tags(el, *["a", "em", "small", "img", "strong"])
        spoilers = el.xpath("span[@class]/text()")
        paragraph_text = etree.tostring(el, method="text", encoding="unicode")

        colon_idx = paragraph_text[:50].find(":")
        if colon_idx != -1:
            paragraph_text = paragraph_text[colon_idx + 1 :]
        paragraph_text = re.sub("\s\s+", " ", paragraph_text).strip()
        # print(etree.tostring(el))
        # print(paragraph_text)

        spoilers_indexes = list()
        for spoiler in spoilers:
            start = paragraph_text.find(spoiler)
            print(f"{start}: {spoiler}")
            end = start + len(spoiler)
            spoilers_indexes.append((start, end))

        def is_overlapping(x1, x2, y1, y2):
            return max(x1, y1) <= min(x2, y2)

        doc = self._nlp(paragraph_text)
        sentences = [str(x) for x in doc.sents]

        # print(spoilers_indexes)
        results = list()
        for sentence in sentences:
            sentence_start = paragraph_text.find(sentence)
            sentence_end = sentence_start + len(sentence)
            spoiler_found = False
            # print(f"{sentence_start}, {sentence_end}")
            for start, end in spoilers_indexes:
                if is_overlapping(sentence_start, sentence_end - 1, start, end - 1):
                    spoiler_found = True
                    break
            if spoiler_found:
                results.append((TAG.SPOILER, sentence))
            else:
                results.append((TAG.NONSPOILER, sentence))
        # print("-------------------------------")
        return results


# <li> <a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/StuffedIntoTheFridge" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/StuffedIntoTheFridge">Stuffed into the Fridge</a>: The between chapters scene right before Mirri's Tale all but says outright that <span class="spoiler" title="you can set spoilers visible by default on your profile">Mirri had to die in order for Gerrard to "shed" her and become a hero</span>, so not only playing this trope as straight as possible but even <em>referencing it in-universe</em>.</li>
example = """
<li> <a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/TheStinger" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/TheStinger">The Stinger</a>: The very last pages recount the literary example of one, with the only librarian reading the scene depicted on the card <a class="urllink" href="http://gatherer.wizards.com/Pages/Card/Details.aspx?printed=true&amp;multiverseid=6076">Mind Over Matter<img src="https://static.tvtropes.org/pmwiki/pub/external_link.gif" style="border:none;" width="12" height="12"></a> (which was <a class="twikilink" href="https://tvtropes.org/pmwiki/pmwiki.php/Main/TheStinger" title="https://tvtropes.org/pmwiki/pmwiki.php/Main/TheStinger">The Stinger</a> for the card set too) where Lyna is shown observing the Weatherlight's escape with <span class="spoiler" title="you can set spoilers visible by default on your profile">Urza</span>. This was a <em>huge</em> deal at the time, as <span class="spoiler" title="you can set spoilers visible by default on your profile">Urza</span> had hitherto been a prerevisionist character that was almost a complete cipher. He would go on to become arguably <strong>the</strong> main character of the Weatherlight Saga.</li>
"""
from lxml import html

tree = html.fromstring(example)
parser = SpoilerParser()
[parser.parse(element) for element in tree.cssselect("li")]
parser.parse(tree)
