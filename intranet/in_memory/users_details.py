from dataclasses import dataclass, field
from typing import Any, Iterator

from intranet.core.user_details import UserDetails, UserDetailsRepository


@dataclass
class UsersDetailsInMemoryRepository(UserDetailsRepository):  # pragma: no cover
    user_details: list[UserDetails] = field(default_factory=list)

    def create(self, user_details: UserDetails) -> UserDetails:
        self._ensure_does_not_exist(user_details.id)

        self.user_details.append(user_details)

        return user_details

    def _ensure_does_not_exist(self, _id: str) -> None:
        for existing in self.user_details:
            if _id == existing.id:
                raise ValueError(f"User Details with id '{_id}' already exists.")

    def read(self, _id: str) -> UserDetails:
        for user in self.user_details:
            if user.id == _id:
                return user

        raise KeyError(f"User Details with id '{_id}' not found.")

    def read_all(self) -> list[UserDetails]:
        return self.user_details

    def __iter__(self) -> Iterator[UserDetails]:
        yield from self.user_details

    def delete(self, _id: Any) -> None:
        for i, user in enumerate(self.user_details):
            if user.id == str(_id):
                del self.user_details[i]
                return

        raise DoesNotExistError(_id)

    def update(self, user_details: UserDetails) -> None:
        self.delete(user_details.id)
        self.create(user_details)


@dataclass
class DoesNotExistError(Exception):
    id: Any = "unknown"
