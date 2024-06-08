from dataclasses import dataclass, field
from typing import Any, Iterator

from intranet.core.user_details import UserDetails, UserDetailsRepository


@dataclass
class UsersDetailsInMemoryRepository(UserDetailsRepository):  # pragma: no cover
    user_details: list[UserDetails] = field(default_factory=list)

    def create(self, user_details: dict[str, Any]) -> UserDetails:
        self._ensure_does_not_exist(user_details["id"])

        self.user_details.append(UserDetails(**user_details))

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
