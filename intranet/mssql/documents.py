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
                    category,
                    directory,
                    status
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    document.id,
                    document.user_id,
                    document.category.value,
                    document.directory,
                    document.status,
                ),
            )

            return document

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
                    FORMAT(
                        creation_date, 'yyyy/MM/dd, HH:mm'
                    ) AS formatted_creation_date,
                    category,
                    directory,
                    status,
                    creation_date
                FROM documents
                ORDER BY creation_date DESC
            """)
            rows = cursor.fetchall()

        for row in rows:
            yield Document(
                id=row["id"],
                user_id=row["user_id"],
                creation_date=row["formatted_creation_date"],
                category=row["category"],
                directory=row["directory"],
                status=row["status"],
            )
