import telebot
import threading
import time
import json
import os
from decouple import config
from parser import parse, get_actual_filtered_data, filter_data

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
    bot.send_message(message.chat.id, "Вы подписались на уведомления!")
    print(f"\nUser {message.chat.id} subscribed.\n")

@bot.message_handler(commands=['parse'])
def get_prices(message):
    pattern_price_str = data_to_str(get_actual_filtered_data())
    bot.reply_to(message, f"Лоты с шаблоном <24000 и >90000:\n{pattern_price_str}")

@bot.message_handler(commands=["stop"])
def stop_command(message):
    if message.chat.id in subscribers:
        subscribers.remove(message.chat.id)
        save_subscribers()
        bot.send_message(message.chat.id, "Вы отписались от уведомлений.")
        print(f"User {message.chat.id} unsubscribed.")
    else:
        bot.send_message(message.chat.id, "Вы не были подписаны.")

@bot.message_handler(commands=["shutdown"])
def shutdown_command(message):
    if str(message.chat.id) == config("ADMIN_ID"):
        bot.reply_to(message, "Бот отключается...")
        os._exit(0)
    else:
        bot.reply_to(message, "У вас нет прав на выполнение этой команды.")

@bot.message_handler(commands=["work"])
def work_command(message):
    bot.reply_to(message, "Бот работает.")

def data_to_str(data_dict):
    data_list = []
    for listing_id, info in data_dict.items():
        pattern = info["pattern"] if info["pattern"] else "None"
        price = info["price"]
        position = info["position"]
        if int(info["pattern"]) < 24000 and int(info["pattern"]) >= 20000:
            data_list.append(f"Позиция {position}: 🟥Шаблон: {pattern} = {price}")
        elif int(info["pattern"]) < 20000 and int(info["pattern"]) >= 6000:
            data_list.append(f"Позиция {position}: 🟧Шаблон: {pattern} = {price}")
        elif int(info["pattern"]) < 6000:
            data_list.append(f"Позиция {position}: 🟨Шаблон: {pattern} = {price}")
        elif int(info["pattern"]) > 90000:
            data_list.append(f"Позиция {position}: 🟦Шаблон: {pattern} = {price}")
    data_str = "\n".join(data_list)
    return data_str

def send_notifications(data):
    filtered_data = filter_data(data)
    count_data = len(filtered_data)
    data_str = data_to_str(filtered_data)
    for chat_id in subscribers:
        try:
            if count_data != 0:
                if count_data == 1:
                    bot.send_message(chat_id, f"Выставлен новый лот:\n{data_str}")
                else:
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
        periodic_parsing(10, parse)
        bot.infinity_polling()
    except Exception as e:
        print(f"Ошибка: {e}")

