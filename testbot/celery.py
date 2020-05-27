import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testbot.settings')

app = Celery('testbot')
app.config.from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

#celery beat task
