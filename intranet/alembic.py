import os
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from alembic import command
from alembic.config import Config


@dataclass
class Alembic:
    config: Config

    @classmethod
    def from_env(cls, script_location: Path) -> Self:
        host = os.environ["DB_HOST"]
        user = os.environ["DB_USER"]
        name = os.environ["DB_NAME"]
        password = os.environ["DB_PASSWORD"]

        config = Config()
        config.set_main_option(
            "sqlalchemy.url",
            f"mssql+pymssql://{user}:{password}@{host}/{name}",
        )
        config.set_main_option("script_location", str(script_location))

        return cls(config)

    def upgrade(self, revision: str = "head") -> None:
        command.upgrade(self.config, revision)


def migrate_db() -> None:
    source = Path(__file__).resolve().parent.parent.joinpath("migrations")

    Alembic.from_env(source).upgrade()
