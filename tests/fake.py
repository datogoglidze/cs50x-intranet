from dataclasses import dataclass, field
from functools import cached_property
from uuid import uuid4

from faker import Faker

from intranet.core.news import News
from intranet.core.user import User
from intranet.core.user_details import UserDetails


@dataclass
class Fake:
    faker: Faker = field(default_factory=Faker)

    def text(self, length: int) -> str:
        return "".join(self.faker.random_letters(length=length))

    def timestamp(self) -> int:
        return int(self.faker.unix_time())


@dataclass
class FakeUser:
    fake: Fake = field(default_factory=Fake)

    @cached_property
    def entity(self) -> User:
        return User(
            id=str(uuid4()),
            username=self.fake.text(length=10),
            password=self.fake.text(length=5),
        )

    def unknown_username(self) -> str:
        return self.fake.text(length=10)


@dataclass
class FakeUserDetails:
    fake: Fake = field(default_factory=Fake)

    @cached_property
    def entity(self) -> UserDetails:
        return UserDetails(
            id=self.fake.text(length=5),
            first_name=self.fake.text(length=5),
            last_name=self.fake.text(length=10),
            birth_date=self.fake.timestamp(),
            department=self.fake.text(length=10),
            email=self.fake.text(length=5),
            phone_number=self.fake.text(length=5),
        )

    def unknown_user_details(self) -> str:
        return self.fake.text(length=10)


@dataclass
class FakeNews:
    fake: Fake = field(default_factory=Fake)

    @cached_property
    def entity(self) -> News:
        return News(
            title=self.fake.text(length=5),
            content=self.fake.text(length=5),
        )
