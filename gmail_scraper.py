import os
import pickle
from dotenv import load_dotenv

# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for decoding messages in base64
from base64 import urlsafe_b64decode

from typing import Optional, List, Dict, Any
from models.message import Message
from utils import model_from_dict

CLIENT_FILE = 'client.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']


class GMailScraper:

    def __init__(self) -> None:
        # sourcery skip: raise-specific-error
        load_dotenv()
        self.query: str
        try:
            self.query: str = str(os.getenv('QUERY'))
        except:
            raise Exception("Could not parse correctly enviroment variables.")

        # Authenticate and create service
        self.service = GMailScraper.gmail_authenticate()
        # get emails that match the query you specify
        self.messages: list = self.search_messages()
        # results = search_messages(service, "Python Code")
        # for each email matched, read it (output plain/text to console & save HTML and attachments)
    
    def crawl_emails(self, n: Optional[int] = None) -> Message:
        if n is None:
            n = len(self.messages)
        for msg in self.messages[:n]:
            yield self.read_message(msg)

    def search_messages(self, query: Optional[str] = None):
        if query is None:
            if self.query is None:
                raise Exception('No query given or found')
            query = self.query
        result = self.service.users().messages().list(userId='me', q=query).execute()
        messages = []
        if 'messages' in result:
            messages.extend(result['messages'])
        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = self.service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
            if 'messages' in result:
                messages.extend(result['messages'])
        print(f"Found {len(messages)} messages.")
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
                # Maybe because of Brave browser or wsl2 openning the browser function hungs.
                # So simple prompt to show the url in the terminal window and click it from there.
                creds = flow.run_local_server(port=0, open_browser=False)
            # save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
        return build(API_NAME, API_VERSION, credentials=creds)

    # Got code from
    # https://www.thepythoncode.com/article/use-gmail-api-in-python#Enabling_Gmail_API
    def read_message(self, message) -> dict:
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
        msg_dict: Dict[str, str, str, str, str, str] = {'_id': '', 'frm': '', '_to': '', 'subject': '', '_datetime': '', 'content': ''}
        if headers:
            # this section prints email basic info & creates a folder for the email
            for header in headers:
                name = header.get("name")
                value = header.get("value")
                match name.lower():
                    case 'from':
                        msg_dict['frm'] = value
                    case 'to':
                        msg_dict['_to'] = value
                    case 'subject':
                        msg_dict['subject'] = value
                    case 'date':
                        msg_dict['_datetime'] = value
        
        if msg_dict['_id'] == '':
            msg_dict['_id'] = message.get('id')
        
        # Get the message content/body
        if parts is not None:
            content_list: List[str] = []
            self.parse_parts(parts, message, content_list)
            content = ''.join(content_list)
        else:
            content = parse_msg(msg)
        msg_dict['content'] = content
        print(msg_dict)
        print("=" * 50)
        return msg_dict

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
                self.parse_parts(part.get("parts"), message, content_list)
            if mimeType == "text/plain" and data:
                text = urlsafe_b64decode(data).decode()
                content_list.append(text)

def parse_msg(msg) -> str:
    if msg.get("payload").get("body").get("data"):
        return urlsafe_b64decode(msg.get("payload").get("body").get("data").encode("ASCII")).decode("utf-8")
    return msg.get("snippet")