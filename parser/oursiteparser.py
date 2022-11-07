from .parser import Parser
from .parsingchecker import ParsingChecker
from utils import remove_spaces

class OurSiteParser(Parser):
    def __init__(self, received_email: dict) -> None:
        super().__init__(received_email)
    
    @ParsingChecker.checker
    def parse_user(self) -> dict:
        name = remove_spaces(self.received_email['content'].split('Από:')[1].split('<')[0])
        user_mail = remove_spaces(self.received_email['content'].split('Από:')[1].split('<')[1].split('>')[0])
        phone = remove_spaces(self.received_email['content'].split('Τηλέφωνο Επικοινωνίας:')[1].split('Σχόλια:')[0])
        return {'name': name, 'email': user_mail, 'phone': phone}

    @ParsingChecker.checker
    def parse_ceremony(self) -> dict:
        # Parse the name given on the form
        date = remove_spaces(self.received_email['content'].split('Ημερομηνία Ενδιαφέροντος:')[1].split('Αριθμός Ατόμων:')[0])
        people = int(self.received_email['content'].split('Αριθμός Ατόμων:')[1].split('Είδος Δεξίωσης')[0])
        ceremony_type = remove_spaces(self.received_email['content'].split('Είδος Δεξίωσης:')[1].split('Τηλέφωνο Επικοινωνίας')[0])
        comments = remove_spaces(self.received_email['content'].split('Σχόλια:')[1].split('--')[0])
        return {'date': date, 'people': people, 'ceremony_type': ceremony_type, 'comments': comments}

    # @ParsingChecker.checker
    # def parse_message(self) -> dict:
    #     # Parse the name given on the form
    #     date = re.search('Ημερομηνία:.*|\s*Άρ$', self.received_email['content']).group().split('Ημερομηνία:')[1][:-1]
    #     people = int(self.received_email['content'].split('Άρ. Ατόμων:')[1].split('Είδος')[0])
    #     ceremony_type = remove_spaces(self.received_email['content'].split('Είδος Δεξίωσης:')[1].split('Τηλ')[0])
    #     comments = self.received_email['content'].split('Σχόλια:')[1]
    #     return {'date': date, 'people': people, 'ceremony_type': ceremony_type, 'comments': comments}