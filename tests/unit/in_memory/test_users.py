import pytest

from intranet.core.user import User
from intranet.in_memory.users import UserInMemoryRepository
from tests.fake import FakeUser


@pytest.fixture()
def users() -> UserInMemoryRepository:
    return UserInMemoryRepository()


def test_should_not_read_when_none_exist(users: UserInMemoryRepository) -> None:
    assert users.read_all() == []
    assert len(users.read_all()) == 0


def test_should_not_read_unknown(users: UserInMemoryRepository) -> None:
    with pytest.raises(KeyError):
        users.read(FakeUser().unknown_username())


def test_should_persist(users: UserInMemoryRepository) -> None:
    user = users.create(FakeUser().entity)

    assert users.read(user.id) == User(
        id=user.id,
        username=user.username,
        password=user.password,
    )


def test_should_persist_many(users: UserInMemoryRepository) -> None:
    user_1 = users.create(FakeUser().entity)
    user_2 = users.create(FakeUser().entity)

    assert users.read_all() == [
        User(id=user_1.id, username=user_1.username, password=user_1.password),
        User(id=user_2.id, username=user_2.username, password=user_2.password),
    ]


def test_should_not_duplicate(users: UserInMemoryRepository) -> None:
    user = FakeUser().entity
    users.create(user)

    with pytest.raises(ValueError):
        users.create(user)
