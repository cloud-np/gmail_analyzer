from dataclasses import dataclass, fields


# We used underscore to escape reserved keywords like 'to'.
@dataclass(frozen=True)
class Message:
    msg_id: str
    frm: str
    _to: str
    subject: str
    _datetime: str
    content: str

    def __str__(self):
        """This representation helps with having an easier time inserting Message obj to the corrisponding table."""
        return "".join(f'{getattr(self, field.name)}, ' for field in fields(self))