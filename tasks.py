from invoke import task
from tvtropes.scraper import TVTropesScraper


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

