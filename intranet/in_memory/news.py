import datetime
from dataclasses import dataclass, field
from typing import Any, Iterator

from intranet.core.news import News, NewsRepository


@dataclass
class NewsInMemoryRepository(NewsRepository):  # pragma: no cover
    news: list[News] = field(default_factory=list)

    def create(self, news: News) -> News:
        news.creation_date = datetime.datetime.now().strftime("%Y/%m/%d, %H:%M")
        self.news.append(news)

        return news

    def read(self, _id: str) -> News:
        for news in self.news:
            if news.id == _id:
                return news

        raise KeyError(f"News with id '{_id}' not found.")

    def read_all(self) -> list[News]:
        return self.news

    def __iter__(self) -> Iterator[News]:
        yield from reversed(self.news)

    def delete(self, _id: str) -> None:
        for i, news in enumerate(self.news):
            if news.id == _id:
                del self.news[i]
                return

        raise DoesNotExistError(_id)


@dataclass
class DoesNotExistError(Exception):
    id: Any = "unknown"
