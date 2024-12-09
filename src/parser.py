from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def parse_steam():
    print("start parsing")
    driver_path = "/usr/bin/chromedriver"
    driver = webdriver.Chrome(service=Service(driver_path))
    print("driver on")
    url = "https://steamcommunity.com/market/listings/730/Charm%20%7C%20Die-cast%20AK/render/?query=&start=0&count=100&country=RU&language=russian&currency=5"
    driver.get(url)
    price_data = ''

    try:
        print("trying to connect")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "market_listing_price"))
        )

        item_names = driver.find_elements(By.CLASS_NAME, "market_listing_row_details_attribute")[:20]
        prices = driver.find_elements(By.CLASS_NAME, "market_listing_price_with_fee")[:20]

        time.sleep(2)


        for i in range(min(10, len(item_names))):
            price_data += f"{item_names[i].text} = {prices[i].text}\n"
            print(f"{item_names[i].text} = {prices[i].text}")
    finally:
        print("closing driver")
        driver.quit()
    return price_data
