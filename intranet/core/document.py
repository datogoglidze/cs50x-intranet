from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterator, Protocol


class DocumentRepository(Protocol):  # pragma: no cover
    def create(self, document: Document) -> Document:
        pass

    def read(self, document_id: str) -> Document:
        pass

    def update(self, document_id: str, new_status: str) -> None:
        pass

    def __iter__(self) -> Iterator[Document]:
        pass


@dataclass
class Document:
    id: str
    user_id: str
    creation_date: str
    category: Category
    directory: str
    status: str


class Category(Enum):
    paid_vacation: str = "Paid Vacation"
    unpaid_vacation: str = "Unpaid Vacation"
    paid_maternity: str = "Paid Maternity Leave"
    resignation: str = "Resignation"
