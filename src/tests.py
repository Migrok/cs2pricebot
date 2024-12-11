from main import data_to_str
from parser import filter_data

test_data = {
    "1": {"pattern": "16614", "price": "1250 руб."},
    "2": {"pattern": "17429", "price": "1500 руб."},
    "3": {"pattern": "22000", "price": "1100 руб."},
    "4": {"pattern": "93000", "price": "2000 руб."},
    "5": {"pattern": "50000", "price": "1800 руб."},
    "6": {"pattern": "12000", "price": "800 руб."},
    "7": {"pattern": "95000", "price": "2100 руб."},
    "8": {"pattern": "10000", "price": "600 руб."},
    "9": {"pattern": "97000", "price": "2500 руб."},
    "10": {"pattern": "24001", "price": "1300 руб."},
}

def test_filter(data):
    filtered_data = filter_data(data)
    print(f"len(filtered_data) = {len(filtered_data)}")
    data_str = data_to_str(filtered_data)
    print(data_str)

test_filter(test_data)