from generateKeywords import generate_keywords
from pageScrapper import scrape_justdial_page
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def scrape_justdial(keyword_url):
    driver = get_driver()
    driver.get(f"https://www.justdial.com/{keyword_url}")

    time.sleep(3)

    all_links = set()

    # Scroll & collect
    for _ in range(6):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)

        results = driver.find_elements(By.CSS_SELECTOR, "div.resultbox a[href]")
        for r in results:
            try:
                link = r.get_attribute("href")
                if link and "justdial.com" in link and "/" in link:
                    all_links.add(link)
            except:
                continue

    print("Found business pages:", len(all_links))

    final_data = []

    for link in list(all_links)[:20]:   # limit to 20 to be safe
        try:
            print("Scraping:", link)
            info = scrape_justdial_page(link, driver)
            if info["name"]:
                final_data.append(info)
        except Exception as e:
            print("Failed:", e)

    driver.quit()
    return final_data


# Run scraper
keywords = generate_keywords("Thane-east", "handmade gifts", "Mumbai")[0]
data = scrape_justdial(keywords)
print(data)
