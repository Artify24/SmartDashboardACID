from scraper import AdvancedBusinessScraper
with AdvancedBusinessScraper() as s:
    data = s.scrape_website("https://www.notion.com/")