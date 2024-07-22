from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator, Protocol
from uuid import uuid4


class NewsRepository(Protocol):  # pragma: no cover
    def create(self, news: News) -> News:
        pass

    def read(self, news_id: str) -> News:
        pass

    def __iter__(self) -> Iterator[News]:
        pass


@dataclass
class News:
    title: str
    content: str

    id: str = field(default_factory=lambda: str(uuid4()))
