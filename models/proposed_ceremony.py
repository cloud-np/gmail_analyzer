from dataclasses import dataclass


# We used underscore to escape reserved keywords like 'to'.
@dataclass(frozen=True)
class ProposedCeremony:
    _id: str
    date: str
    people: str
    ceremony_type: str
    comments: str
    user_id: int
    msg_id: str
