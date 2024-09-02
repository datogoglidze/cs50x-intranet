from dataclasses import dataclass
from typing import Any, Iterator

from intranet.core.user_details import UserDetails, UserDetailsRepository
from intranet.mssql.connector import MsSqlConnector


@dataclass
class UserDetailsMssqlRepository(UserDetailsRepository):  # pragma: no cover
    def create(self, user_details: UserDetails) -> UserDetails:
        self._ensure_does_not_exist(user_details.id)

        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO user_details (
                    id,
                    first_name,
                    last_name,
                    birth_date,
                    department,
                    email,
                    phone_number
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    user_details.id,
                    user_details.first_name,
                    user_details.last_name,
                    user_details.birth_date,
                    user_details.department,
                    user_details.email,
                    user_details.phone_number,
                ),
            )

            return user_details

    def _ensure_does_not_exist(self, _id: str) -> None:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id FROM user_details WHERE id = %s
                """,
                (_id,),
            )

            if cursor.fetchone() is not None:
                raise ValueError(f"UserDetails with id '{_id}' already exists.")

    def read(self, _id: str) -> UserDetails:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    id,
                    first_name,
                    last_name,
                    birth_date,
                    department,
                    email,
                    phone_number
                FROM user_details
                WHERE id = %s
                """,
                (_id,),
            )
            row = cursor.fetchone()

            if row is not None:
                return UserDetails(
                    row["id"],
                    row["first_name"],
                    row["last_name"],
                    row["birth_date"],
                    row["department"],
                    row["email"],
                    row["phone_number"],
                )

        raise KeyError(f"UserDetails with id '{_id}' not found.")

    def delete(self, item_id: Any) -> None:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                DELETE FROM user_details WHERE id = %s
                """,
                (item_id),
            )

    def update(self, item: UserDetails) -> None:
        self.delete(item.id)
        self.create(item)

    def __iter__(self) -> Iterator[UserDetails]:
        with MsSqlConnector().connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    id,
                    first_name,
                    last_name,
                    birth_date,
                    department,
                    email, phone_number
                FROM user_details
                """
            )
            rows = cursor.fetchall()

        for row in rows:
            yield UserDetails(
                row["id"],
                row["first_name"],
                row["last_name"],
                row["birth_date"],
                row["department"],
                row["email"],
                row["phone_number"],
            )
