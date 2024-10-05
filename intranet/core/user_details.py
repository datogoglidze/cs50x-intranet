from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterator, Protocol


class UserDetailsRepository(Protocol):  # pragma: no cover
    def create(self, user_details: UserDetails) -> UserDetails:
        pass

    def read(self, user_id: str) -> UserDetails:
        pass

    def update(self, user_details: UserDetails) -> None:
        pass

    def __iter__(self) -> Iterator[UserDetails]:
        pass


@dataclass
class UserDetails:
    id: str
    department: Department
    first_name: str
    last_name: str
    birth_date: str
    email: str
    phone_number: str


class Department(Enum):
    no_department: str = "no_department"
    it: str = "IT"
    hr: str = "Human Resources"
    support: str = "Customer Support"
    finance: str = "Finance"
    logistics: str = "Logistics"
    project_manager: str = "Project Manager"
