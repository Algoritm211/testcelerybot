import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testbot.settings.dev')

app = Celery('testbot')
app.config.from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

#celery beat task

app.conf.beat = {
    'send-daily-crypto': {
        'task': 'bot.tasks.send_daily_cryptocurrency',
        'schedule': crontab('*/3')
    }
}
