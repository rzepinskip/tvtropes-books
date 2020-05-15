import json
import os

from invoke import task

from tvtropes.parser import SpoilerParser
from tvtropes.scraper import TVTropesScraper


@task
def scrape_tvtropes(context, cache_directory=None, session=None):
    """
    Scrape tropes by film in TvTropes.org
    :param cache_directory: The folder that all the downloaded pages are going to be written into.
    :param session: (Optional) Name of the cache folder. If not provided, then it will use the current date/time.
    """
    if cache_directory is None:
        raise ValueError("Please, add the missing parameters!!")

    TVTropesScraper.set_logger_file_id("scrape_tvtropes", session)
    scraper = TVTropesScraper(directory=cache_directory, session=session)
    scraper.run()


@task
def parse_tvtropes(context, cache_directory=None, session=None, output_file=None):
    if cache_directory is None or session is None or output_file is None:
        raise ValueError("Please, add the missing parameters!!")

    SpoilerParser.set_logger_file_id("parse_tvtropes", session)
    directory = os.path.join(cache_directory, session)
    data = SpoilerParser().parse_dir(directory)
    with open(output_file, "w") as f:
        f.write("\n".join([json.dumps(line) for line in data]))
