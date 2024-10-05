from uuid import uuid4

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug import Response
from werkzeug.security import check_password_hash, generate_password_hash

from intranet.core.user import User, UserRepository
from intranet.core.user_details import Department, UserDetails, UserDetailsRepository
from intranet.error import apology
from intranet.flask.dependable import Container

authorization = Blueprint(
    "authorization", __name__, template_folder="../front/templates"
)


@authorization.get("/login")
def login_page() -> str:
    session.clear()

    return render_template("login.html")


@authorization.get("/register")
def register_page() -> str:
    session.clear()

    return render_template("register.html")


@authorization.post("/login")
@inject
def login(
    users: UserRepository = Provide[Container.user_repository],
) -> Response | tuple[str, int]:
    session.clear()

    user = User(
        id=str(uuid4()),
        username=request.form.get("username", "").lower(),
        password=request.form.get("password", ""),
    )

    if not user.username:
        return apology("must provide username", 403)

    if not user.password:
        return apology("must provide password", 403)

    for existing in users:
        if user.username == existing.username and check_password_hash(
            existing.password, user.password
        ):
            session["user_id"] = existing.id
            session["username"] = existing.username

            return redirect(url_for("news.read_news"))

    return apology("invalid username and/or password", 403)


@authorization.get("/logout")
def logout() -> Response:
    session.clear()

    return redirect(url_for("authorization.login_page"))


@authorization.post("/register")
@inject
def register(
    users: UserRepository = Provide[Container.user_repository],
    details: UserDetailsRepository = Provide[Container.user_details_repository],
) -> Response | tuple[str, int]:
    session.clear()

    user = User(
        id=str(uuid4()),
        username=request.form.get("username", "").lower(),
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
            User(
                id=user.id,
                username=user.username,
                password=generate_password_hash(
                    user.password,
                    method="pbkdf2",
                    salt_length=16,
                ),
            )
        )
    except ValueError:
        return apology("username already exists", 403)

    details.create(
        UserDetails(
            id=user.id,
            department=Department["no_department"],
            first_name="",
            last_name="",
            birth_date="",
            email="",
            phone_number="",
        )
    )

    session.clear()

    return redirect(url_for("authorization.login_page"))
