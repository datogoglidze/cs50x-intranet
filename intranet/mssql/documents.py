from dataclasses import dataclass
from typing import Iterator

from intranet.core.document import Document, DocumentRepository
from intranet.mssql.connector import MsSqlConnector


@dataclass
class DocumentMssqlRepository(DocumentRepository):  # pragma: no cover
    def create(self, document: Document) -> Document:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO documents (
                    id,
                    user_id,
                    creation_date,
                    category,
                    directory,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    document.id,
                    document.user_id,
                    document.creation_date,
                    document.category.value,
                    document.directory,
                    document.status,
                ),
            )

            return document

    def read(self, document_id: str) -> Document:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    id,
                    user_id,
                    creation_date,
                    category,
                    directory,
                    status
                FROM documents
                WHERE id = %s
                """,
                (document_id,),
            )
            row = cursor.fetchone()

            if row is not None:
                return Document(
                    row["id"],
                    row["user_id"],
                    row["creation_date"],
                    row["category"],
                    row["directory"],
                    row["status"],
                )

        raise KeyError(f"Document with id '{document_id}' not found.")

    def update(self, _id: str, new_status: str) -> None:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE documents
                SET status = %s
                WHERE id = %s
                """,
                (new_status, _id),
            )

    def __iter__(self) -> Iterator[Document]:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    id,
                    user_id,
                    creation_date,
                    category,
                    directory,
                    status
                FROM documents
                ORDER BY creation_date DESC
            """)
            rows = cursor.fetchall()

        for row in rows:
            yield Document(
                row["id"],
                row["user_id"],
                row["creation_date"],
                row["category"],
                row["directory"],
                row["status"],
            )
