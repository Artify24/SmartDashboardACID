from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse

BLOCKED_DOMAINS = [
    "wix.com",
    "wordpress.com",
    "notion.site",
    "medium.com",
    "blog",
    "webflow.io",
    "carrd.co",
    "g2.com",
    "capterra.com"
]

def is_valid_business_site(url, brand):
    domain = urlparse(url).netloc.lower()

    if not domain:
        return False

    # Block obvious junk
    for blocked in BLOCKED_DOMAINS:
        if blocked in domain:
            return False

    # Brand should roughly match domain
    return brand.lower() in domain


def get_target_website(request, driver, wait):
    # 1. If website link exists, trust it
    if request.get("websiteLink"):
        return request["websiteLink"]

    brand = request["name"]
    query = f"{brand} official website"

    driver.get(f"https://duckduckgo.com/html/?q={query}")

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.result__a")))

    results = driver.find_elements(By.CSS_SELECTOR, "a.result__a")

    for result in results[:5]:  # only check top 5
        url = result.get_attribute("href")
        if is_valid_business_site(url, brand):
            return url

    return None  # let caller handle failure
