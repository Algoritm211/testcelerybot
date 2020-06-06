web: gunicorn testbot.wsgi
worker: celery -A testbot beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

