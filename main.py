from gmail_scraper import GMailScraper
from extract_info import Extractor
from controllers import MessageController

def main():
    gms = GMailScraper()
    for e in gms.crawl_emails(3):
        Extractor.extract_email_info(e)

if __name__ == "__main__":
    main()