# Домашнее задание к семинару №6 (Сферы применения искусственного интеллекта)

# Реальная задача для моей текущей работы: 

# Написать телеграм-бота который должен будет работать в нашем чате Helpdesk для пользователей компании Автобаки
# и по запросу пользователя добавлять новый тикет на решения проблемы, а если от того же пользователя будет
# еще вопрос, то писать ему номер уже открытого тикета. Также по запросу выводить список открытых тикетов.

# Делаю пока основу для этого бота, очень примитивную, в дальнейшем доработаю его и буду реально использовать

# Импортируем библиотеки
import requests
import telebot
from random import *

# Для добавления поиска решений часто встречающихся проблем пользователей Windows в запросе пользователя
# лучше задействовать какую нибудь другую AI систему, например на базе Алисы от Яндекс, можно воспользоваться
# API Яндекс.Диалоги. Яндекс предоставляет возможность создания навыков для Алисы, которые могут отвечать на
# вопросы пользователей и предоставлять решения, но для целей обучения пока так, через Deeppavlov.

# Адрес AI Deeppavlov для поиска часто встречающихся проблем пользователей и вывода им подсказок
API_URL='https://7012.deeppavlov.ai/model'

# Токен телеграм-бота
token='6941923367:AAEPksjNLXq8nHs57NOx9lyoLmKw-eFOa_A'

# Инициализация бота
bot = telebot.TeleBot(token)

# Словарь для хранения открытых тикетов пользователя
tickets = {}

# Обработчик команды /ticket
@bot.message_handler(commands=['ticket'])
def ticket(message):
    user_id = message.from_user.id
    if user_id in tickets:
        ticket_number = tickets[user_id]
        bot.send_message(message.chat.id, f"У вас уже есть открытый тикет с номером {ticket_number}")
    else:
        ticket_number = len(tickets) + 1
        tickets[user_id] = ticket_number
        bot.send_message(message.chat.id, f"Тикет с номером {ticket_number} успешно добавлен")

# Обработчик команды /tickets
@bot.message_handler(commands=['tickets'])
def list_tickets(message):
    user_id = message.from_user.id
    if user_id in tickets:
        ticket_number = tickets[user_id]
        bot.send_message(message.chat.id, f"Открытый тикет с номером {ticket_number}")
    else:
        bot.send_message(message.chat.id, "У вас нет открытых тикетов")

# Поиск решения через wiki
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

# Если бот видит в тексте пользователя часть слова *проблем*, он задает ему вопрос, не хочет ли он добавить новый тикет
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if "проблем" in message.text.lower():
        list_tickets(message)
        bot.send_message(message.chat.id, "Вы хотите добавить новый тикет (запрос на решение проблемы)?")

# Запуск бота
bot.polling()
