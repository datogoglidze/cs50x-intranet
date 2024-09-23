from dependency_injector.wiring import Provide, inject
from flask import Blueprint, redirect, render_template, request, session
from werkzeug import Response

from intranet.core.user_details import UserDetails, UserDetailsRepository
from intranet.error import login_required
from intranet.flask.dependable import Container

user_details = Blueprint("user_details", __name__, template_folder="../front/templates")


@user_details.get("/user-details")
@inject
@login_required
def user_details_page(
    details: UserDetailsRepository = Provide[Container.user_details_repository],
) -> str:
    _user_details = details.read(session["user_id"])

    return render_template("user_details.html", user_details=_user_details)


@user_details.post("/user-details")
@inject
@login_required
def create_user_details(
    details: UserDetailsRepository = Provide[Container.user_details_repository],
) -> Response | tuple[str, int]:
    _details = UserDetails(
        id=session["user_id"],
        first_name=request.form.get("first_name", ""),
        last_name=request.form.get("last_name", ""),
        birth_date=request.form.get("birth_date", ""),
        department=request.form.get("department", ""),
        email=request.form.get("email", ""),
        phone_number=request.form.get("phone_number", ""),
    )

    details.update(_details)

    return redirect("/user-details")
