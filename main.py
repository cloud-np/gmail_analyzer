from gmail_scraper import GMailScraper
from extract_info import Extractor
from controllers import MessageController

def main():
    gms = GMailScraper()
    msg_con: MessageController = MessageController()
    for msg in gms.crawl_messages(10):
        msg_con.insert_message(msg)
        # print(msg)
        # Extractor.extract_email_info(msg)
    msg_con.close_db()

def test():
    msg_con: MessageController = MessageController()
    pd = msg_con.get_all_messages()
    print(pd)
    msg_con.close_db()

if __name__ == "__main__":
    # main()
    test()