from invoke import task
from tvtropes.scraper import TVTropesScraper
from tvtropes.parser import SpoilerParser
import os
import json


@task
def scrape_tvtropes(context, cache_directory=None, session=None):
    """
    Scrape tropes by film in TvTropes.org
    :param cache_directory: The folder that all the downloaded pages are going to be written into.
    :param session: (Optional) Name of the cache folder. If not provided, then it will use the current date/time.
    """
    if cache_directory is None:
        print("Please, add the missing parameters!!")

    TVTropesScraper.set_logger_file_id("scrape_tvtropes", session)
    scraper = TVTropesScraper(directory=cache_directory, session=session)
    scraper.run()


@task
def parse_tvtropes(context, cache_directory=None, session=None, output_file=None):
    if cache_directory is None or session is None or output_file is None:
        print("Please, add the missing parameters!!")

    SpoilerParser.set_logger_file_id("parse_tvtropes", session)
    dir = os.path.join(cache_directory, session)
    data = SpoilerParser().parse_dir(dir)
    with open(output_file, "w") as f:
        f.write(json.dumps(data, indent=4))

