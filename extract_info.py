import os
import re
from parser import MelanSiteParser, NefSiteParser, OurSiteParser
from typing import List, TypeVar

# Used to access the .env file
from dotenv import load_dotenv

from controllers import (MessageController, ProposedCeremonyController,
                         UserController)
from models import Message, ProposedCeremony, User, proposed_ceremony
from utils import model_from_dict, remove_spaces

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
    
    def parse_content(self, received_email: dict) -> None | tuple[dict, dict, dict]:

        # Remove special character that breaks SQL queries.
        received_email['content'] = received_email['content'].replace("'", '')

        # Pick the correct parser.
        if received_email['frm'].__contains__(os.getenv('OUR_WEBSITE')):
            self.parser = OurSiteParser(received_email)
        elif received_email['subject'].__contains__(os.getenv('MELAN_WEBSITE')):
            self.parser = MelanSiteParser(received_email)
        elif received_email['subject'].__contains__(os.getenv('NEF_WEBSITE')):
            self.parser = NefSiteParser(received_email)
        else:
            return None, None, None
            # raise Exception('Received email from unknown source: ', received_email['frm'])

        user_dict: dict = self.parser.parse_user()
        user: User = self.uc.create_user(user_dict)

        ceremony_dict: dict = self.parser.parse_ceremony()
        ceremony_dict['msg_id'] = received_email['_id']
        ceremony_dict['user_id'] = user._id 
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
        return user, message, proposed_ceremony
    
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
    our_new_site = {'_id': '184294e4d380cba5', 
                'frm': 'test <info@ktima-naias.gr>', 
                '_to': 'info@ktima-naias.gr', 
                'subject': 'Κτήμα Ναϊάς | Γάμος - Βάπτιση - Εκδήλωση "Εκδήλωση ενδιαφέροντος"', 
                '_datetime': 'Sun, 30 Oct 2022 14:31:46 +0000', 
                'content': 'Από: test <kok@k.com>\r\nΗμερομηνία Ενδιαφέροντος: 2022-10-17\r\nΑριθμός Ατόμων: 99999999999999999999999999999999999999999999\r\nΕίδος Δεξίωσης: Γάμος\r\nΤηλέφωνο Επικοινωνίας: 8\r\n\r\nΣχόλια:\r\nokokj\r\n\r\n-- \r\nΑυτό το μήνυμα ηλεκτρονικού ταχυδρομείου στάλθηκε από την φόρμα επικοινωνίας του Κτήμα Ναϊάς | Γάμος - Βάπτιση - Εκδήλωση (https://ktima-naias.gr)\r\n\r\n'}
    our_old_site = {'_id': '183ec32cdb2e5524',
                 'frm': '"ΜΑΡΙΝΑ ΛΕΒΕΝΤΗ" <info@ktima-naias.gr>',
                 '_to': 'ktimanaias@gmail.com',
                 'subject': 'Message from your website "[your-subject]"', 
                 '_datetime': 'Tue, 18 Oct 2022 17:44:55 +0000', 
                 'content': 'Ονομα: ΜΑΡΙΝΑ ΛΕΒΕΝΤΗ\r\n\r\nΗμερομηνία: 2023-06-24\r\n\r\nΆρ. Ατόμων: 160\r\n\r\nΕίδος Δεξίωσης: Γάμος\r\n\r\nΤηλέφωνο: 6942681039\r\n\r\nEmail: marleventi@gmail.com\r\n\r\nΣχόλια: Καλησπέρα,\r\n\r\nΘα μας ενδιέφερε να πραγματοποιησουμε γάμο-βάπτιση στο χώρος σας, 150-180 άτομα, Παρασκευή ή Σάββατο, από αρχές Ιουνίου έως και μέσα Ιουλίου και από τέλος Αυγούστου έως και τέλος Σεπτεμβρίου. \r\nΕκτός από τη δεξίωση, θα θέλαμε και το μυστήριο να πραγματοποιηθεί στο χώρο σας.\r\n\r\nΠαρακαλώ όπως μας ενημερώσετε για διαθεσιμότητες και προσφορές.\r\n\r\nΠαραμένω στη διάθεση σας.\r\n\r\nΦιλικά,\r\nΜαρίνα Λεβέντη\r\n6942681039\r\n\r\n'}
    our_old_site_case2 = {'_id': '180f1e8323ade8d7',
                          'frm': '"Ειρήνη Μωραΐτη" <info@ktima-naias.gr>', 
                          '_to': 'ktimanaias@gmail.com', 
                          'subject': 'Message from your website "[your-subject]"', 
                          '_datetime': 'Mon, 23 May 2022 17:12:46 +0000', 
                          'content': 'Ονομα: Ειρήνη Μωραΐτη\r\n\r\nΗμερομηνία: 2023-06-24\r\n\r\nΆρ. Ατόμων: 250.300\r\n\r\nΕίδος Δεξίωσης: Γάμος\r\n\r\nΤηλέφωνο: 6983122965\r\n\r\nEmail: eirhnh.moraith@gmail.com\r\n\r\nΣχόλια: Καλησπέρα σας,\r\nΠαρακαλώ όπως μου αποστείλετε μια οικονομική προσφορά.\r\n\r\nΣας ευχαριστώ.\r\n\r\n'}
    nef_case = {'_id': '183a845adc21e967', 
                       'frm': 'maria louiza papadopoulou <maria_louiza@hotmail.com>', 
                       '_to': 'ktima naias <ktimanaias@gmail.com>', 
                       'subject': 'Πρ: New message from Παυλοπουλου Ξένια  KtimaNefeles.gr',
                       '_datetime': 'Wed, 5 Oct 2022 13:11:21 +0000', 
                       'content': '\r\n\r\nΕστάλη από το Outlook<http://aka.ms/weboutlook>\r\n\r\n________________________________\r\nΑπό: Κτήμα Νεφέλες <info@webproviders.gr>\r\nΣτάλθηκε: Τρίτη, 4 Οκτωβρίου 2022 4:56 μμ\r\nΠρος: maria_louiza@hotmail.com <maria_louiza@hotmail.com>\r\nΘέμα: New message from Παυλοπουλου Ξένια KtimaNefeles.gr\r\n\r\n\r\nΤο ονοματεπώνυμο σας::  Παυλοπουλου Ξένια\r\nΕνδιαφέρεστε για::      ΒΑΠΤΙΣΗ\r\nΗμερομηνία εκδήλωσης: : 25/08/2023\r\nΑριθμός ατόμων::        150\r\nΤηλέφωνο επικοινωνίας:: 6973769392\r\nΤο received_email σας::  Xenouladp@yahoo.com\r\nΤο μήνυμά σας: :        Ενδιαφέρομαι για μια βάπτιση 100 με 150 άτομα, ήθελα να ρωτήσω τιμές, παροχές, μενού κτλ. Ευχαριστώ.\r\n'}

    test_case = {'_id': '183ad45a37d36f13', 'frm': 'maria louiza papadopoulou <maria_louiza@hotmail.com>', '_to': 'ktima naias <ktimanaias@gmail.com>', 'subject': 'Πρ: New message from ΑΣΠΑΣΙΑ ΜΠΙΣΔΟΥΛΗ  KtimaNefeles.gr', '_datetime': 'Thu, 6 Oct 2022 12:29:24 +0000', 'content': '\r\n\r\nΕστάλη από το Outlook<http://aka.ms/weboutlook>\r\n\r\n________________________________\r\nΑπό: Κτήμα Νεφέλες <info@webproviders.gr>\r\nΣτάλθηκε: Πέμπτη, 6 Οκτωβρίου 2022 10:19 πμ\r\nΠρος: maria_louiza@hotmail.com <maria_louiza@hotmail.com>\r\nΘέμα: New message from ΑΣΠΑΣΙΑ ΜΠΙΣΔΟΥΛΗ KtimaNefeles.gr\r\n\r\n\r\nΤο ονοματεπώνυμο σας::  ΑΣΠΑΣΙΑ ΜΠΙΣΔΟΥΛΗ\r\nΕνδιαφέρεστε για::      ΓΑΜΟ\r\nΗμερομηνία εκδήλωσης: : 30/09/2023\r\nΑριθμός ατόμων::        130\r\nΤηλέφωνο επικοινωνίας:: 6984504101\r\nΤο email σας::  mpisdouli_aspasia@hotmail.com\r\nΤο μήνυμά σας: :        ΚΑΛΗΜΕΡΑ ΣΑΣ.ΘΑ ΗΘΕΛΑ ΣΑΣ ΠΑΡΑΚΑΛΩ ΝΑ ΜΟΥ ΑΠΟΣΤΕΙΛΕΤΕ ΤΙΜΕΣ ΓΙΑ ΓΑΜΟ ΣΥΟ ΕΚΚΛΗΣΑΚΙ ΤΟΥ ΚΤΗΜΑΤΟΣ ΜΕ ΕΠΑΚΟΛΟΥΘΟ ΤΡΑΠΕΖΙ ΣΤΟ ΚΤΗΜΑ ΓΙΑ ΠΕΡΙΠΟΥ 130 ΑΤΟΜΑ.\r\n'}
    melan_case = {'_id': '18452a64f81931aa', 
                 'frm': 'maria louiza papadopoulou <maria_louiza@hotmail.com>', 
                 '_to': 'ktima naias <ktimanaias@gmail.com>', 
                 'subject': 'Fwd New message from "Ktima Melanthia"', 
                 '_datetime': 'Mon, 7 Nov 2022 15:12:21 +0000', 'content': '\r\n\r\nΛήψη Outlook για Android<https://aka.ms/AAb9ysg>\r\n________________________________\r\nFrom: Ktima Melanthia <info@webproviders.gr>\r\nSent: Sunday, November 6, 2022 6:15:58 PM\r\nTo: kkatsimigas@foodandstyle.gr <kkatsimigas@foodandstyle.gr>; info@webproviders.gr <info@webproviders.gr>; maria_louiza@hotmail.com <maria_louiza@hotmail.com>; kkatsimigas@yahoo.gr <kkatsimigas@yahoo.gr>\r\nSubject: New message from "Ktima Melanthia"\r\n\r\nΤο ονοματεπώνυμο σας: *: veronica vlahou\r\nΤο email σας: *: veronicavlahou@yahoo.com\r\nΕνδιαφέρεστε για: *: Γάμο\r\nΗμερομηνία εκδήλωσης:*: 2023-06-10\r\nΑριθμός ατόμων: *: 150\r\nΤηλέφωνο επικοινωνίας: *: 6984116207\r\nΤο μήνυμά σας: *: Klaispera sas,\r\n\r\nEndiaferomaste gia gamo ston xwro sas me 150 kalesmenous.\r\n\r\nDen exoume orisei imerominia, kata protimisi omws ta Savvata tou Iouniou,Ioyliou kai Septemvriou to 2023 mas endiaferoun.\r\n\r\nAnamenoume tin apantisei sas!\r\nMe ektimisi,\r\n\r\nVeronica Vlahou\r\n6984116207\r\n\r\n---\r\n\r\nDate: 6 Νοεμβρίου, 2022\r\nTime: 4:15 μμ\r\nPage URL: https://ktimamelanthia.gr/\r\n\r\n'}
    ext = Extractor()
    for test in [our_old_site_case2]:
        user, message, ceremony = ext.get_email_info(test)
        # print(user, message)