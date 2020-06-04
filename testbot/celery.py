from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testbot.settings')
os.environ.setdefault('REDIS_URL',
                      'redis://h:p5067e3205757872a84ea31d841e6cf3ce88f7fcb568d463ff4dc1708d8f8c792@ec2-3-220-244-30.compute-1.amazonaws.com:14059')

app = Celery('testbot')
# app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
#                 CELERY_RESULT_BACKEND=os.environ['REDIS_URL'],
#                 CELERY_ACCEPT_CONTENT=['json'],
#                 CELERY_TASK_SERIALIZER='json',
#                 CELERY_RESULT_SERIALIZER='json',
#                 CELERY_BEAT_SCHEDULE={
#                     'send-daily-crypto': {
#                         'task': 'bot.tasks.send_daily_cryptocurrency',
#                         'schedule': crontab(minute='*/2'),
#                     },
#                 }
#                 )
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# celery beat task
# app.conf.beat_schedule = {
#     'send-daily-crypto': {
#         'task': 'bot.tasks.send_daily_cryptocurrency',
#         'schedule': crontab(minute='*/5'),
#     },
# }


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
