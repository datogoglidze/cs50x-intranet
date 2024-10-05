import datetime
from math import ceil
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

    page = request.args.get("page", 1, type=int)
    news_per_page = 10

    all_news = [item for item in news_repository]
    total_news = len(all_news)
    total_pages = ceil(total_news / news_per_page)

    start = (page - 1) * news_per_page
    end = start + news_per_page
    news_items = all_news[start:end]

    return render_template(
        "index.html",
        is_admin=is_admin,
        news=news_items,
        page=page,
        total_pages=total_pages,
        total_news=total_news,
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
