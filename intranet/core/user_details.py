from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator, Protocol


class UserDetailsRepository(Protocol):  # pragma: no cover
    def create(self, user_details: dict[str, Any]) -> UserDetails:
        pass

    def read(self, user_id: str) -> UserDetails:
        pass

    def __iter__(self) -> Iterator[UserDetails]:
        pass


@dataclass
class UserDetails:
    id: str
    first_name: str = ""
    last_name: str = ""
    birth_date: int = 0
    department: str = ""
    email: str = ""
    phone_number: str = ""
