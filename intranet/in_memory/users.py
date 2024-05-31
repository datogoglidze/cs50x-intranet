from dataclasses import dataclass, field
from typing import Any, Iterator
from uuid import uuid4

from intranet.core.user import User, UserRepository


@dataclass
class UserInMemoryRepository(UserRepository):  # pragma: no cover
    users: list[User] = field(default_factory=list)

    def create(self, user: dict[str, Any]) -> User:
        self._ensure_does_not_exist(user["username"])

        self.users.append(User(id=str(uuid4()), **user))

        return self.users[-1]

    def _ensure_does_not_exist(self, username: str) -> None:
        for existing in self.users:
            if username == existing.username:
                raise ValueError

    def read(self, username: str) -> User:
        for user in self.users:
            if user.username == username:
                return user

        raise KeyError

    def read_all(self) -> list[User]:
        return self.users

    def __iter__(self) -> Iterator[User]:
        yield from self.users
