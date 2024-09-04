from dataclasses import dataclass
from typing import Iterator

from intranet.core.user import User, UserRepository
from intranet.mssql.connector import MsSqlConnector


@dataclass
class UserMssqlRepository(UserRepository):  # pragma: no cover
    def create(self, user: User) -> User:
        self._ensure_does_not_exist(user.username)

        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO users (
                    id,
                    username,
                    password)
                VALUES (%s, %s, %s)
                """,
                (
                    user.id,
                    user.username,
                    user.password,
                ),
            )

            return user

    def _ensure_does_not_exist(self, username: str) -> None:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    id,
                    username,
                    password
                FROM users
                WHERE username = %s
                """,
                (username,),
            )

            if cursor.fetchone() is not None:
                raise ValueError(f"User with username '{username}' already exists.")

    def read(self, user_id: str) -> User:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    id,
                    username,
                    password
                FROM users
                WHERE id = %s
                """,
                (user_id,),
            )
            row = cursor.fetchone()

            if row is not None:
                return User(
                    row["username"],
                    row["password"],
                    row["id"],
                )

        raise KeyError(f"User with id '{user_id}' not found.")

    def __iter__(self) -> Iterator[User]:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    id,
                    username,
                    password
                FROM users
            """)
            rows = cursor.fetchall()

        for row in rows:
            yield User(
                row["username"],
                row["password"],
                row["id"],
            )
