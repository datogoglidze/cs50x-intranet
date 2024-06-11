from dataclasses import dataclass, field
from typing import Any, Iterator

from intranet.core.user_details import UserDetails, UserDetailsRepository


@dataclass
class UsersDetailsInMemoryRepository(UserDetailsRepository):  # pragma: no cover
    user_details: list[UserDetails] = field(default_factory=list)

    def create(self, user_details: UserDetails) -> UserDetails:
        self._ensure_does_not_exist(user_details.id)

        self.user_details.append(user_details)

        return self.user_details[-1]

    def _ensure_does_not_exist(self, _id: str) -> None:
        for existing in self.user_details:
            if _id == existing.id:
                raise ValueError

    def read(self, _id: str) -> UserDetails:
        for user in self.user_details:
            if user.id == _id:
                return user

        raise KeyError

    def read_all(self) -> list[UserDetails]:
        return self.user_details

    def __iter__(self) -> Iterator[UserDetails]:
        yield from self.user_details

    def delete(self, item_id: Any) -> None:
        for i, user in enumerate(self.user_details):
            if user.id == str(item_id):
                del self.user_details[i]
                return

        raise DoesNotExistError(item_id)

    def update(self, item: UserDetails) -> None:
        self.delete(item.id)
        self.create(item)


@dataclass
class DoesNotExistError(Exception):
    id: Any = "unknown"
