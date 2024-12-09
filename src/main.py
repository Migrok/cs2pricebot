import telebot
from decouple import config
from parser import parse_prices

bot = telebot.TeleBot(config('TOKEN'))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    with open('image.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['parse'])
def get_prices(message):
    bot.reply_to(message, "Паршу")
    pattern_price_str = pattern_price_dict_to_str(parse_prices())
    bot.reply_to(message, f"{pattern_price_str}")

def pattern_price_dict_to_str(pattern_price_dict):
    pattern_price_str = ""
    for key, value in pattern_price_dict.items():
        pattern_price_str += f"{key} = {value}\n"
    return pattern_price_str


if __name__ == '__main__':
    try:
        print("Бот запущен")
        bot.infinity_polling()
    except Exception as e:
        print(f"Ошибка: {e}")