from dependency_injector.wiring import Provide, inject
from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug import Response

from intranet.core.user_details import Department, UserDetails, UserDetailsRepository
from intranet.core.user_link import UserLinksRepository
from intranet.error import login_required
from intranet.flask.dependable import Container

user_details = Blueprint("user_details", __name__, template_folder="../front/templates")


@user_details.get("/user-details")
@inject
@login_required
def user_details_page(
    details: UserDetailsRepository = Provide[Container.user_details_repository],
    links: UserLinksRepository = Provide[Container.user_link_repository],
) -> str:
    _user_details = details.read(session["user_id"])
    _user_links = [link for link in links if link.user_id == session["user_id"]]

    department_map = [
        (department.name, department.value)
        for department in Department
        if department.name != "no_department"
    ]

    return render_template(
        "user_details.html",
        user_details=_user_details,
        user_links=_user_links,
        departments=department_map,
    )


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
        department=Department[request.form.get("department", "")],
        email=request.form.get("email", ""),
        phone_number=request.form.get("phone_number", ""),
    )

    details.update(_details)

    return redirect(url_for("user_details.user_details_page"))
