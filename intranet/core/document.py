from dataclasses import dataclass


@dataclass
class Document:
    id: str
    user_id: str
    directory: str
    status: str
