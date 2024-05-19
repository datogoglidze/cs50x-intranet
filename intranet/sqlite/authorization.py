from dataclasses import dataclass

from flask import request, session
from werkzeug.security import check_password_hash, generate_password_hash

from intranet.error import apology
from intranet.runner.factory import SqliteConnector


@dataclass
class AuthorizationSqliteRepository:
    def login(self) -> tuple[str, int] | None:  # type: ignore
        with SqliteConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = :username;",
                dict(username=request.form.get("username")),
            )
            rows = cursor.fetchall()

            if len(rows) != 1 or not check_password_hash(
                rows[0]["hash"],
                request.form.get("password"),  # type: ignore
            ):
                return apology("invalid username and/or password", 403)

            session["user_id"] = rows[0]["id"]
            session["username"] = rows[0]["username"]

    def register(self) -> tuple[str, int] | None:  # type: ignore
        with SqliteConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = :username;",
                dict(username=request.form.get("username")),
            )
            rows = cursor.fetchall()

            if not request.form.get("username"):
                return apology("must provide username", 400)
            elif len(rows) != 0:
                return apology("username already exists", 400)
            elif not request.form.get("password"):
                return apology("must provide password", 400)
            elif request.form.get("password") != request.form.get("confirmation"):
                return apology("password didn't match", 400)

            password = generate_password_hash(
                str(request.form.get("password")),
                method="pbkdf2",
                salt_length=16,
            )

            cursor.execute(
                "INSERT INTO users (username, hash) VALUES(:username, :hash);",
                dict(username=request.form.get("username"), hash=password),
            )
