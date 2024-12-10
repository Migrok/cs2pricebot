import requests
import json
import time
from bs4 import BeautifulSoup
from decouple import config

def download_json():
    borders = [0, 100, 200, 300]
    for i in range(len(borders)):
        url = f"https://steamcommunity.com/market/listings/730/Charm%20%7C%20Die-cast%20AK/render/?query=&start={borders[i]}&count=100&country=RU&language=russian&currency=5"
        response = requests.get(url)
        if response.status_code == 200:
            time.sleep(1)
            print(f"steam_data{i}.json data downloaded successfully.")
            with open(f"steam_data/steam_data{i}.json", "w", encoding="utf-8") as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=4)
            print(f"steam_data{i}.json saved.")
        else:
            print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")


def parse_prices():
    download_json()
    data = {}
    for i in range(4):
        print(f"Parsing №{i} start")
        with open(f"steam_data/steam_data{i}.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)
        results_html = json_data.get('results_html')
        soup = BeautifulSoup(results_html, 'html.parser')
        listings = soup.find_all('div', class_='market_listing_row')

        for listing in listings:
            listing_id = listing.get('id', 'unknown')

            pattern_tag = listing.find('div', class_='market_listing_row_details_attribute')
            pattern = None
            if pattern_tag:
                pattern_text = pattern_tag.get_text(strip=True)
                if "Шаблон брелка:" in pattern_text:
                    pattern = pattern_text.split(":")[-1].strip()

            price_tag = listing.find('span', class_='market_listing_price_with_fee')
            price = None
            if price_tag:
                price = price_tag.get_text(strip=True)

            data[listing_id] = {"pattern": pattern, "price": price}
        print(f"Parsing №{i} end")
    print(f"End parsing with len(data) = {len(data)}")

    filtered_data = filter_data(data)
    for listing_id, info in filtered_data.items():
        print(f"Шаблон: {info['pattern']} = {info['price']}")

    return data

def filter_data(data):
    filtered_data = {
        key: value
        for key, value in data.items()
        if value["pattern"] != None and (int(value["pattern"]) < 24000 or int(value["pattern"]) > 90000)
    }
    return filtered_data

parse_prices()
