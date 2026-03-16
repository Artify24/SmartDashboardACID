from fastapi import FastAPI
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

from generateKeywords import generate_keywords
from pageScrapper import scrape_justdial_page


app = FastAPI()


class ScrapeRequest(BaseModel):
    description: str
    location: str
    city: str


def get_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


@app.post("/scrape")
async def scrape_business(data: ScrapeRequest):

    # Generate JustDial keyword url part
    keyword_path = generate_keywords(
        business_location=data.location,
        description=data.description,
        city=data.city
    )[0]   # your function returns tuple

    url = f"https://www.justdial.com/{keyword_path}"

    driver = get_driver()
    driver.get(url)

    # scroll to load listings
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    results = driver.find_elements(By.CSS_SELECTOR, "div.resultbox")

    business_links = []
    for box in results:
        try:
            page = box.find_element(By.CSS_SELECTOR, "a[href]").get_attribute("href")
            business_links.append(page)
        except:
            continue

    scraped_data = []

    for link in business_links:
        try:
            scraped_data.append(scrape_justdial_page(link, driver))
        except:
            continue

    driver.quit()

    return {
        "count": len(scraped_data),
        "data": scraped_data
    }
