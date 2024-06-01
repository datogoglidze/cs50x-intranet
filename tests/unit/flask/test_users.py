from unittest.mock import ANY

import pytest

from intranet.core.user import User
from intranet.in_memory.users import UserInMemoryRepository


@pytest.fixture()
def users() -> UserInMemoryRepository:
    return UserInMemoryRepository()


def test_should_not_read_when_none_exist(users: UserInMemoryRepository) -> None:
    assert users.read_all() == []


def test_should_not_read_unknown(users: UserInMemoryRepository) -> None:
    with pytest.raises(KeyError):
        users.read("datoie")


def test_should_persist(users: UserInMemoryRepository) -> None:
    username = users.create({"username": "datoie", "password": "123"}).username

    assert users.read(username) == User(id=ANY, username="datoie", password="123")


def test_should_persist_many(users: UserInMemoryRepository) -> None:
    users.create({"username": "datoie", "password": "123"})
    users.create({"username": "datoie2", "password": "123"})

    assert users.read_all() == [
        User(id=ANY, username="datoie", password="123"),
        User(id=ANY, username="datoie2", password="123"),
    ]
