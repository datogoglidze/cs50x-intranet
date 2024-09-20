import pytest
from flask.testing import FlaskClient

from intranet.runner.setup import setup
from tests.fake import FakeUserDetails


@pytest.fixture()
def app() -> FlaskClient:
    app = setup().test_client()

    return app


def test_should_display_details_page(app: FlaskClient) -> None:
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

    response = app.get("/user-details")

    assert response.status_code == 200
    assert "User Details | Intranet" in response.get_data(as_text=True)


def test_should_not_display_details_page_without_authorization(
    app: FlaskClient,
) -> None:
    response = app.get("/user-details")

    assert response.status_code == 302
    assert "Redirecting..." in response.get_data(as_text=True)
    assert "/login" in response.get_data(as_text=True)


def test_should_add_details(app: FlaskClient) -> None:
    user_details = FakeUserDetails().entity
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
        "/user-details",
        data={
            "first_name": user_details.first_name,
            "last_name": user_details.last_name,
            "birth_date": user_details.birth_date,
            "department": user_details.department,
            "email": user_details.email,
            "phone_number": user_details.phone_number,
        },
    )

    response = app.get("/user-details")

    assert response.status_code == 200
    assert f"{user_details.first_name}" in response.get_data(as_text=True)
    assert f"{user_details.last_name}" in response.get_data(as_text=True)
    assert f"{user_details.birth_date}" in response.get_data(as_text=True)
    assert f"{user_details.department}" in response.get_data(as_text=True)
    assert f"{user_details.email}" in response.get_data(as_text=True)
    assert f"{user_details.phone_number}" in response.get_data(as_text=True)


def test_should_not_add_details_without_authorization(app: FlaskClient) -> None:
    user_details = FakeUserDetails().entity

    response = app.post(
        "/user-details",
        data={
            "first_name": user_details.first_name,
            "last_name": user_details.last_name,
            "birth_date": user_details.birth_date,
            "department": user_details.department,
            "email": user_details.email,
            "phone_number": user_details.phone_number,
        },
    )

    assert response.status_code == 302
