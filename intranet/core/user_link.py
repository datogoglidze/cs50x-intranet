from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Protocol


class UserLinksRepository(Protocol):  # pragma: no cover
    def create(self, user_links: UserLink) -> UserLink:
        pass

    def read(self, user_id: str) -> UserLink:
        pass

    def __iter__(self) -> Iterator[UserLink]:
        pass


@dataclass
class UserLink:
    id: str
    user_id: str = ""
    name: str = ""
    link: str = ""
