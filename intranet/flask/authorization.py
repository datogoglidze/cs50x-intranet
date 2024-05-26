from uuid import uuid4

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, current_app, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from intranet.core.user import User, UserRepository
from intranet.error import apology
from intranet.flask.dependable import Container

authorization = Blueprint(
    "authorization", __name__, template_folder="../front/templates"
)


@authorization.route("/login", methods=["GET", "POST"])
@inject
def login(users: UserRepository = Provide[Container.user_repository]):  # type: ignore
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

        try:
            existing_user = users.read(user.username)
        except KeyError:
            return apology("invalid username and/or password", 403)

        if not check_password_hash(
            existing_user.password,
            user.password,
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = existing_user.id
        session["username"] = existing_user.username

        return redirect("/")

    else:
        return render_template("login.html")


@authorization.route("/logout")  # type: ignore
def logout():
    session.clear()

    return redirect("/")


@authorization.route("/register", methods=["GET", "POST"])
@inject
def register(users: UserRepository = Provide[Container.user_repository]):  # type: ignore
    session.clear()

    current_app.logger.debug(f"users: {users}")

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

        if user.password != request.form.get("confirmation", ""):
            return apology("password didn't match", 403)

        try:
            users.create(
                {
                    "username": user.username,
                    "password": (
                        generate_password_hash(
                            user.password,
                            method="pbkdf2",
                            salt_length=16,
                        )
                    ),
                }
            )
        except ValueError:
            pass

        session.clear()

        return redirect("/login")

    else:
        return render_template("register.html")
