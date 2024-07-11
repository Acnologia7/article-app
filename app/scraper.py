"""
Web scraping service for fetching and saving news articles.
"""

import logging
from time import sleep

try:
    from app.news import IdnesScraper, IhnedScraper, BbcScraper
    from app.service import save_articles_if_new
except ImportError:
    from news import IdnesScraper, IhnedScraper, BbcScraper
    from service import save_articles_if_new

logger = logging.getLogger(__name__)
SCRAPERS = [IdnesScraper(), IhnedScraper(), BbcScraper()]


def scrape_news():
    """Fetches articles from news servers and saves new ones into our DB.
    Logs errors for each scraper but continues operation.
    """
    for scraper in SCRAPERS:
        try:
            logger.info(f"Scraping news using {type(scraper).__name__}")
            articles = scraper.get_headers()
            save_articles_if_new(articles)

        except Exception as e:
            logger.error(
                f"An error occurred in Scraper {type(scraper).__name__}: {str(e)}"
            )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="{asctime} {levelname:<8} {name}:{module}:{lineno} - {message}",
        style="{",
    )
    while True:
        try:
            scrape_news()

        except Exception as e:
            logger.error(f"Unhandled exception in main loop: {str(e)}")

        finally:
            sleep(60)
