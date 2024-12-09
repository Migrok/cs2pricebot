import telebot
from decouple import config
from parser import parse_steam

bot = telebot.TeleBot(config('TOKEN'))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    with open('image.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['parse'])
def get_prices(message):
    bot.reply_to(message, "Паршу")
    price_data = parse_steam()
    bot.reply_to(message, f"{price_data}")


if __name__ == '__main__':
    try:
        print("Бот запущен")
        bot.infinity_polling()
    except Exception as e:
        print(f"Ошибка: {e}")