from gmail_scraper import GMailScraper

gms = GMailScraper()
for e in gms.crawl_emails(3):
    print('\n\n\n')
    print(e)
    print('\n\n\n')