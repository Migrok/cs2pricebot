import telebot
import threading
import time
import json
from decouple import config
from parser import parse

bot = telebot.TeleBot(config('TOKEN'))

SUBSCRIBERS_FILE = "subscribers.json"

def load_subscribers():
    try:
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_subscribers():
    with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(subscribers), f, ensure_ascii=False, indent=4)

subscribers = load_subscribers()
@bot.message_handler(commands=['start'])
def send_welcome(message):
    subscribers.add(message.chat.id)
    save_subscribers()
    with open('image.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    print(f"\nUser {message.chat.id} subscribed.\n")

#@bot.message_handler(commands=['parse'])
#def get_prices(message):
#    bot.reply_to(message, "Паршу")
#    pattern_price_str = pattern_price_dict_to_str(parse_prices())
#    bot.reply_to(message, f"{pattern_price_str}")

def data_to_str(data_dict):
    data_list = []
    for listing_id, info in data_dict.items():
        pattern = info["pattern"] if info["pattern"] else "None"
        price = info["price"]
        data_list.append(f"Шаблон: {pattern} = {price}")

    data_str = "\n".join(data_list)
    return data_str

def send_notifications(data):
    data_str = data_to_str(data)
    for chat_id in subscribers:
        try:
            bot.send_message(chat_id, f"Выставлены новые лоты:\n{data_str}")
        except Exception as e:
            print(f"Ошибка отправки уведомления пользователю {chat_id}: {e}")

def periodic_parsing(interval, parse):
    def wrapper():
        while True:
            try:
                new_data = parse()
                if new_data != 0:
                    send_notifications(new_data)
            except Exception as e:
                print(f"Ошибка в задаче: {e}")
            time.sleep(interval)

    thread = threading.Thread(target=wrapper, daemon=True)
    thread.start()

if __name__ == '__main__':
    try:
        print("Бот запущен!")
        periodic_parsing(20, parse)
        bot.infinity_polling()
    except Exception as e:
        print(f"Ошибка: {e}")