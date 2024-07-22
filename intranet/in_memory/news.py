from dataclasses import dataclass, field
from typing import Any, Iterator

from intranet.core.news import News, NewsRepository


@dataclass
class NewsInMemoryRepository(NewsRepository):  # pragma: no cover
    news: list[News] = field(default_factory=list)

    def create(self, news: News) -> News:
        self._ensure_does_not_exist(news.id)

        self.news.append(news)

        return self.news[-1]

    def _ensure_does_not_exist(self, _id: str) -> None:
        for existing in self.news:
            if _id == existing.id:
                raise ValueError

    def read(self, _id: str) -> News:
        for news in self.news:
            if news.id == _id:
                return news

        raise KeyError

    def read_all(self) -> list[News]:
        return self.news

    def __iter__(self) -> Iterator[News]:
        yield from self.news

    def delete(self, item_id: Any) -> None:
        for i, news in enumerate(self.news):
            if news.id == str(item_id):
                del self.news[i]
                return

        raise DoesNotExistError(item_id)


@dataclass
class DoesNotExistError(Exception):
    id: Any = "unknown"
