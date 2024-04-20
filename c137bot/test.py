import telebot
import logging
from telebot import types
import requests
import sqlite3

logging.basicConfig(filename='c137bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print('bot online! prog main')
bot = telebot.TeleBot('6767096954:AAEUGBFSTDqQHW476WrBiMTwRBJ3PM8UJ14')
SERVER_URL = 'https://hack137.ru/reg/'

db = sqlite3.connect('ce137.db', check_same_thread=False)
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS incidents
             (chat_id INTEGER PRIMARY KEY,
             username TEXT,
             fio TEXT,
             key TEXT)
             ''')

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    bot.send_message(message.chat.id, 'Приветствую!👋 \nЯ бот команды C-137 text text text text text text text text text text, войдите пожалуйста в ваш аккаунт ,)')
    logging.info(f"User {user_name} ({user_id}) start bot")
    msg = bot.send_message(message.chat.id, 'Пожалуйста, введите ключ, который вы получили на сайте:')
    bot.register_next_step_handler(msg, check_key, message.chat.id, message.from_user.username)

def check_key(message, chat_id, username):
    key = message.text
    response = requests.post(SERVER_URL, data={'key': key})
    if response.status_code == 200 and response.json()['result'] == 'success':
        user_fio = response.json()['fio']
        bot.send_message(chat_id, 'Вы успешно вошли в свой аккаунт!')
        cursor.execute("INSERT INTO incidents (chat_id, username, fio, key) VALUES (?, ?, ?, ?)", (chat_id, username, user_fio, key))
        db.commit()
    else:
        bot.send_message(chat_id, 'Ключ неверный. Попробуйте еще раз.')






bot.polling()