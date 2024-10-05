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

    def read(self, _id: str) -> UserLink:
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
                WHERE id = %s
                """,
                (_id,),
            )
            row = cursor.fetchone()

            if row is not None:
                return UserLink(
                    row["id"],
                    row["user_id"],
                    row["name"],
                    row["link"],
                )

        raise KeyError(f"User Link with id '{_id}' not found.")

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
                row["id"],
                row["user_id"],
                row["name"],
                row["link"],
            )
