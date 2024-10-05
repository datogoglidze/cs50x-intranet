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
                    title,
                    content
                )
                VALUES (%s, %s, %s)
                """,
                (
                    news.id,
                    news.title,
                    news.content,
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
                    content
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
                )

        raise KeyError(f"News with id '{news_id}' not found.")

    def __iter__(self) -> Iterator[News]:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    id,
                    FORMAT(
                        creation_date, 'yyyy/MM/dd'
                    ) AS formatted_creation_date,
                    title,
                    content,
                    creation_date
                FROM news
                ORDER BY creation_date DESC
            """)
            rows = cursor.fetchall()

        for row in rows:
            yield News(
                id=row["id"],
                creation_date=row["formatted_creation_date"],
                title=row["title"],
                content=row["content"],
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
