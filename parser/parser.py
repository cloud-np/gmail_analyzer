from abc import abstractmethod

class Parser:
    def __init__(self, received_email: dict) -> None:
        self.received_email: dict = received_email

    @abstractmethod
    def parse_user(self) -> dict:
        """Extracts user information from a received email.
            name: str
            email: str
            phone: str
        """

    @abstractmethod
    def parse_ceremony(self) -> dict:
        """"""

    # def parse_message(self, received_email: dict):
        """Extracts message information from a received email.
            _id: str (This is unique id from google)
            frm: str
            _to: str
            subject: str
            _datetime: str
            content: str
        """