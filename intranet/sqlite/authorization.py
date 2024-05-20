from dataclasses import dataclass
from typing import Any

from werkzeug.security import generate_password_hash

from intranet.core.user import User
from intranet.runner.factory import SqliteConnector

SELECT = """SELECT * FROM users WHERE username = :username;"""
INSERT = """INSERT INTO users (username, hash) VALUES(:username, :hash);"""


@dataclass
class AuthorizationSqliteRepository:
    user: User

    def login(self) -> Any:
        with SqliteConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                SELECT,
                dict(username=self.user.username),
            )

            return cursor.fetchone()

    def register(self) -> tuple[str, int] | None:  # type: ignore
        with SqliteConnector().connect() as connection:
            password = generate_password_hash(
                self.user.password,
                method="pbkdf2",
                salt_length=16,
            )
            cursor = connection.cursor()
            cursor.execute(
                INSERT,
                dict(username=self.user.username, hash=password),
            )

    def user_existence(self) -> Any:
        with SqliteConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                SELECT,
                dict(username=self.user.username),
            )
            return cursor.fetchone()
