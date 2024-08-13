from dependency_injector.wiring import Provide, inject
from flask import Blueprint, redirect, render_template, request
from werkzeug import Response

from intranet.core.news import News, NewsRepository
from intranet.error import login_required
from intranet.flask.dependable import Container

news = Blueprint("news", __name__, template_folder="../front/templates")


@news.get("/")
@inject
@login_required
def news_page(
    news_repository: NewsRepository = Provide[Container.news_repository],
) -> str:
    news_items = []

    for _news in news_repository:
        news_items.append(_news)

    return render_template("index.html", news=news_items)


@news.post("/news")
@inject
@login_required
def create_news(
    news_repository: NewsRepository = Provide[Container.news_repository],
) -> Response | tuple[str, int]:
    _news = News(
        title=request.form.get("title", ""),
        content=request.form.get("content", ""),
    )

    news_repository.create(_news)

    return redirect("/")
