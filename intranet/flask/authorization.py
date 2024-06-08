from uuid import uuid4

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from intranet.core.user import User, UserRepository
from intranet.core.user_details import UserDetailsRepository
from intranet.error import apology
from intranet.flask.dependable import Container

authorization = Blueprint(
    "authorization", __name__, template_folder="../front/templates"
)


@authorization.get("/login")
def login_page():  # type: ignore
    session.clear()

    return render_template("login.html")


@authorization.get("/register")
def register_page():  # type: ignore
    session.clear()

    return render_template("register.html")


@authorization.post("/login")
@inject
def login(users: UserRepository = Provide[Container.user_repository]):  # type: ignore
    session.clear()

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


@authorization.get("/logout")  # type: ignore
def logout():
    session.clear()

    return redirect("/")


@authorization.post("/register")
@inject
def register(
    users: UserRepository = Provide[Container.user_repository],
    details: UserDetailsRepository = Provide[Container.user_details_repository],
):  # type: ignore
    session.clear()

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
        return apology("username already exists", 403)

    details.create({"id": users.read(user.username).id})

    session.clear()

    return redirect("/login")
