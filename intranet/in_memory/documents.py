from dataclasses import dataclass, field
from typing import Iterator

from intranet.core.document import Document, DocumentRepository


@dataclass
class DocumentInMemoryRepository(DocumentRepository):  # pragma: no cover
    documents: list[Document] = field(default_factory=list)

    def create(self, document: Document) -> Document:
        self.documents.append(document)

        return document

    def read(self, _id: str) -> Document:
        for document in self.documents:
            if document.id == _id:
                return document

        raise KeyError(f"Document with id '{_id}' not found.")

    def read_all(self) -> list[Document]:
        return self.documents

    def update(self, _id: str, new_status: str) -> None:
        for document in self.documents:
            if document.id == _id:
                document.status = new_status
                return
        raise KeyError(f"Document with id '{_id}' not found.")

    def __iter__(self) -> Iterator[Document]:
        yield from self.documents
