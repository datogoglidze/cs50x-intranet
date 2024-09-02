from dataclasses import dataclass
from typing import Iterator

from intranet.core.news import News, NewsRepository
from intranet.mssql.connector import MsSqlConnector


@dataclass
class NewsMssqlRepository(NewsRepository):  # pragma: no cover
    def create(self, news: News) -> News:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO news (id, title, content)
                VALUES (%s, %s, %s)
                """,
                (news.id, news.title, news.content),
            )

            return news

    def read(self, news_id: str) -> News:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, title, content FROM news WHERE id = %s
                """,
                (news_id,),
            )
            row = cursor.fetchone()

            if row is not None:
                return News(row["title"], row["content"], row["id"])

        raise KeyError(f"News with id '{news_id}' not found.")

    def __iter__(self) -> Iterator[News]:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    position,
                    id,
                    title,
                    content
                FROM news
                ORDER BY position DESC
            """)
            rows = cursor.fetchall()

        for row in rows:
            yield News(row["title"], row["content"], row["id"])
