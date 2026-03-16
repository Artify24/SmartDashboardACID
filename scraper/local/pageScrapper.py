from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def scrape_justdial_page(page_link, driver):
    wait = WebDriverWait(driver, 25)
    data = {}

    driver.get(page_link)

    # Force React hydration
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(3)

    # Scroll to activate dynamic sections
    driver.execute_script("window.scrollBy(0, 600)")
    time.sleep(2)

    # ------------------------------------
    # BUSINESS NAME (MULTI-FALLBACK)
    # ------------------------------------
    name = None

    selectors = [
        "h1",
        "h1 span",
        "div[role='heading']",
        "div[class*='business'] h1"
    ]

    for sel in selectors:
        try:
            el = driver.find_element(By.CSS_SELECTOR, sel)
            text = el.text.strip()
            if text:
                name = text
                break
        except:
            continue

    data["name"] = name

    # ------------------------------------
    # QUICK INFO (LABEL → VALUE)
    # ------------------------------------
    quick_info = {}

    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.dtl_infolist_item")
            )
        )

        items = driver.find_elements(By.CSS_SELECTOR, "div.dtl_infolist_item")

        for item in items:
            try:
                label = item.find_element(By.CSS_SELECTOR, "div.dtl_labeltext").text.strip()
                value = item.find_element(By.CSS_SELECTOR, "div.dtl_infotext").text.strip()
                quick_info[label] = value
            except:
                continue
    except:
        pass

    data["quick_info"] = quick_info

    # ------------------------------------
    # WEBSITE
    # ------------------------------------
    websites = set()
    for a in driver.find_elements(By.CSS_SELECTOR, "a[href]"):
        href = a.get_attribute("href")
        if href and href.startswith("http") and "justdial" not in href:
            websites.add(href)

    data["website"] = list(websites)

    # ------------------------------------
    # RATING + COUNT
    # ------------------------------------
    try:
        data["rating"] = driver.find_element(By.CSS_SELECTOR, "div.green_box").text.strip()
    except:
        data["rating"] = None

    try:
        data["total_ratings"] = driver.find_element(
            By.XPATH, "//*[contains(text(),'Ratings')]"
        ).text.strip()
    except:
        data["total_ratings"] = None

    # ------------------------------------
    # TOP 5 REVIEWS
    # ------------------------------------
    reviews = []

    try:
        review_boxes = driver.find_elements(By.CSS_SELECTOR, "div.review_box")[:5]

        for box in review_boxes:
            try:
                user = box.find_element(By.TAG_NAME, "h3").text.strip()
            except:
                user = None

            try:
                text = box.find_element(By.TAG_NAME, "q").text.strip()
            except:
                text = None

            reviews.append({
                "user": user,
                "review": text
            })
    except:
        pass

    data["reviews"] = reviews

    return data
