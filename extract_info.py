from controllers import MessageController, UserController, ProposedCeremonyController 
from models import Message, User, ProposedCeremony, proposed_ceremony
from utils import remove_spaces, model_from_dict
from parser import Parser, OurSiteParser, NefSiteParser
from typing import List, TypeVar
import re

# Used to access the .env file
from dotenv import load_dotenv
import os


P = TypeVar("P", OurSiteParser, NefSiteParser)

class Extractor:

    def __init__(self) -> None:
        load_dotenv()
        self.uc: UserController = UserController()
        # self.usc.create_users_table()
        # self.msc.create_messages_table()
        self.mc: MessageController = MessageController()
        self.cc: ProposedCeremonyController = ProposedCeremonyController()
        self.parser: P
    
    def __parse_user(self, received_email: dict) -> User:
        """Extracts information from a received email."""
    
    def __parse_proposed_ceremony(self, received_email: dict) -> ProposedCeremony:
        """Extracts information from a received email."""
        # try:
        #     proposed_ceremony: ProposedCeremony | None = self.cc.create_proposed_ceremony({'date': date, 'people': people, 'ceremony_type': ceremony_type, 'comments': comments, 'user_id': received_email['user_id'], 'msg_id': received_email['_id']})
        #     if proposed_ceremony is None:
        #         raise Exception('There was a Problem creating proposed_ceremony from email: ', received_email)
        # except:
        #     raise Exception('Something wrong with the content input of received_email id: ', received_email['_id'])
        # return proposed_ceremony 
    
    def __parse_message(self, received_email: dict, user_id: int):
        received_email['user_id'] = user_id
        message: Message = model_from_dict(Message, received_email)
        self.mc.insert_message(message)
        return message
    
    def __received_email_from_our_website(self, received_email: dict):
        """Extracts information from an received_email."""
        user: User = self.__parse_user(received_email)

        # Parse the message content and insert into the database if it doesn't exist already.
        message: Message = self.__parse_message(received_email, user._id)

        # Parse the ceremony information.
        proposed_ceremony: ProposedCeremony = self.__parse_proposed_ceremony(received_email)

        return user, message, proposed_ceremony
    
    def parse_content(self, received_email: dict) -> None:
        if received_email['frm'].__contains__(os.getenv('OUR_WEBSITE')):
            self.parser = OurSiteParser(received_email)
        else:
            self.parser = NefSiteParser(received_email)

        user_dict: dict = self.parser.parse_user()
        user: User = self.uc.create_user(user_dict)

        ceremony_dict: dict = self.parser.parse_ceremony()
        proposed_ceremony: ProposedCeremony = self.cc.create_proposed_ceremony(ceremony_dict)

        message: Message = model_from_dict(Message, {**received_email, 'user_id': user._id})
        self.mc.insert_message(message)
        return user, message, proposed_ceremony


    def get_email_info(self, received_email: dict) -> list:
        # message = model_from_dict(Message, received_email)
        user, message, proposed_ceremony = self.parse_content(received_email)
        # user, message, proposed_ceremony = self.__received_email_from_our_website(received_email)
        # else:
        #     user, message, proposed_ceremony = self.__received_email_from_other_source(received_email)
        # return user, message, proposed_ceremony
    
    def __received_email_from_other_source(self, received_email: dict):
        # name, received_email = message['frm'].split('<')
        # Clean the user name
        # name = name[0][:-1].replace('"', '')
        user: User = self.__parse_user(received_email)
        # Parse the message content and insert into the database if it doesn't exist already.
        message = self.__parse_message(received_email, user._id)
        proposed_ceremony: ProposedCeremony = self.__parse_proposed_ceremony(received_email)
        return user, message, proposed_ceremony
        

    @staticmethod
    def analyze_email_content(content: str):
        """Analyzes the content of an received_email."""

if __name__ == '__main__':
    our_site_test = {'_id': '183a82167e32ae99', 'frm': '"Ιωάννης Κασιδιάρης" <info@ktima-naias.gr>', 
                     '_to': 'ktimanaias@gmail.com', 'subject': 'Message from your website "[your-subject]"', 
                     '_datetime': 'Wed, 5 Oct 2022 12:31:43 +0000', 
                     'content': 'Ονομα: Ιωάννης Κασιδιάρης\r\n\r\nΗμερομηνία: 2202-10-05\r\n\r\nΆρ. Ατόμων: 1\r\n\r\nΕίδος Δεξίωσης: Γάμος\r\n\r\nΤηλέφωνο: 6939792174\r\n\r\nEmail: gk@eurodigital.gr\r\n\r\nΣχόλια: Παρακαλώ επιβεβαιώστε για την ορθή λήψη της φόρμας\r\n\r\n'}
    their_site_test = {'_id': '183a845adc21e967', 
                       'frm': 'maria louiza papadopoulou <maria_louiza@hotmail.com>', 
                       '_to': 'ktima naias <ktimanaias@gmail.com>', 
                       'subject': 'Πρ: New message from Παυλοπουλου Ξένια  KtimaNefeles.gr',
                       '_datetime': 'Wed, 5 Oct 2022 13:11:21 +0000', 
                       'content': '\r\n\r\nΕστάλη από το Outlook<http://aka.ms/weboutlook>\r\n\r\n________________________________\r\nΑπό: Κτήμα Νεφέλες <info@webproviders.gr>\r\nΣτάλθηκε: Τρίτη, 4 Οκτωβρίου 2022 4:56 μμ\r\nΠρος: maria_louiza@hotmail.com <maria_louiza@hotmail.com>\r\nΘέμα: New message from Παυλοπουλου Ξένια KtimaNefeles.gr\r\n\r\n\r\nΤο ονοματεπώνυμο σας::  Παυλοπουλου Ξένια\r\nΕνδιαφέρεστε για::      ΒΑΠΤΙΣΗ\r\nΗμερομηνία εκδήλωσης: : 25/08/2023\r\nΑριθμός ατόμων::        150\r\nΤηλέφωνο επικοινωνίας:: 6973769392\r\nΤο received_email σας::  Xenouladp@yahoo.com\r\nΤο μήνυμά σας: :        Ενδιαφέρομαι για μια βάπτιση 100 με 150 άτομα, ήθελα να ρωτήσω τιμές, παροχές, μενού κτλ. Ευχαριστώ.\r\n'}
    test_case = {'_id': '183ad45a37d36f13', 'frm': 'maria louiza papadopoulou <maria_louiza@hotmail.com>', '_to': 'ktima naias <ktimanaias@gmail.com>', 'subject': 'Πρ: New message from ΑΣΠΑΣΙΑ ΜΠΙΣΔΟΥΛΗ  KtimaNefeles.gr', '_datetime': 'Thu, 6 Oct 2022 12:29:24 +0000', 'content': '\r\n\r\nΕστάλη από το Outlook<http://aka.ms/weboutlook>\r\n\r\n________________________________\r\nΑπό: Κτήμα Νεφέλες <info@webproviders.gr>\r\nΣτάλθηκε: Πέμπτη, 6 Οκτωβρίου 2022 10:19 πμ\r\nΠρος: maria_louiza@hotmail.com <maria_louiza@hotmail.com>\r\nΘέμα: New message from ΑΣΠΑΣΙΑ ΜΠΙΣΔΟΥΛΗ KtimaNefeles.gr\r\n\r\n\r\nΤο ονοματεπώνυμο σας::  ΑΣΠΑΣΙΑ ΜΠΙΣΔΟΥΛΗ\r\nΕνδιαφέρεστε για::      ΓΑΜΟ\r\nΗμερομηνία εκδήλωσης: : 30/09/2023\r\nΑριθμός ατόμων::        130\r\nΤηλέφωνο επικοινωνίας:: 6984504101\r\nΤο email σας::  mpisdouli_aspasia@hotmail.com\r\nΤο μήνυμά σας: :        ΚΑΛΗΜΕΡΑ ΣΑΣ.ΘΑ ΗΘΕΛΑ ΣΑΣ ΠΑΡΑΚΑΛΩ ΝΑ ΜΟΥ ΑΠΟΣΤΕΙΛΕΤΕ ΤΙΜΕΣ ΓΙΑ ΓΑΜΟ ΣΥΟ ΕΚΚΛΗΣΑΚΙ ΤΟΥ ΚΤΗΜΑΤΟΣ ΜΕ ΕΠΑΚΟΛΟΥΘΟ ΤΡΑΠΕΖΙ ΣΤΟ ΚΤΗΜΑ ΓΙΑ ΠΕΡΙΠΟΥ 130 ΑΤΟΜΑ.\r\n'}
    ext = Extractor()
    for test in [test_case]:
        user, message = ext.get_email_info(test)
        # print(user, message)