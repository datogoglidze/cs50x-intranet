from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator, Protocol


class UserRepository(Protocol):  # pragma: no cover
    def create(self, user: dict[str, Any]) -> User:
        pass

    def read(self, username: str) -> User:
        pass

    def __iter__(self) -> Iterator[User]:
        pass


@dataclass
class User:
    id: str
    username: str
    password: str
