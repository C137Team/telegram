import telebot
import logging
from telebot import types
import requests
import logging
import sqlite3

logging.basicConfig(filename='c137bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print('bot online! prog main')
bot = telebot.TeleBot('6767096954:AAEUGBFSTDqQHW476WrBiMTwRBJ3PM8UJ14')
SERVER_URL = ['https://hack137.ru/reg/']

db = sqlite3.connect('ce137.db', check_same_thread=False)
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS incidents
             (chat_id INTEGER PRIMARY KEY,
             username TEXT,
            token TEXT, 
            rname TEXT)
             ''')


@bot.message_handler(commands=['start'])
def start(message):
    link = 'https://hack137.ru/'
    ss = f'<a href="{link}">САЙТЕ</a>'
    token = message.text.split(' ')[-1]
    chat_id = message.from_user.id
    user_name = message.from_user.username
    bot.send_message(message.chat.id, 'Приветствую!👋 \nЯ бот команды C-137. \nДождитесь пожалуйтста окончания авторизации...')
    logging.info(f"{user_name} ({chat_id}) start bot. Personal token: {token}")
    response = requests.post(SERVER_URL, data={'token': token})
    if response.status_code == 200 and response.json()['result'] == 'success':
        rname = response.json()['rname']
        bot.send_message(chat_id, f'Ваш аккаунт успешно авторизован! Добро пожаловать, {rname}!❤️ '
                                  f'\n Выберите, что вы хотите сделать👇')
    else:
        bot.send_message(chat_id, f'Пожалуйста, сначала авторизуйтесь у нас на {ss}')





bot.polling()