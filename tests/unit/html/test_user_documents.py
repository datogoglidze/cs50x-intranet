import pytest
from flask.testing import FlaskClient

from intranet.runner.setup import setup
from tests.fake import FakeUserDetails


@pytest.fixture()
def app() -> FlaskClient:
    app = setup().test_client()

    return app


def test_should_display_documents_page(app: FlaskClient) -> None:
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

    response = app.get("/documents")

    assert response.status_code == 200
    assert "Documents | Intranet" in response.get_data(as_text=True)


def test_should_not_display_documents_page_without_authorization(
    app: FlaskClient,
) -> None:
    response = app.get("/documents")

    assert response.status_code == 302
    assert "Redirecting..." in response.get_data(as_text=True)
    assert "/login" in response.get_data(as_text=True)


def test_should_not_add_without_user_details(app: FlaskClient) -> None:
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

    response = app.post(
        "/documents",
        data={"dates": "January"},
    )

    assert response.status_code == 403
    assert "must-fill-user-details" in response.get_data(as_text=True)


@pytest.mark.skip(reason="Not testable right now")
def test_should_not_add_without_dates(app: FlaskClient) -> None:
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
            "department": user_details.department.name,
            "email": user_details.email,
            "phone_number": user_details.phone_number,
        },
    )

    response = app.post(
        "/documents",
        data={"dates": ""},
    )

    assert response.status_code == 403
    assert "must-specify-date" in response.get_data(as_text=True)
