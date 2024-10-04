import datetime
from uuid import uuid4

from dependency_injector.wiring import Provide, inject
from flask import Blueprint, redirect, render_template, request, session
from werkzeug import Response

from intranet.core.news import News, NewsRepository
from intranet.core.user import UserRepository
from intranet.error import login_required
from intranet.flask.dependable import Container

news = Blueprint("news", __name__, template_folder="../front/templates")


@news.get("/")
@inject
@login_required
def read_news(
    news_repository: NewsRepository = Provide[Container.news_repository],
    users: UserRepository = Provide[Container.user_repository],
) -> str:
    is_admin = True if users.read(session["user_id"]).username == "admin" else False
    news_items = [item for item in news_repository]

    return render_template(
        "index.html",
        news=news_items,
        is_admin=is_admin,
    )


@news.post("/news")
@inject
@login_required
def create_news(
    news_repository: NewsRepository = Provide[Container.news_repository],
) -> Response | tuple[str, int]:
    _news = News(
        id=str(uuid4()),
        creation_date=datetime.datetime.now().strftime("%Y/%m/%d, %H:%M"),
        title=request.form.get("title", ""),
        content=request.form.get("content", ""),
    )

    news_repository.create(_news)

    return redirect("/")
