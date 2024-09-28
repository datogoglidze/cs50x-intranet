from unittest.mock import ANY

import pytest

from intranet.core.news import News
from intranet.in_memory.news import NewsInMemoryRepository
from tests.fake import FakeNews


@pytest.fixture()
def news() -> NewsInMemoryRepository:
    return NewsInMemoryRepository()


def test_should_not_read_when_none_exist(
    news: NewsInMemoryRepository,
) -> None:
    assert news.read_all() == []
    assert len(news.read_all()) == 0


def test_should_persist(news: NewsInMemoryRepository) -> None:
    _news = news.create(FakeNews().entity)

    assert news.read(_news.id) == News(
        id=ANY,
        creation_date=_news.creation_date,
        title=_news.title,
        content=_news.content,
        status=_news.status,
    )


def test_should_persist_many(news: NewsInMemoryRepository) -> None:
    news_1 = news.create(FakeNews().entity)
    news_2 = news.create(FakeNews().entity)
    assert news.read_all() == [
        News(
            id=ANY,
            creation_date=news_1.creation_date,
            title=news_1.title,
            content=news_1.content,
            status=news_1.status,
        ),
        News(
            id=ANY,
            creation_date=news_2.creation_date,
            title=news_2.title,
            content=news_2.content,
            status=news_2.status,
        ),
    ]
