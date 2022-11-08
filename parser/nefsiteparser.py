from utils import remove_spaces

from .parser import Parser
from .parsingchecker import ParsingChecker


class NefSiteParser(Parser):
    def __init__(self, received_email: dict) -> None:
        super().__init__(received_email)
        self.received_email['content'] = self.received_email['content'].replace('received_email', 'email')
    
    @ParsingChecker.checker
    def parse_user(self) -> dict:
        name = ' '.join(self.received_email['content'].split('Το ονοματεπώνυμο σας::')[1].split('Ενδια')[0].split())
        user_mail = remove_spaces(self.received_email['content'].split('Το email σας::')[1].split('Το μήνυμ')[0])
        phone = remove_spaces(self.received_email['content'].split('Το email σας::')[0].split('Τηλέφωνο επικοινωνίας::')[1])
        return {'name': name, 'email': user_mail, 'phone': phone}

    @ParsingChecker.checker
    def parse_ceremony(self) -> dict:
        # Parse the name given on the form
        date = remove_spaces(self.received_email['content'].split('Ημερομηνία εκδήλωσης: :')[1].split('Αριθμός')[0])
        people = remove_spaces(self.received_email['content'].split('Αριθμός ατόμων::')[1].split('Τηλ')[0])
        ceremony_type = remove_spaces(self.received_email['content'].split('Ενδιαφέρεστε για::')[1].split('Ημερο')[0]) 
        comments = self.received_email['content'].split('Το μήνυμά σας: :')[1]
        return {'date': date, 'people': people, 'ceremony_type': ceremony_type, 'comments': comments}