from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Protocol


class NewsRepository(Protocol):  # pragma: no cover
    def create(self, news: News) -> News:
        pass

    def read(self, news_id: str) -> News:
        pass

    def delete(self, news_id: str) -> None:
        pass

    def __iter__(self) -> Iterator[News]:
        pass


@dataclass
class News:
    id: str
    creation_date: str
    title: str
    content: str
