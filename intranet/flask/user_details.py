
from dependency_injector.wiring import Provide, inject
from flask import Blueprint, render_template, session

from intranet.core.user_details import UserDetailsRepository
from intranet.error import login_required
from intranet.flask.dependable import Container

user_details = Blueprint("user_details", __name__, template_folder="../front/templates")


@user_details.get("/user-details")
@inject
@login_required  # type: ignore
def user_details_page(
    details: UserDetailsRepository = Provide[Container.user_details_repository],
):  # type: ignore
    _user_details = details.read(session["user_id"])

    return render_template("user_details.html", user_details=_user_details)
