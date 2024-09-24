from unittest.mock import ANY

import pytest

from intranet.core.document import Document
from intranet.in_memory.documents import DocumentInMemoryRepository
from tests.fake import FakeDocument


@pytest.fixture()
def documents() -> DocumentInMemoryRepository:
    return DocumentInMemoryRepository()


def test_should_not_read_when_none_exist(
    documents: DocumentInMemoryRepository,
) -> None:
    assert documents.read_all() == []
    assert len(documents.read_all()) == 0


def test_should_persist(documents: DocumentInMemoryRepository) -> None:
    _document = documents.create(FakeDocument().entity)

    assert documents.read(_document.id) == Document(
        id=ANY,
        user_id=_document.user_id,
        creation_date=_document.creation_date,
        category=_document.category,
        directory=_document.directory,
        status=_document.status,
    )


def test_should_persist_many(documents: DocumentInMemoryRepository) -> None:
    document_1 = documents.create(FakeDocument().entity)
    document_2 = documents.create(FakeDocument().entity)
    assert documents.read_all() == [
        Document(
            id=ANY,
            user_id=document_1.user_id,
            creation_date=document_1.creation_date,
            category=document_1.category,
            directory=document_1.directory,
            status=document_1.status,
        ),
        Document(
            id=ANY,
            user_id=document_2.user_id,
            creation_date=document_2.creation_date,
            category=document_2.category,
            directory=document_2.directory,
            status=document_2.status,
        ),
    ]
