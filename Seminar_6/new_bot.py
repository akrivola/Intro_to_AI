import telebot
from random import *
import json
import requests
films=[]

API_URL='https://7012.deeppavlov.ai/model'

API_TOKEN='6941923367:AAEPksjNLXq8nHs57NOx9lyoLmKw-eFOa_A'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
        films.append("Матрица")
        films.append("Солярис")
        films.append("Властелин колец")
        films.append("Техас")
        films.append("Санта Барбара")
        bot.send_message(message.chat.id,"Фильмотека была загружена по умолчанию!")

@bot.message_handler(commands=['all'])
def show_all(message):
    try:
        bot.send_message(message.chat.id,"Вот список фильмов:")
        bot.send_message(message.chat.id, ", ".join(films))
    except:
        bot.send_message(message.chat.id,"Фильмотека то пустая!")

@bot.message_handler(commands=['save'])
def save_all(message):
    with open("films.json","w",encoding="utf-8") as fh:
        fh.write(json.dumps(films,ensure_ascii=False))
    bot.send_message(message.chat.id,"Наша фильмотека успешно сохранена.")

@bot.message_handler(commands=['wiki'])
def wiki(message):
    quest = message.text.split()[1:]
    qq=" ".join(quest)
    data = { 'question_raw': [qq]}
    try:
        res = requests.post(API_URL,json=data,verify=False).json()
        bot.send_message(message.chat.id, res)
    except:
        bot.send_message(message.chat.id, "Что-то я ничего не нашел :-(")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if "дела" in message.text.lower():
        bot.send_message(message.chat.id, "Дела у меня хорошо, сам как?")

bot.polling()