import pytest
from flask.testing import FlaskClient

from intranet.runner.setup import setup


@pytest.fixture()
def app() -> FlaskClient:
    app = setup().test_client()

    return app


def test_should_display_login_page(app: FlaskClient) -> None:
    response = app.get("/login")

    assert response.status_code == 200
    assert "Login | Intranet" in response.get_data(as_text=True)


def test_should_display_register_page(app: FlaskClient) -> None:
    response = app.get("/register")

    assert response.status_code == 200
    assert "Register | Intranet" in response.get_data(as_text=True)


@pytest.mark.skip()
def test_should_not_register_without_username(app: FlaskClient) -> None:
    response = app.post(
        "/register",
        data={
            "username": "",
            "password": "asdf",
            "confirmation": "asdf",
        },
    )

    assert response.status_code == 403
    assert "must-provide-username" in response.get_data(as_text=True)


@pytest.mark.skip()
def test_should_not_register_without_password(app: FlaskClient) -> None:
    response = app.post(
        "/register",
        data={
            "username": "asdf",
            "password": "",
            "confirmation": "asdf",
        },
    )

    assert response.status_code == 403
    assert "must-provide-password" in response.get_data(as_text=True)


def test_should_not_register_without_password_confirmation(app: FlaskClient) -> None:
    response = app.post(
        "/register",
        data={
            "username": "asdf",
            "password": "asdf",
            "confirmation": "qwerty",
        },
    )

    assert response.status_code == 403
    assert "password-didn%27t-match" in response.get_data(as_text=True)


def test_should_register(app: FlaskClient) -> None:
    response = app.post(
        "/register",
        data={
            "username": "asdf",
            "password": "asdf",
            "confirmation": "asdf",
        },
    )

    assert response.status_code == 302
    assert "Redirecting..." in response.get_data(as_text=True)
    assert "/login" in response.get_data(as_text=True)


def test_should_not_register_with_same_username(app: FlaskClient) -> None:
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
    assert "username-already-exists" in response.get_data(as_text=True)


@pytest.mark.skip()
def test_should_not_login_without_username(app: FlaskClient) -> None:
    response = app.post("/login", data={"username": "", "password": "asdf"})

    assert response.status_code == 403
    assert "must-provide-username" in response.get_data(as_text=True)


@pytest.mark.skip()
def test_should_not_login_without_password(app: FlaskClient) -> None:
    response = app.post("/login", data={"username": "asdf", "password": ""})

    assert response.status_code == 403
    assert "must-provide-password" in response.get_data(as_text=True)


def test_should_not_login_with_wrong_password(app: FlaskClient) -> None:
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
    assert "invalid-username-and~sor-password" in response.get_data(as_text=True)


def test_should_login(app: FlaskClient) -> None:
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
            "username": "asdf",
            "password": "asdf",
        },
    )

    assert response.status_code == 302
    assert "Redirecting..." in response.get_data(as_text=True)


def test_should_logout(app: FlaskClient) -> None:
    app.post(
        "/register",
        data={
            "username": "asdf",
            "password": "asdf",
            "confirmation": "asdf",
        },
    )

    app.post(
        "/login",
        data={
            "username": "asdf",
            "password": "asdf",
        },
    )

    response = app.get("/logout")

    assert response.status_code == 302
    assert "Redirecting..." in response.get_data(as_text=True)


def test_should_not_display_home_without_authorization(app: FlaskClient) -> None:
    response = app.get("/")

    assert response.status_code == 302
    assert "Redirecting..." in response.get_data(as_text=True)
    assert "/login" in response.get_data(as_text=True)


def test_should_display_home_with_authorization(app: FlaskClient) -> None:
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
