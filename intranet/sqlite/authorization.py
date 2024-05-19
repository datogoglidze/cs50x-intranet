from dataclasses import dataclass

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from intranet.error import apology
from intranet.runner.factory import SqliteConnector


@dataclass
class AuthorizationSqliteRepository:
    username: str | None
    password: str | None

    def login(self) -> tuple[str, int] | None:  # type: ignore
        with SqliteConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = :username;",
                dict(username=self.username),
            )
            rows = cursor.fetchall()

            if len(rows) != 1 or not check_password_hash(
                rows[0]["hash"],
                self.password,  # type: ignore
            ):
                return apology("invalid username and/or password", 403)

            session["user_id"] = rows[0]["id"]
            session["username"] = rows[0]["username"]

    def register(self) -> tuple[str, int] | None:  # type: ignore
        with SqliteConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = :username;",
                dict(username=self.username),
            )

            password = generate_password_hash(
                self.password,  # type: ignore
                method="pbkdf2",
                salt_length=16,
            )

            cursor.execute(
                "INSERT INTO users (username, hash) VALUES(:username, :hash);",
                dict(username=self.username, hash=password),
            )

    def user_existence(self) -> int:
        with SqliteConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = :username;",
                dict(username=self.username),
            )
            return len(cursor.fetchall())
