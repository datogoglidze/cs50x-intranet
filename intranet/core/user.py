from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator, Protocol
from uuid import uuid4


class UserRepository(Protocol):  # pragma: no cover
    def create(self, user: User) -> User:
        pass

    def read(self, user_id: str) -> User:
        pass

    def __iter__(self) -> Iterator[User]:
        pass


@dataclass
class User:
    username: str
    password: str

    id: str = field(default_factory=lambda: str(uuid4()))
