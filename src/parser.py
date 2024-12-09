import requests
import json
from bs4 import BeautifulSoup

def download_json():
    url = "https://steamcommunity.com/market/listings/730/Charm%20%7C%20Die-cast%20AK/render/?query=&start=0&count=100&country=RU&language=russian&currency=5"
    response = requests.get(url)
    if response.status_code == 200:
        print("JSON data downloaded successfully.")
        with open("steam_data.json", "w", encoding="utf-8") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
        print("File saved as steam_data.json")
    else:
        print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")


def parse_prices():
    pattern_price_dict = {}
    download_json()
    print("Opening JSON data")
    with open("steam_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    results_html = data.get('results_html')
    if results_html:
        soup = BeautifulSoup(results_html, 'html.parser')
        print("Parsing")
        prices = soup.find_all(class_='market_listing_price market_listing_price_with_fee')
        patterns = soup.find_all(class_='market_listing_row_details_attribute')
        print("Count of patterns = ", len(patterns))
        print("Count of prices = ", len(prices))
        for pattern, price in zip(patterns, prices):
            pattern_text = pattern.get_text(strip=True).replace("Шаблон брелка: ", "")
            price_text = price.get_text(strip=True)
            if price_text == "Продано!":
                continue
            pattern_price_dict[pattern_text] = price_text
    else:
        print("Ключ 'results_html' не найден в JSON.")
    return pattern_price_dict

