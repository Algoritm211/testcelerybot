from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testbot.settings')
app = Celery('testbot')
app.config_from_object('django.conf:settings')
app.conf.timezone = 'Europe/Kiev'
app.autodiscover_tasks()

# app.conf.celery_beat = {
#     'send-daily-crypto': {
#         'task': 'bot.tasks.send_daily_cryptocurrency',
#         'schedule': crontab(minute='*/2'),
#     },
# }
