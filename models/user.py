from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    _id: int
    email: str
    name: str
    phone: str