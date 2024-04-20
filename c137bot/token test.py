import telebot
import sqlite3

bot = telebot.TeleBot('6767096954:AAEUGBFSTDqQHW476WrBiMTwRBJ3PM8UJ14')
@bot.message_handler(commands=['start'])
def start(message):
    token = message.text.split(' ')[-1]
    bot.send_message(message.chat.id, f"Ваш токен '{token}' успешно сохранен в базе данных.")
if __name__ == '__main__':
    bot.polling(none_stop=True)