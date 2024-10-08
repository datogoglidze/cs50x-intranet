from uuid import uuid4

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, redirect, request, session, url_for
from werkzeug import Response

from intranet.core.user_link import UserLink, UserLinksRepository
from intranet.error import login_required
from intranet.flask.dependable import Container

user_links = Blueprint("user_links", __name__)


@user_links.post("/user-links")
@inject
@login_required
def create_user_link(
    links: UserLinksRepository = Provide[Container.user_link_repository],
) -> Response | tuple[str, int]:
    link = UserLink(
        id=str(uuid4()),
        user_id=session["user_id"],
        name=request.form.get("social_name", ""),
        link=request.form.get("social_link", ""),
    )

    links.create(link)

    return redirect(url_for("user_details.user_details_page"))


@user_links.post("/delete-link")
@inject
@login_required
def delete_user_link(
    links: UserLinksRepository = Provide[Container.user_link_repository],
) -> Response | tuple[str, int]:
    links.delete(request.form.get("link_id", ""))

    return redirect(url_for("user_details.user_details_page"))
