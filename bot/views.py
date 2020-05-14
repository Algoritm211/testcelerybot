from django.shortcuts import render
__author__ = '@Alexey_Horbunov'
from rest_framework.response import Response
from rest_framework.views import APIView
import telebot
from telebot import types
from collections import defaultdict
import datetime
import time
import numpy as np
from pprint import pprint
from .models import User


# Create your views here.
TOKEN = '1113179664:AAEaV5nToFyEdoOAF5NrhjjncnLCJKbHXGs'
bot = telebot.TeleBot(TOKEN)

class UpdateBot(APIView):

    def post(self, request):
        json_string = request.body.decode("UTF-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])

        return Response({'code':200})

GOTOSET, FINAL = range(2)

keyboard_1 = telebot.types.ReplyKeyboardMarkup(True, False, row_width=1)
keyboard_1.row('get_date', 'test')

MYLIST = ['item1', 'item2', 'item3', 'item4', 'item5', 'item6']

USER_STATE = defaultdict(lambda: GOTOSET)
def get_state(message):
    return USER_STATE[message.chat.id]


def update_state(message, state):
    USER_STATE[message.chat.id] = state


@bot.message_handler(commands=['start'])
def message_start(message):
    bot.send_message(message.chat.id, '🤖Здравствуйте, '+ message.from_user.first_name + '!\n' \
    '💵Я могу показать Вам цены и графики цифровых активов, а также рассказать о последних новостях в сфере криптовалют \n\n' +
    'Для просмотра инструкции пользователя нажмите /help.\n\n\n'+
    'Powered by Alexey Horbunov\n'+
    '@Alexey_Horbunov', reply_markup=keyboard_1)
    user = User()
    user.user_id = message.chat.id
    user.save()

k = 0
@bot.message_handler(content_types=['text'])
def bot_answer_to_text(message):
    if message.text.lower() == 'get_date':

        user = User()
        id = 402954445
        info = User.objects.get(user_id__exact=id)
        # for i in date_mes:
        #     bot.send_message(message.chat.id, str(i))
        print(type(info))

    elif message.text.lower() == 'test':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton('back', callback_data='back')
        item2 = types.InlineKeyboardButton('up', callback_data='up')
        cutter = lambda list, size: [list[i:i + size] for i in range(0, len(list), size)]
        global matrix_text
        matrix_text = cutter(MYLIST, 2)
        global k
        k = 0
        for i in matrix_text[0]:
            item = types.InlineKeyboardButton(i, callback_data=i)
            keyboard.add(item)
        keyboard.add(item1, item2)
        sent = bot.send_message(message.chat.id, 'change', reply_markup=keyboard)

        # bot.edit_message_text(text='edited', chat_id=message.chat.id, message_id=edited)

@bot.callback_query_handler(func=lambda call: True)
def test_menu(call):
    if call.message:
        if call.data == 'up':
            global k
            k += 1
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            for i in matrix_text[k]:
                item = types.InlineKeyboardButton(i, callback_data=i)
                keyboard.add(item)
            item1 = types.InlineKeyboardButton('back', callback_data='back')
            item2 = types.InlineKeyboardButton('up', callback_data='up')
            keyboard.add(item1, item2)
            bot.edit_message_text('change', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)




CRYPTOS = defaultdict(lambda: {})

def update_cryptos(id, name, values):
    test.write_user_to_db(id, name, values)
def get_cryptos(id):
    return CRYPTOS[id]

# bot.polling(none_stop=True)
