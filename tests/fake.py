from dataclasses import dataclass, field
from functools import cached_property
from typing import Any

from faker import Faker


@dataclass
class Fake:
    faker: Faker = field(default_factory=Faker)

    def text(self, length: int) -> str:
        return "".join(self.faker.random_letters(length=length))


@dataclass
class FakeUser:
    fake: Fake = field(default_factory=Fake)

    @cached_property
    def dict(self) -> dict[str, Any]:
        return {
            "username": self.fake.text(length=10),
            "password": self.fake.text(length=5),
        }

    def unknown_username(self) -> str:
        return self.fake.text(length=10)
