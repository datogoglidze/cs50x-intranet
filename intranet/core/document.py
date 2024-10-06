from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, Protocol


class DocumentRepository(Protocol):  # pragma: no cover
    def create(self, document: Document) -> Document:
        pass

    def update(self, document_id: str, new_status: str) -> None:
        pass

    def __iter__(self) -> Iterator[Document]:
        pass


@dataclass
class Document:
    id: str
    user_id: str
    category: Category
    directory: str
    status: str

    creation_date: str | None = field(default_factory=lambda: None)


class Category(Enum):
    paid_vacation: str = "Vacation (Paid)"
    unpaid_vacation: str = "Vacation (Unpaid)"
    paid_maternity: str = "Maternity Leave (Paid)"
    resignation: str = "Resignation"
    development: str = "Course/Training Request"
