from uuid import uuid4

from flask import Blueprint, redirect, render_template, request, session
from werkzeug.security import check_password_hash

from intranet.core.user import User
from intranet.error import apology
from intranet.sqlite.authorization import AuthorizationSqliteRepository

authorization = Blueprint(
    "authorization", __name__, template_folder="../front/templates"
)


@authorization.route("/login", methods=["GET", "POST"])
def login():  # type: ignore
    session.clear()

    if request.method == "POST":
        user = User(
            id=str(uuid4()),
            username=request.form.get("username", ""),
            password=request.form.get("password", ""),
        )

        if not user.username:
            return apology("must provide username", 403)

        if not user.password:
            return apology("must provide password", 403)

        authorize = AuthorizationSqliteRepository(user).login()

        if not authorize:
            return apology("invalid username and/or password", 403)

        if not check_password_hash(
            dict(authorize)["password_hash"],
            user.password,
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = dict(authorize)["id"]
        session["username"] = dict(authorize)["username"]

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
        user = User(
            id=str(uuid4()),
            username=request.form.get("username", ""),
            password=request.form.get("password", ""),
        )

        if AuthorizationSqliteRepository(user).user_existence():
            return apology("username already exists", 400)

        if not user.username:
            return apology("must provide username", 403)

        if not user.password:
            return apology("must provide password", 403)

        if user.password != request.form.get("confirmation", ""):
            return apology("password didn't match", 403)

        AuthorizationSqliteRepository(user).register()

        session.clear()

        return redirect("/login")

    else:
        return render_template("register.html")
