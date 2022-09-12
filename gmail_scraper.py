import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for decoding messages in base64
from base64 import urlsafe_b64decode

from typing import Optional, List, Dict
from models.email import Email
from utils import model_from_dict

CLIENT_FILE = 'client.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']
# our_email = 'cloudanarchy@gmail.com'


class GMailScraper:

    def __init__(self) -> None:
        # sourcery skip: raise-specific-error
        # load_dotenv()
        try:
            self.query: str = os.getenv('QUERY')
        except:
            raise Exception("Could not parse correctly enviroment variables.")

        # Authenticate and create service
        self.service = GMailScraper.gmail_authenticate()
        # get emails that match the query you specify
        self.messages = self.search_messages(query=self.query)
        # results = self.search_messages("from:maria_louiza@hotmail.com")
        # results = search_messages(service, "Python Code")
        print(f"Found {len(self.messages)} messages.")
        # for each email matched, read it (output plain/text to console & save HTML and attachments)
    
    def crawl_emails(self, n: Optional[int] = None) -> Email:
        if n is None:
            n = len(self.messages)
        for msg in self.messages[:n]:
            yield self.read_message(msg)

    def search_messages(self, query: str):
        result = self.service.users().messages().list(userId='me', q=query).execute()
        messages = []
        if 'messages' in result:
            messages.extend(result['messages'])
        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = self.service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
            if 'messages' in result:
                messages.extend(result['messages'])
        return messages

    @staticmethod
    def gmail_authenticate():
        creds = None
        # the file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        # if there are no (valid) credentials availablle, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
        return build('gmail', 'v1', credentials=creds)

    # Got code from
    # https://www.thepythoncode.com/article/use-gmail-api-in-python#Enabling_Gmail_API
    def read_message(self, message) -> Email:
        """
        This function takes Gmail API `service` and the given `message_id` and does the following:
            - Downloads the content of the email
            - Prints email basic information (To, From, Subject & Date) and plain/text parts
            - Creates a folder for each email based on the subject
            - Downloads text/html content (if available) and saves it under the folder created as index.html
            - Downloads any file that is attached to the email and saves it in the folder created
        """
        msg = self.service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        # parts can be the message body, or attachments
        payload = msg['payload']
        headers = payload.get("headers")
        parts = payload.get("parts")
        email_dict: Dict[str, str, str, str, str] = {'frm': '', 'to': '', 'subject': '', 'datetime': '', 'content': ''}
        if headers:
            # this section prints email basic info & creates a folder for the email
            for header in headers:
                name = header.get("name")
                value = header.get("value")
                if name.lower() == 'from':
                    # we print the From address
                    print("From:", value)
                    email_dict['frm'] = value
                if name.lower() == "to":
                    # we print the To address
                    print("To:", value)
                    email_dict['to'] = value
                if name.lower() == "subject":
                    print("Subject:", value)
                    email_dict['subject'] = value
                if name.lower() == "date":
                    # we print the date when the message was sent
                    print("Date:", value)
                    email_dict['datetime'] = value

        # if not has_subject and not os.path.isdir(folder_name):
        #     # if the email does not have a subject, then make a folder with "email" name
        #     # since folders are created based on subjects
        #     os.mkdir(folder_name)
        if parts is not None:
            content_list: List[str] = []
            self.parse_parts(parts, message, content_list)
            content = ''.join(content_list)
        else:
            content = parse_msg(msg)
        email_dict['content'] = content
        print("=" * 50)
        return model_from_dict(Email, email_dict)

    def parse_parts(self, parts, message, content_list: List[str]):
        """
        Utility function that parses the content of an email partition
        """
        if not parts:
            return
        for part in parts:
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            if part.get("parts"):
                # recursively call this function when we see 
                # that a part has parts inside
                self.parse_parts(part.get("parts"), message)
            if mimeType == "text/plain" and data:
                text = urlsafe_b64decode(data).decode()
                content_list.append(text)

def parse_msg(msg) -> str:
    if msg.get("payload").get("body").get("data"):
        return urlsafe_b64decode(msg.get("payload").get("body").get("data").encode("ASCII")).decode("utf-8")
    return msg.get("snippet")