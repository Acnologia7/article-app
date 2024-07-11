"""
Service layer for handling articles.
"""

import logging
from typing import List
from sqlalchemy import or_, exc
from sqlalchemy.dialects.postgresql import insert

try:
    from app.model import Article
    from app import db
except ImportError:
    import db
    from model import Article

logger = logging.getLogger(__name__)


def get_articles_with_keywords(keywords: List[str]) -> List[Article]:
    """
    Retrieves articles from the database where at least one of the given keywords is found in the article's header.
    Articles are returned in descending order of creation date.
    Returns an empty list if no keywords are provided.
    """
    keyword_filters = [Article.header.ilike(f"%{keyword}%") for keyword in keywords]
    try:
        if keywords:
            articles = db.session.query(Article).filter(or_(*keyword_filters)).all()
        else:
            articles = []
        return articles

    except exc.OperationalError:
        logger.error("Database is not reachable")
        raise

    finally:
        db.session.close()


def save_articles_if_new(articles: List[Article]) -> None:
    """Saves articles to the database if they do not already exist (checked by URL)."""
    try:
        for article in articles:
            insert_stmt = insert(Article).values(header=article.header, url=article.url)
            on_conflict_stmt = insert_stmt.on_conflict_do_nothing(
                index_elements=["url"]
            )
            db.session.execute(on_conflict_stmt)
        db.session.commit()

    except Exception as e:
        logger.error(f"Error occurred while inserting data: {e}")
        db.session.rollback()
        raise

    finally:
        db.session.close()
