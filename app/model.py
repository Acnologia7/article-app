"""
ORM definitions.
"""

from datetime import datetime

from sqlalchemy import Column, String, Integer, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Article(Base):
    __tablename__ = "article"

    id: int = Column(Integer, primary_key=True)
    header: str = Column(String, nullable=False, index=True)
    url: str = Column(
        String, unique=True, nullable=False, index=True
    )  # added unique check on db level for peformance aproach
    timestamp: datetime = Column(
        TIMESTAMP(timezone=True), nullable=False, default=func.now(), index=True
    )

    def __str__(self):
        return f"Article(id={self.id}, header={self.header}, url={self.url})"
