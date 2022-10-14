from dataclasses import dataclass


# We used underscore to escape reserved keywords like 'to'.
@dataclass(frozen=True)
class Message:
    _id: str
    frm: str
    _to: str
    subject: str
    _datetime: str
    content: str
    user_id: int
