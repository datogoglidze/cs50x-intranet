from dataclasses import dataclass


@dataclass
class UserDocument:
    id: str
    first_name: str
    last_name: str
    dates: str
    category: str
