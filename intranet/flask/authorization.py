from flask import Blueprint, redirect, render_template, request, session

from intranet.error import apology
from intranet.sqlite.authorization import AuthorizationSqliteRepository

authorization = Blueprint(
    "authorization", __name__, template_folder="../front/templates"
)


@authorization.route("/login", methods=["GET", "POST"])
def login():  # type: ignore
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        AuthorizationSqliteRepository().login()

        return redirect("/")

    else:
        return render_template("login.html")


@authorization.route("/logout")  # type: ignore
def logout():
    session.clear()

    return redirect("/")


@authorization.route("/register", methods=["GET", "POST"])
def register():  # type: ignore
    session.clear()

    if request.method == "POST":
        AuthorizationSqliteRepository().register()

        session.clear()

        return redirect("/login")

    else:
        return render_template("register.html")
