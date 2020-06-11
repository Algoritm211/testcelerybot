import os

from django.shortcuts import render

__author__ = '@Alexey_Horbunov'

from rest_framework.response import Response
from rest_framework.views import APIView
import telebot
from telebot import types
from collections import defaultdict
import datetime
from .models import User
from . import market
from . import parse

from .tasks import send_daily_cryptocurrency

# Create your views here.
TOKEN = '1113179664:AAEaV5nToFyEdoOAF5NrhjjncnLCJKbHXGs'
bot = telebot.TeleBot(TOKEN)


class UpdateBot(APIView):

    def post(self, request):
        json_string = request.body.decode("UTF-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])

        return Response({'code': 200})


GOTOSET, FINAL = range(2)

keyboard_1 = telebot.types.ReplyKeyboardMarkup(True, False, row_width=1)
keyboard_1.row('My MarketCap')
keyboard_1.row('Настройка уведомлений')

USER_STATE = defaultdict(lambda: GOTOSET)


def get_state(message):
    return USER_STATE[message.chat.id]


def update_state(message, state):
    USER_STATE[message.chat.id] = state


'''WEBHOOK'''


# app = Flask(__name__)
#
# @app.route('/' + TOKEN, methods=['POST'])
# def get_message():
#     bot.process_new_updates([types.Update.de_json(
#         flask.request.stream.read().decode("utf-8"))])
#     return "!", 200
#
#
# @app.route('/', methods=["GET"])
# def index():
#     bot.remove_webhook()
#     bot.set_webhook(url="https://{}.herokuapp.com/{}".format(APP_NAME, TOKEN))
#     return "Hello from CoinsInfo Bot!", 200

@bot.message_handler(commands=['start'])
def message_start(message):
    bot.send_message(message.chat.id, '🤖Здравствуйте, ' + message.from_user.first_name + '!\n' \
                                                                                          '💵Я могу показать Вам цены цифровых активов с биржи Binance, а также отслеживать Ваши криптовалюты \n\n' +
                     'Для просмотра инструкции пользователя нажмите /help.\n\n\n', reply_markup=keyboard_1)
    now = datetime.datetime.now()
    curr_date = now.strftime("%d-%m-%Y")
    user = User()
    user.user_id = message.chat.id
    user.save()


@bot.message_handler(commands=['help'])
def message_help(message):
    markup_author = types.InlineKeyboardMarkup(row_width=1)
    item_author = types.InlineKeyboardButton('Об авторе бота', callback_data='author')
    # markup_author.add(item_author)
    bot.send_message(message.chat.id,
                     '❓Итак, в настоящий момент бот может показать Вам цену цифровых активов с биржи ' +
                     'Binance в парах с биткоином и USDT (для этого достаточно ввести тикер актива (Например, eth)), ' +
                     'а также отслеживать введенные Вами активы(команда /set). ', reply_markup=markup_author)


@bot.message_handler(commands=['getinfobot'])
def get_info_bitbullbot(message):
    # all_users = str(dbhelper.get_number_of_all_users())
    bot.send_message(message.chat.id, 'ℹПодключаюсь к базе данных и получаю информацию........')
    all = User.objects.all()
    # for i in all:
    #     print(i.user_id)
    # print(type(all))


@bot.message_handler(commands=['set'], func=lambda message: get_state(message) == GOTOSET)
def message_to_set_coins(message):
    bot.send_message(message.chat.id, 'Напишите токены, цены которых Вы бы хотели отслеживать, котировки ' +
                     'будут браться с портала CoinMarketCap.\nВводите тикеры токенов через пробел. ' +
                     '<b>Например, btc eth ada xrp.</b> \n\n' +
                     'После этого достаточно нажать кнопку My CoinMarket для отслеживания криптовалют',
                     parse_mode='HTML')
    update_state(message, FINAL)
    # bot.send_message(message.chat.id, 'Я тут')


@bot.message_handler(func=lambda message: get_state(message) == FINAL)
def set_crypto(message):
    bot.send_message(message.chat.id, 'Проверяю наличие введенных активов на CoinMarketCap.....')
    tickers = list(set([elem.upper() for elem in message.text.split()]))
    # print(tickers)
    check = []
    data = market.get_data()
    for i in tickers:
        for j in data['data']:
            if i == j['symbol'] and j['name'] != 'BuySell':
                check.append(i)
    if len(check) != 0:
        text = 'Из введенных Вами криптовалют будут отслеживаться такие активы: \n'
        for i in check:
            text += i + '\n'
        info = User.objects.get(user_id=message.chat.id)
        text1 = ''
        for i in check:
            text1 += i + ','
        info.coins = text1
        info.save()
        bot.send_message(message.chat.id, text, reply_markup=keyboard_1)
    else:
        bot.send_message(message.chat.id, 'Из введенных Вами криптовалют ни одна не торгуется на CoinMarketCap. ' +
                         'Нажмите /set и введите активы еще раз. ')
    update_state(message, GOTOSET)


@bot.message_handler(content_types=['text'], func=lambda message: get_state(message) != FINAL)
def message_cryptos(message):
    if message.text.lower() == 'my marketcap':
        info = User.objects.get(user_id=message.chat.id)
        # print(info)
        if info.coins == None:
            bot.send_message(message.chat.id, 'B базе нет отслеживаемых Вами криптовалют, нажмите /set, ' +
                             'чтобы указать желаемые цифровые активы.')
        else:
            bot.send_message(message.chat.id, 'Беру информацию о Ваших токенах и связываюсь с CoinMarketCap......')
            drop_db = info.coins.split(',')
            # print(drop_db)
            # print(type(drop_db))
            data = market.get_data()
            now = datetime.datetime.now()
            id = 1
            text = 'Отслеживаемые Вами криптовалюты: \n\n'
            for i in drop_db:
                # print(i)
                for j in data['data']:
                    if i == j['symbol'] and j['name'] != 'BuySell':
                        text += '<b>№' + str(id) + '</b> <i>' + j['name'] + '</i> <code>' + str(
                            round(j['quote']['USD']['price'], 3)) + '</code> USD ' + \
                                str(round(j['quote']['USD']['percent_change_24h'], 2)) + '(%|24h)\n\n'

                        id += 1
            text += '<b>Информация с портала CoinMarketCap по состоянию на ' + now.strftime("%d-%m-%Y") + '.</b>\n\n'
            text += '<i>Вы всегда можете изменить отслеживаемые криптовалюты с помощью команды</i> /set'
            bot.send_message(message.chat.id, text, parse_mode='HTML')
    else:
        text_up = message.text.upper()
        mes_usdt = parse.get_crypto_to_usdt(message.text)
        mes_btc = parse.get_crypto_to_btc(message.text)
        bot.send_message(message.chat.id, 'ℹПодключаюсь к Binance, беру актуальную информацию')
        text = '~~~~~~~~~~~~~\n' + 'Данные с биржи 🔸Binance🔸\n' + '~~~~~~~~~~~~~\n' + 'Информация по паре ' + text_up + '-USDT:\n' + \
               '1 ' + text_up + ' = ' + mes_usdt + '\n' + 'Информация по паре ' + text_up + '-BTC:\n' + '1 ' + text_up + ' = ' + \
               mes_btc + '\n'
        if 'не торгуется' in mes_usdt and mes_btc:
            bot.send_message(message.chat.id, 'Введенный Вами тикер токена не торгуется против USDT и BTC')
        else:
            bot.send_message(message.chat.id, text, parse_mode='HTML')
    if 'настройка уведомлений' in message.text.lower():
        user_data = User.objects.filter(user_id=message.chat.id)
        keyboard_notif = types.InlineKeyboardMarkup(row_width=1)
        if user_data.send_daily_prices:
            button_set_false = types.InlineKeyboardButton('Выключить уведомления', callback_data='set_notif_off')
            keyboard_notif.add(button_set_false)
        elif not user_data.send_daily_prices:
            button_set_true = types.OutlineKeyboardButton('Включить уведомления', callback_data='set_notif_on')
            keyboard_notif.add(button_set_true)

        bot.send_message(message.chat.id,
                         '<b>Уведомления</b>\n + У Вас есть возможность включить уведомления о самых актуальных ценах ТОП-10 криптовалют.\n' + \
                         'Бот будет присылать Вам уведомление каждый день в <b>7:30</b>\n\n. <i>От уведомлений можно отказаться в любой удобный момент</i>',
                         parse_mode='HTML', reply_markup=keyboard_notif)


@bot.callback_query_handler(func=lambda call: True)
def inline_buttons(call):
    if call.message:
        if call.data == 'getall':
            help_file = open('all.txt', 'rb')
            bot.send_document(call.message.chat.id, help_file)
        elif call.data == 'author':
            bot.send_message(call.message.chat.id, 'Команда 2348', parse_mode='HTML')
        elif call.data == 'notification':
            pass


send_daily_cryptocurrency.delay()

# bot.polling(none_stop=True)
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
