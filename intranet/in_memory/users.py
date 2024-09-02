from dataclasses import dataclass, field
from typing import Iterator

from intranet.core.user import User, UserRepository


@dataclass
class UserInMemoryRepository(UserRepository):  # pragma: no cover
    users: list[User] = field(default_factory=list)

    def create(self, user: User) -> User:
        self._ensure_does_not_exist(user.username)

        self.users.append(user)

        return user

    def _ensure_does_not_exist(self, username: str) -> None:
        for existing in self.users:
            if username == existing.username:
                raise ValueError(f"User with username '{username}' already exists.")

    def read(self, user_id: str) -> User:
        for user in self.users:
            if user.id == user_id:
                return user

        raise KeyError(f"User with id '{user_id}' not found.")

    def read_all(self) -> list[User]:
        return self.users

    def __iter__(self) -> Iterator[User]:
        yield from self.users
