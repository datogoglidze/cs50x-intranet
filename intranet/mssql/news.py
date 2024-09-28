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
                INSERT INTO news (
                    id,
                    creation_date,
                    title,
                    content,
                    status
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    news.id,
                    news.creation_date,
                    news.title,
                    news.content,
                    news.status,
                ),
            )

            return news

    def read(self, news_id: str) -> News:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    id,
                    creation_date,
                    title,
                    content,
                    status
                FROM news
                WHERE id = %s
                """,
                (news_id,),
            )
            row = cursor.fetchone()

            if row is not None:
                return News(
                    row["id"],
                    row["creation_date"],
                    row["title"],
                    row["content"],
                    row["status"],
                )

        raise KeyError(f"News with id '{news_id}' not found.")

    def __iter__(self) -> Iterator[News]:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    id,
                    creation_date,
                    title,
                    content,
                    status
                FROM news
                ORDER BY creation_date DESC
            """)
            rows = cursor.fetchall()

        for row in rows:
            yield News(
                row["id"],
                row["creation_date"],
                row["title"],
                row["content"],
                row["status"],
            )

    def delete(self, news_id: str) -> None:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                DELETE FROM news
                WHERE id = %s
                """,
                (news_id,),
            )
