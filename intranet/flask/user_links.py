from uuid import uuid4

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, redirect, request, session, url_for
from werkzeug import Response

from intranet.core.user_link import UserLink, UserLinksRepository
from intranet.error import login_required
from intranet.flask.dependable import Container

user_links = Blueprint("user_links", __name__, template_folder="../front/templates")


@user_links.post("/user_links")
@inject
@login_required
def create_user_links(
    links: UserLinksRepository = Provide[Container.user_links_repository],
) -> Response | tuple[str, int]:
    link = UserLink(
        id=str(uuid4()),
        user_id=session["user_id"],
        name=request.form.get("social_name", ""),
        link=request.form.get("social_link", ""),
    )

    links.create(link)

    return redirect(url_for("user_details.user_details_page"))
