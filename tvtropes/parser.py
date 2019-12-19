from lxml import html, etree
from enum import Enum
import spacy
from lxml.html.clean import Cleaner


class TAG(Enum):
    NONSPOILER = 0
    SPOILER = 1


def parse(el):
    paragraph_text = etree.tostring(el, method="text", encoding="unicode")
    if el.find("ul") is not None:
        childs = el.xpath("//li/ul/li")
        return [] + [parse_single(x) for x in childs]
    else:
        return [parse_single(el)]


def parse_single(el):
    etree.strip_tags(el, *["a", "em"])
    spoilers = el.xpath("span[@class]/text()")
    paragraph_text = etree.tostring(el, method="text", encoding="unicode")

    print(etree.tostring(el))
    print(paragraph_text)

    spoilers_indexes = list()
    for spoiler in spoilers:
        start = paragraph_text.find(spoiler)
        print(f"{start}: {spoiler}")
        end = start + len(spoiler)
        spoilers_indexes.append((start, end))

    def is_overlapping(x1, x2, y1, y2):
        return max(x1, y1) <= min(x2, y2)

    nlp = en_core_web_sm.load()
    doc = nlp(paragraph_text)
    sentences = [str(x) for x in doc.sents]

    print(spoilers_indexes)
    results = list()
    for sentence in sentences:
        sentence_start = paragraph_text.find(sentence)
        sentence_end = sentence_start + len(sentence)
        spoiler_found = False
        print(f"{sentence_start}, {sentence_end}")
        for start, end in spoilers_indexes:
            if is_overlapping(sentence_start, sentence_end - 1, start, end - 1):
                spoiler_found = True
                break
        if spoiler_found:
            results.append((TAG.SPOILER, sentence))
        else:
            results.append((TAG.NONSPOILER, sentence))
    print("-------------------------------")
    return results


example = (
    """<li> <a class="twikilink" href="x" title="x">Contrived Coincidence</a>: Some sentence:
<ul>
    <li> <span class="spoiler" title="x">Had the climax not
            occurred on a night with a full moon. This is especially funny when it's revealed, <a class="twikilink"
            title="x">three books later</a>, that Voldemort cursed it.</span> New sentence. 
            <span class="spoiler" title="x">New spoiler</span></li>
    <li> <span class="spoiler" title="x">The only reason that
            Sirius even breaks out of Azkaban in the first place is that: (A) the Weasleys win the wizard lottery;
            (B) this is apparently front-page news; (C) Ron has Scabbers in the picture; and (D) Cornelius Fudge
            just happens to be carrying that exact issue of the <em>Daily Prophet</em> when he visits Black's
            cell.</span></li>
    <li> Harry just happens to get his hands on the Marauder's Map the 
    very same year that one of its creators is teaching at Hogwarts. 
    <span class="spoiler" title="x">The other three were his own departed
    father, Ron's rat, and lastly, the eponymous prisoner of Azkaban.</span></li>
    </ul>
</li>""",
)
tree = etree.XML(example[0])
# childs = tree.xpath("//li/ul/li")
# [etree.tostring(el, method="text", encoding="unicode") for el in childs]
# [x.xpath("span[@class]/text()") for x in childs[:1]]
parse(tree)
first = childs[0]
first.findall("span")
[etree.tostring(x, method="text", encoding="unicode") for x in first.findall("span")]

