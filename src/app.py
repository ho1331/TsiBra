import os
import json

import telebot
from telebot import types

from .services import SIGN_RU, answer_by_ai, horoskop_parser

bot = telebot.TeleBot(os.getenv('TOKEN'))


def start_handler(chat_id, firstname):
    markup = types.ReplyKeyboardMarkup(True)
    start_buttom = types.KeyboardButton('/start')
    zodiac_buttom = types.KeyboardButton('/zodiac')
    markup.add(start_buttom)
    markup.add(zodiac_buttom)
    message = f'Бот приветсвует тебя @{firstname}'
    bot.send_message(chat_id, message, reply_markup=markup)


def zodiac_menu(chat_id):
    # Готовим кнопки
    keyboard = types.InlineKeyboardMarkup()
    for i in SIGN_RU:
        # готовим текст и обработчик для каждого знака зодиака
        btm = types.InlineKeyboardButton(text=i, callback_data=i)
        # И добавляем кнопку на экран
        keyboard.add(btm)
    bot.send_message(chat_id, text='Выбери свой знак зодиака', reply_markup=keyboard)


def lambda_handler(event, context):
    events = json.loads(event['body'])
    if events.get('callback_query'):
        chat_id = events['callback_query']['message']['chat']['id']
        sign = events['callback_query']['data']
        horoskop = horoskop_parser(sign)
        bot.send_message(chat_id, text=horoskop)

    elif message := events["message"]["text"]:
        chat_id = events['message']['chat']['id']
        first_name = events["message"]['chat']['first_name']

        if message == '/start':
            start_handler(chat_id, first_name)

        elif message == '/zodiac':
            zodiac_menu(chat_id)

        else:
            ai_say = answer_by_ai(message)
            bot.send_message(chat_id, text=ai_say)
    
    return {
        'body': json.dumps(event['body']),
        'statusCode': 200
    }
