from dataclasses import dataclass
from typing import Iterator

from intranet.core.user_link import UserLink, UserLinksRepository
from intranet.mssql.connector import MsSqlConnector


@dataclass
class UserLinksMssqlRepository(UserLinksRepository):  # pragma: no cover
    def create(self, user_link: UserLink) -> UserLink:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO user_links (
                    id,
                    user_id,
                    name,
                    link
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    user_link.id,
                    user_link.user_id,
                    user_link.name,
                    user_link.link,
                ),
            )

            return user_link

    def delete(self, _id: str) -> None:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                DELETE FROM user_links
                WHERE id = %s
                """,
                (_id,),
            )

    def __iter__(self) -> Iterator[UserLink]:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    name,
                    link
                FROM user_links
                """
            )
            rows = cursor.fetchall()

        for row in rows:
            yield UserLink(
                id=row["id"],
                user_id=row["user_id"],
                name=row["name"],
                link=row["link"],
            )
