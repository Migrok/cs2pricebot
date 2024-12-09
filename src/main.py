import telebot
from decouple import config

bot = telebot.TeleBot(config('TOKEN'))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    with open('image.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)



if __name__ == '__main__':
    try:
        print("Бот запущен")
        bot.infinity_polling()
    except Exception as e:
        print(f"Ошибка: {e}")