import pytest
from flask.testing import FlaskClient

from intranet.runner.setup import setup


@pytest.fixture()
def app() -> FlaskClient:
    app = setup().test_client()

    return app


def test_home_with_authorization(app: FlaskClient) -> None:
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
    assert b"Home | Intranet" in response.data


def test_home_without_authorization(app: FlaskClient) -> None:
    response = app.get("/")

    assert response.status_code == 302
    assert b"Redirecting..." in response.data
    assert b"/login" in response.data


def test_login_without_username(app: FlaskClient) -> None:
    response = app.post("/login", data={"username": "", "password": "asdf"})

    assert response.status_code == 403
    assert b"must-provide-username" in response.data


def test_login_without_password(app: FlaskClient) -> None:
    response = app.post("/login", data={"username": "asdf", "password": ""})

    assert response.status_code == 403
    assert b"must-provide-password" in response.data


def test_register_without_username(app: FlaskClient) -> None:
    response = app.post(
        "/register",
        data={
            "username": "",
            "password": "asdf",
            "confirmation": "asdf",
        },
    )

    assert response.status_code == 403
    assert b"must-provide-username" in response.data


def test_register_without_password(app: FlaskClient) -> None:
    response = app.post(
        "/register",
        data={
            "username": "asdf",
            "password": "",
            "confirmation": "asdf",
        },
    )

    assert response.status_code == 403
    assert b"must-provide-password" in response.data


def test_login_with_wrong_password(app: FlaskClient) -> None:
    app.post(
        "/register",
        data={
            "username": "asdf",
            "password": "asdf",
            "confirmation": "asdf",
        },
    )

    response = app.post(
        "/login",
        data={
            "username": "datoie",
            "password": "qwerty",
        },
    )

    assert response.status_code == 403
    assert b"invalid-username-and~sor-password" in response.data


def test_register_without_confirmation(app: FlaskClient) -> None:
    response = app.post(
        "/register",
        data={
            "username": "asdf",
            "password": "asdf",
            "confirmation": "qwerty",
        },
    )

    assert response.status_code == 403
    assert b"password-didn%27t-match" in response.data


def test_register(app: FlaskClient) -> None:
    response = app.post(
        "/register",
        data={
            "username": "asdf",
            "password": "asdf",
            "confirmation": "asdf",
        },
    )

    assert response.status_code == 302
    assert b"Redirecting..." in response.data
    assert b"/login" in response.data


def test_register_with_same_username(app: FlaskClient) -> None:
    app.post(
        "/register",
        data={
            "username": "asdf",
            "password": "asdf",
            "confirmation": "asdf",
        },
    )

    response = app.post(
        "/register",
        data={
            "username": "asdf",
            "password": "asdf",
            "confirmation": "asdf",
        },
    )

    assert response.status_code == 403
    assert b"username-already-exists" in response.data
