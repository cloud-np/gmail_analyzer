from .parser import Parser
from .parsingchecker import ParsingChecker
from utils import remove_spaces

class MelanSiteParser(Parser):
    def __init__(self, received_email: dict) -> None:
        super().__init__(received_email)
        self.received_email['content'] = self.received_email['content'].replace('received_email', 'email')
    
    @ParsingChecker.checker
    def parse_user(self) -> dict:
        name = ' '.join(self.received_email['content'].split('Το ονοματεπώνυμο σας: *:')[1].split('Ενδια')[0].split())
        user_mail = remove_spaces(self.received_email['content'].split('Το email σας: *:')[1].split('Το μήνυμ')[0])
        phone = remove_spaces(self.received_email['content'].split('Το email σας: *:')[0].split('Τηλέφωνο επικοινωνίας: *:')[1])
        return {'name': name, 'email': user_mail, 'phone': phone}