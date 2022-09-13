from models import Message, User

class Extractor:
    
    @staticmethod
    def extract_from_email_content(message: Message):
        """Extracts information from an email."""
        if message.subject == 'Message from your website "[your-subject]"':
            Extractor.email_from_our_website(message)
        print(message)
        print()
    
    @staticmethod
    def email_from_our_website(message: Message):
        User()

    @staticmethod
    def analyze_email_content(content: str):
        """Analyzes the content of an email."""
