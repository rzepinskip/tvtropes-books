tvtropes
========

Scraper for TV Tropes site to download all tropes related to books (and their spoiler annotations).

Usage
-----

1. Get all relevant HTML documents::

    invoke scrape-tvtropes --cache-directory data/scraper/cache/ --session 20190502

2. Prase downloaded HTML documents::

    invoke parse-tvtropes --cache-directory data/scraper/cache/ --session 20190502 --output-file output.jsonl

Requirements
^^^^^^^^^^^^

1. Python 3.7
2. Python packages as specified in `requirements.txt`
