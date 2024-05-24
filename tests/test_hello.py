import pytest
from flask.testing import FlaskClient

from intranet.runner.cli import app


@pytest.fixture()
def client() -> FlaskClient:
    client = app.test_client()

    with client.session_transaction() as session:
        session["user_id"] = "33b58955-d84b-40b0-b480-8416f519a567"

    return client


def test_home_with_authorization(client: FlaskClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert b"Home | Intranet" in response.data


def test_home_without_authorization(client: FlaskClient) -> None:
    client.get("/logout")

    response = client.get("/")

    assert b"Redirecting..." in response.data


def test_login_without_username(client: FlaskClient) -> None:
    response = client.post("/login", data={"username": "", "password": "asdf"})

    assert b"must-provide-username" in response.data


def test_login_without_password(client: FlaskClient) -> None:
    response = client.post("/login", data={"username": "asdf", "password": ""})

    assert b"must-provide-password" in response.data
