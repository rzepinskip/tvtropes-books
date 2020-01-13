tvtropes
========

.. image:: https://img.shields.io/pypi/v/tvtropes.svg
    :target: https://pypi.python.org/pypi/tvtropes
    :alt: Latest PyPI version

.. image:: No.png
   :target: No
   :alt: Latest Travis CI build status

Scraper for Tv Tropes site

Usage
-----

1. Get all relevant HTMl documents::

    invoke scrape-tvtropes --cache-directory data/scraper/cache/ --session 20190502

2. Prase downloaded HTML documents::

    invoke parse-tvtropes --cache-directory data/scraper/cache/ --session 20190502


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
