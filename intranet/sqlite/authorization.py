from dataclasses import dataclass

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from intranet.core.user import User
from intranet.error import apology
from intranet.runner.factory import SqliteConnector


@dataclass
class AuthorizationSqliteRepository:
    user: User

    def login(self) -> tuple[str, int] | None:  # type: ignore
        with SqliteConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = :username;",
                dict(username=self.user.username),
            )
            raw = cursor.fetchone()

            if not raw or not check_password_hash(
                raw["hash"],
                self.user.password,  # type: ignore
            ):
                return apology("invalid username and/or password", 403)

            session["user_id"] = raw["id"]
            session["username"] = raw["username"]

    def register(self) -> tuple[str, int] | None:  # type: ignore
        with SqliteConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = :username;",
                dict(username=self.user.username),
            )

            password = generate_password_hash(
                self.user.password,  # type: ignore
                method="pbkdf2",
                salt_length=16,
            )

            cursor.execute(
                "INSERT INTO users (username, hash) VALUES(:username, :hash);",
                dict(username=self.user.username, hash=password),
            )

    def user_existence(self) -> int:
        with SqliteConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = :username;",
                dict(username=self.user.username),
            )
            return len(cursor.fetchall())
