from datetime import timedelta

from celery.task import periodic_task

from testbot.celery import app
from .models import User
import telebot
from . import coinmarket

TOKEN = '1113179664:AAEaV5nToFyEdoOAF5NrhjjncnLCJKbHXGs'

bot = telebot.TeleBot(TOKEN)


@periodic_task(run_every=timedelta(hours=20, minutes=38))
def send_daily_cryptocurrency():
    all_users = User.objects.all()
    text = coinmarket.get_top_10()
    for user in all_users:
        if user.send_daily_prices:
            bot.send_message(user.user_id, text, parse_mode='HTML')
