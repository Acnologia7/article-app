"""
News scrapers for fetching articles from various news websites.
"""

from abc import abstractmethod
from dataclasses import dataclass
from typing import List
from http import HTTPStatus

import requests
from bs4 import BeautifulSoup


@dataclass
class Article:
    """Represents an article from a news server."""

    header: str
    url: str


class NewsScraper:
    @abstractmethod
    def get_headers(self) -> List[Article]:
        """Returns a list of articles from the news server."""
        pass


class IdnesScraper(NewsScraper):
    def get_headers(self) -> List[Article]:
        base_url = "https://www.idnes.cz/"
        response = requests.get(base_url)

        if response.status_code != HTTPStatus.OK:
            raise requests.RequestException(
                f"Failed to fetch {base_url}: {response.status_code}"
            )

        articles = []
        soup = BeautifulSoup(response.text, "html.parser")

        for article in soup.find_all("div", class_="art"):
            header_tag = article.find("h3")
            link_tag = article.find("a", class_="art-link")
            header = header_tag.text.strip()
            article_url = link_tag.get("href")

            if header and article_url:
                articles.append(Article(header=header, url=article_url))

        return articles


class IhnedScraper(NewsScraper):
    def get_headers(self) -> List[Article]:
        base_url = "https://www.ihned.cz/"
        response = requests.get(base_url)

        if response.status_code != HTTPStatus.OK:
            raise requests.RequestException(
                f"Failed to fetch {base_url}: {response.status_code}"
            )

        articles = []
        soup = BeautifulSoup(response.text, "html.parser")

        for article in soup.find_all("div", class_="article-box"):
            header_tag = article.find("h3", class_="article-title")
            link_tag = header_tag.find("a")
            header = link_tag.text.strip().replace("\xa0", " ")
            article_url = link_tag.get("href")

            if header and article_url:
                articles.append(Article(header=header, url=article_url))

        return articles


class BbcScraper(NewsScraper):
    def get_headers(self) -> List[Article]:
        base_url = "https://www.bbc.com"
        response = requests.get(base_url)

        if response.status_code != HTTPStatus.OK:
            raise requests.RequestException(
                f"Failed to fetch {base_url}: {response.status_code}"
            )

        articles = []
        soup = BeautifulSoup(response.text, "html.parser")

        article = soup.find("article")
        for section in article.find_all("section"):
            for a_tag in section.find_all("a"):
                article_url = f"{base_url}{a_tag.get("href")}"
                if "https://cloud.email.bbc.com" in article_url:
                    continue
                header_tag = a_tag.find("h2")
                header = header_tag.text.strip()

                if header and article_url:
                    articles.append(Article(header=header, url=article_url))

        return articles
