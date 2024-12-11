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
            time.sleep(2)
            print(f"steam_data{i}.json data downloaded successfully.")
            with open(f"steam_data/steam_data{i}.json", "w", encoding="utf-8") as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=4)
            print(f"steam_data{i}.json saved.")
        else:
            print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")


def parse_prices():
    download_json()
    data = {}
    position = 1
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

            data[listing_id] = {"position": position, "pattern": pattern, "price": price}
            position += 1
        print(f"Parsing №{i} end")
    print(f"End parsing with len(data) = {len(data)}")

    return data

def filter_data(data):
    filtered_data = {
        key: value
        for key, value in data.items()
        if value["pattern"] != None and (int(value["pattern"]) < 24000 or int(value["pattern"]) > 90000)
    }
    return filtered_data

def exclude_existing_keys(new_data):
    old_data = get_old_data()
    print(f"len(old_data) = {len(old_data)}")
    unique_data = {
        key: value for key, value in new_data.items() if key not in old_data
    }
    if len(unique_data) == 0:
        unique_data = 0

    old_data.update(new_data)
    #old_data = new_data
    save_new_data(old_data)

    return unique_data

def parse():
    data = parse_prices()
    save_actual_data(data)
    unique_data = exclude_existing_keys(data)
    if unique_data == 0:
        print("\nThere is no new data.")
    else:
        print("\nThere is a new data!")
        for key, value in unique_data.items():
            print(f"ID: {key}, Позиция {value['position']}:  Шаблон: {value['pattern']}, Цена: {value['price']}")
    print()
    return unique_data

def get_old_data():
    old_data_file = "steam_data/old_data.json"
    try:
        with open(old_data_file, "r", encoding="utf-8") as f:
            old_data = json.load(f)
    except FileNotFoundError:
        old_data = {}
    return old_data

def get_actual_data():
    actual_data_file = "steam_data/actual_data.json"
    try:
        with open(actual_data_file, "r", encoding="utf-8") as f:
            actual_data = json.load(f)
    except FileNotFoundError:
        actual_data = {}
    return actual_data

def save_new_data(new_data):
    old_data_file = "steam_data/old_data.json"
    with open(old_data_file, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)

def save_actual_data(actual_data):
    actual_data_file = "steam_data/actual_data.json"
    with open(actual_data_file, "w", encoding="utf-8") as f:
        json.dump(actual_data, f, ensure_ascii=False, indent=4)

def get_old_filtered_data():
    data = get_old_data()
    filtered_data = filter_data(data)
    return filtered_data

def get_actual_filtered_data():
    data = get_actual_data()
    filtered_data = filter_data(data)
    return filtered_data
