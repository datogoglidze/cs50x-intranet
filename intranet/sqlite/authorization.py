from dataclasses import dataclass
from typing import Any

from werkzeug.security import generate_password_hash

from intranet.core.user import User
from intranet.runner.factory import SqliteConnector

SELECT = """
    SELECT
        *
    FROM users
    WHERE username = :username;
"""

INSERT = """
    INSERT INTO users (
        id,
        username,
        password_hash
    ) VALUES (
        :id, :username, :password_hash
    );
"""


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
            password_hash = generate_password_hash(
                self.user.password,
                method="pbkdf2",
                salt_length=16,
            )
            cursor = connection.cursor()
            cursor.execute(
                INSERT,
                dict(
                    id=self.user.id,
                    username=self.user.username,
                    password_hash=password_hash,
                ),
            )

    def user_existence(self) -> Any:
        with SqliteConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                SELECT,
                dict(username=self.user.username),
            )
            return cursor.fetchone()
