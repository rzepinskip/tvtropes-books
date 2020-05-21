tvtropes
========

Scraper for Tv Tropes site

Usage
-----

1. Get all relevant HTMl documents::

    invoke scrape-tvtropes --cache-directory data/scraper/cache/ --session 20190502

2. Prase downloaded HTML documents::

    invoke parse-tvtropes --cache-directory data/scraper/cache/ --session 20190502 --output-file output.jsonl


Installation
------------

Requirements
^^^^^^^^^^^^

Compatibility
-------------

Licence
-------

Authors
-------

`tvtropes` was written by `Paweł Rzepiński < >`_.
