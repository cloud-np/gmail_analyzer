from gmail_scraper import GMailScraper
from extract_info import Extractor
from models import User, message

def main():
    gms = GMailScraper()
    ext = Extractor()
    for e in gms.crawl_emails(6):
        user, message, proposed_ceremony = ext.get_email_info(e)
        print(user)
        print(message)
        print(proposed_ceremony)
        # user, msg = ext.get_email_info(e)
    # print(msc.get_all_messages())

if __name__ == "__main__":
    # msc.create_messages_table()
    main()
    # usc.create_users_table()
    # print(usc.get_all_users())
    # # usc.insert_user('ep@gmail.com', 'nk', 'po')
    # usc.insert_user('ep@gmail.com', 'nk', 'po')
    # print(usc.get_all_users())