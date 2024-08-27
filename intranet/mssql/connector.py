from __future__ import annotations

import os
from dataclasses import dataclass

import pymssql
from pymssql import Connection


@dataclass
class MsSqlConnector:
    def connect(self) -> Connection:
        return pymssql.connect(
            server=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            as_dict=True,
            autocommit=True,
        )
