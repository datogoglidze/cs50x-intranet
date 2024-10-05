from dataclasses import dataclass, field
from typing import Any, Iterator

from intranet.core.user_link import UserLink, UserLinksRepository


@dataclass
class UserLinksInMemoryRepository(UserLinksRepository):  # pragma: no cover
    user_links: list[UserLink] = field(default_factory=list)

    def create(self, user_link: UserLink) -> UserLink:
        self.user_links.append(user_link)

        return user_link

    def read(self, _id: str) -> UserLink:
        for link in self.user_links:
            if link.id == _id:
                return link

        raise KeyError(f"User Link with id '{_id}' not found.")

    def delete(self, _id: str) -> None:
        for i, link in enumerate(self.user_links):
            if link.id == str(_id):
                del self.user_links[i]
                return

        raise DoesNotExistError(_id)

    def __iter__(self) -> Iterator[UserLink]:
        yield from self.user_links


@dataclass
class DoesNotExistError(Exception):
    id: Any = "unknown"
