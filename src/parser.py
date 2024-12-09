from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_price():
    driver_path = "../chromedriver/chromedriver.exe"
    driver = webdriver.Chrome(service=Service(driver_path))

    url = "https://steamcommunity.com/market/listings/730/Charm%20%7C%20Die-cast%20AK"
    driver.get(url)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "market_listing_price"))
        )

        item_names = driver.find_elements(By.CLASS_NAME, "market_listing_row_details_attribute")[:10]
        prices = driver.find_elements(By.CLASS_NAME, "market_listing_price_with_fee")[:10]

        time.sleep(2)

        for i in range(min(10, len(item_names))):
            print(f"{item_names[i].text} = {prices[i].text}")
    finally:
        driver.quit()