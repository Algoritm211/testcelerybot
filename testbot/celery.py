from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testbot.settings')
app = Celery('testbot')
app.config_from_object('django.conf:settings')
app.conf.timezone = 'Europe/Kiev'
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Executes every day at  12:30 pm.
    'run-every-afternoon': {
        'task': 'bot.tasks.send_daily_cryptocurrency',
        'schedule': crontab(hour=21, minute=45),
        'args': (),
    },
}