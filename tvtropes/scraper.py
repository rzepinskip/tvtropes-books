import base64
import bz2
import datetime
import json
import os
from collections import OrderedDict
from time import sleep

import requests
from lxml import html

from .base_script import BaseScript


class TVTropesScraper(BaseScript):
    """Code adapted from https://github.com/raiben/made_recommender
    """

    MAIN_SEARCH = "https://tvtropes.org/pmwiki/pmwiki.php/Main/Literature"
    BASE_book_URL = "https://tvtropes.org/pmwiki/pmwiki.php/Literature/"
    BASE_MAIN_URL = "https://tvtropes.org/pmwiki/pmwiki.php/Main/"
    TARGET_RESULT_FILE_TEMPLATE = "books_tropes_{}.json"

    WAIT_TIME_BETWEEN_CALLS_IN_SECONDS = 0.5
    SESSION_DATETIME_FORMAT = "%Y%m%d_%H%M%S"

    MAIN_RESOURCE = "/Main/"
    book_RESOURCE = "/Literature/"
    LINK_SELECTOR = "a"
    LINK_SELECTOR_INSIDE_ARTICLE = "#main-article ul li a"
    LINK_ADDRESS_SELECTOR = "href"
    EXTENSION = ".html"
    COMPRESSED_EXTENSION = ".bz2"
    DEFAULT_ENCODING = "utf-8"

    def __init__(self, directory, session):
        parameters = dict(
            directory=directory,
            session=session,
            wait_time_between_calls_in_seconds=self.WAIT_TIME_BETWEEN_CALLS_IN_SECONDS,
        )
        BaseScript.__init__(self, parameters)

        self.directory_name = directory
        self.session = session
        self._set_default_session_value_if_empty()
        self._build_required_directories()

        self.books = None
        self.tropes = None
        self.urls = None
        self.tropes_by_book = OrderedDict()

    def _set_default_session_value_if_empty(self):
        if not self.session:
            now = datetime.datetime.now()
            self.session = now.strftime(self.SESSION_DATETIME_FORMAT)

    def _build_required_directories(self):
        whole_path = os.path.join(self.directory_name, self.session)
        if not os.path.isdir(whole_path):
            self._info(f"Building directory: {whole_path}")
            os.makedirs(whole_path)

    def run(self):
        self._extract_book_ids()
        self._extract_tropes()
        self._finish_and_summary()

    def _extract_book_ids(self):
        self.books = set()
        self.urls = set()
        main_url = self.MAIN_SEARCH
        category_ids = self._get_links_from_url(main_url, self.MAIN_RESOURCE)

        for category_id in category_ids:
            url = self.BASE_MAIN_URL + category_id
            book_ids = self._get_links_from_url(url, self.book_RESOURCE)
            self.books.update(book_ids)

        self._add_to_summary("n_books", len(self.books))

    def _extract_tropes(self):
        self.tropes = set()
        self.tropes_by_book = OrderedDict()
        sorted_books = sorted(list(self.books))

        self._info(f"Found {len(sorted_books)} books")

        for counter, book in enumerate(sorted_books):
            self._info(f"Status: {counter}/{len(sorted_books)} books")
            self._get_tropes_by_book(book)

        self._add_to_summary("n_tropes", len(self.tropes))
        self._add_to_summary("n_cached_urls", len(self.urls))

    def _get_tropes_by_book(self, book):
        url = self.BASE_book_URL + book
        trope_ids = self._get_links_from_url(url, self.MAIN_RESOURCE, only_article=True)

        self._info(f"book {book} ({len(trope_ids)} tropes): {trope_ids}")

        self.tropes.update(trope_ids)
        self.tropes_by_book[book] = sorted(trope_ids)

    def _get_links_from_url(self, url, link_type, only_article=False):
        page = self._get_content_from_url(url)
        tree = html.fromstring(page)
        selector = (
            self.LINK_SELECTOR_INSIDE_ARTICLE if only_article else self.LINK_SELECTOR
        )
        links = [
            element.get(self.LINK_ADDRESS_SELECTOR)
            for element in tree.cssselect(selector)
            if element.get(self.LINK_ADDRESS_SELECTOR)
        ]
        return [
            link.split("/")[-1]
            for link in links
            if link_type in link and "action" not in link
        ]

    def _get_content_from_url(self, url):
        self.urls.add(url)
        encoded_url = self._build_encoded_url(url)
        file_path = os.path.join(self.directory_name, self.session, encoded_url)

        if self._file_exists(file_path):
            self._info(f"Retrieving URL from cache: {url}")
            content = self._read_file(file_path)
            return self._read_content_safely(content)

        self._info(f"Retrieving URL from TVTropes and storing in cache: {url}")
        self._wait_between_calls_to_avoid_attacking()
        page = requests.get(url)
        content = page.content
        self._write_file(content, file_path)
        return self._read_content_safely(content)

    @classmethod
    def _file_exists(cls, file_path):
        compressed_path = f"{file_path}{cls.COMPRESSED_EXTENSION}"
        return os.path.isfile(compressed_path)

    @classmethod
    def _read_file(cls, file_path):
        compressed_path = f"{file_path}{cls.COMPRESSED_EXTENSION}"
        with open(compressed_path, "rb") as file:
            content = file.read()
        return bz2.decompress(content)

    def _write_file(self, content, file_path):
        compressed_path = f"{file_path}{self.COMPRESSED_EXTENSION}"
        self.compressed_content = bz2.compress(content)
        with open(compressed_path, "wb") as file:
            file.write(self.compressed_content)

        self._add_to_summary("compressed_generated_file_path", compressed_path)
        self._add_to_summary(
            "compressed_generated_file_size_bytes", len(self.compressed_content)
        )

    def _read_content_safely(self, content):
        return content.decode(self.DEFAULT_ENCODING, errors="ignore")

    def _build_encoded_url(self, url):
        encoded_url = (
            base64.urlsafe_b64encode(url.encode(self.DEFAULT_ENCODING)).decode(
                self.DEFAULT_ENCODING
            )
            + self.EXTENSION
        )
        return encoded_url

    def _wait_between_calls_to_avoid_attacking(self):
        sleep(self.WAIT_TIME_BETWEEN_CALLS_IN_SECONDS)
