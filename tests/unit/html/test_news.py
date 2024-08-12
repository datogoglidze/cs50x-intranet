import pytest
from flask.testing import FlaskClient

from intranet.core.news import News
from intranet.runner.setup import setup
from tests.fake import FakeNews


@pytest.fixture()
def app() -> FlaskClient:
    app = setup().test_client()

    return app


def test_should_display_news_page(app: FlaskClient) -> None:
    app.post(
        "/register",
        data={
            "username": "datoie",
            "password": "asdf",
            "confirmation": "asdf",
        },
    )
    app.post(
        "/login",
        data={
            "username": "datoie",
            "password": "asdf",
        },
    )

    response = app.get("/")

    assert response.status_code == 200
    assert "Home | Intranet" in response.get_data(as_text=True)


def test_should_not_display_news_page_without_authorization(
    app: FlaskClient,
) -> None:
    response = app.get("/")

    assert response.status_code == 302
    assert "Redirecting..." in response.get_data(as_text=True)
    assert "/login" in response.get_data(as_text=True)


def test_should_add_news(app: FlaskClient) -> None:
    news = News(**FakeNews().dict)
    app.post(
        "/register",
        data={
            "username": "datoie",
            "password": "asdf",
            "confirmation": "asdf",
        },
    )
    app.post(
        "/login",
        data={
            "username": "datoie",
            "password": "asdf",
        },
    )
    app.post(
        "/news",
        data={
            "title": news.title,
            "content": news.content,
        },
    )

    response = app.get("/")

    assert response.status_code == 200
    assert f"{news.title}" in response.get_data(as_text=True)
    assert f"{news.content}" in response.get_data(as_text=True)


def test_should_not_add_news_without_authorization(app: FlaskClient) -> None:
    news = News(**FakeNews().dict)

    response = app.post(
        "/news",
        data={
            "title": news.title,
            "content": news.content,
        },
    )

    assert response.status_code == 302
