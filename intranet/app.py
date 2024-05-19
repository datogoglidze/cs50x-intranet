import sqlite3
from dataclasses import dataclass
from sqlite3 import Connection
from typing import ContextManager

from flask import Blueprint, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from intranet.error import apology, login_required

intranet_page = Blueprint("intranet", __name__, template_folder="templates")


@dataclass
class SqliteConnector:
    dsn: str = "database/database.db"

    def connect(self) -> ContextManager[Connection]:
        connection = sqlite3.connect(self.dsn)
        connection.row_factory = sqlite3.Row

        return connection


@intranet_page.after_request
def after_request(response):  # type: ignore
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@intranet_page.route("/")
@login_required  # type: ignore
def index() -> str:
    return render_template("index.html")


@intranet_page.route("/login", methods=["GET", "POST"])
def login():  # type: ignore
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

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

        return redirect("/")

    else:
        return render_template("login.html")


@intranet_page.route("/logout")  # type: ignore
def logout():
    session.clear()

    return redirect("/")


@intranet_page.route("/register", methods=["GET", "POST"])
def register():  # type: ignore
    session.clear()

    if request.method == "POST":
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

        session.clear()

        return redirect("/login")

    else:
        return render_template("register.html")
