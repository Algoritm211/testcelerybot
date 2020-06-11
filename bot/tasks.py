from datetime import timedelta
from celery.schedules import crontab

from celery.task import periodic_task

from testbot.celery import app
from .models import User
import telebot
from . import coinmarket

TOKEN = '1113179664:AAEaV5nToFyEdoOAF5NrhjjncnLCJKbHXGs'

bot = telebot.TeleBot(TOKEN)


@app.task
def send_daily_cryptocurrency():
    all_users = User.objects.all()
    text = coinmarket.get_top_10()
    for user in all_users:
        if user.send_daily_prices:
            bot.send_message(user.user_id, text, parse_mode='HTML')


app.conf.beat_schedule = {
    'task-name': {
        'task': 'tasks.send_daily_cryptocurrency',
        'schedule': crontab(hour=18, minute=12)
    },
}
app.conf.timezone = 'Europe/Kiev'
