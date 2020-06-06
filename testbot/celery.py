from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testbot.settings')
app = Celery('testbot')
app.config_from_object('django.conf:settings')
app.conf.timezone = 'UTC'
app.conf.enable_utc = True
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.celery_beat = {
    'send-daily-crypto': {
        'task': 'bot.tasks.send_daily_cryptocurrency',
        'schedule': crontab(minute='*/1'),
    },
}
