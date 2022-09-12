from dataclasses import dataclass

@dataclass(frozen=True)
class Email:
    frm: str
    to: str
    subject: str
    datetime: str
    content: str
