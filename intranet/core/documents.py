from dataclasses import dataclass


@dataclass
class Document:
    id: str
    first_name: str
    last_name: str
    dates: str
    category: str
    status: str
