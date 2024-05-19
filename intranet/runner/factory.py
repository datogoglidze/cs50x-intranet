import sqlite3
from dataclasses import dataclass
from sqlite3 import Connection
from typing import ContextManager


@dataclass
class SqliteConnector:
    dsn: str = "database/database.db"

    def connect(self) -> ContextManager[Connection]:
        connection = sqlite3.connect(self.dsn)
        connection.row_factory = sqlite3.Row

        return connection
