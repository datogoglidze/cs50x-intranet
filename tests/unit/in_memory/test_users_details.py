from unittest.mock import ANY

import pytest

from intranet.core.user_details import UserDetails
from intranet.in_memory.users import UserInMemoryRepository
from intranet.in_memory.users_details import UsersDetailsInMemoryRepository
from tests.fake import FakeUser, FakeUserDetails


@pytest.fixture()
def users() -> UserInMemoryRepository:
    return UserInMemoryRepository()


@pytest.fixture()
def details() -> UsersDetailsInMemoryRepository:
    return UsersDetailsInMemoryRepository()


def test_should_not_read_when_none_exist(
    details: UsersDetailsInMemoryRepository,
) -> None:
    assert details.read_all() == []
    assert len(details.read_all()) == 0


def test_should_not_read_unknown(details: UsersDetailsInMemoryRepository) -> None:
    with pytest.raises(KeyError):
        details.read(FakeUserDetails().unknown_user_details())


def test_should_persist(details: UsersDetailsInMemoryRepository) -> None:
    _details = details.create(FakeUserDetails().entity)

    assert details.read(_details.id) == UserDetails(
        id=ANY,
        first_name=_details.first_name,
        last_name=_details.last_name,
        birth_date=_details.birth_date,
        department=_details.department,
        email=_details.email,
        phone_number=_details.phone_number,
    )


def test_should_persist_many(details: UsersDetailsInMemoryRepository) -> None:
    details_1 = details.create(FakeUserDetails().entity)
    details_2 = details.create(FakeUserDetails().entity)

    assert details.read_all() == [
        UserDetails(
            id=ANY,
            first_name=details_1.first_name,
            last_name=details_1.last_name,
            birth_date=details_1.birth_date,
            department=details_1.department,
            email=details_1.email,
            phone_number=details_1.phone_number,
        ),
        UserDetails(
            id=ANY,
            first_name=details_2.first_name,
            last_name=details_2.last_name,
            birth_date=details_2.birth_date,
            department=details_2.department,
            email=details_2.email,
            phone_number=details_2.phone_number,
        ),
    ]


def test_should_not_duplicate(
    users: UserInMemoryRepository,
    details: UsersDetailsInMemoryRepository,
) -> None:
    user_id = users.create(FakeUser().entity).id
    _details = FakeUserDetails().entity
    _details.id = user_id
    details.create(_details)

    with pytest.raises(ValueError):
        details.create(_details)
