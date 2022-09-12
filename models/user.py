from dataclasses import dataclass

@dataclass(frozen=True)
class Mail:
    email: str
    name: str
    comments: str
