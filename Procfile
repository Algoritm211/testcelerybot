web: gunicorn testbot.wsgi
worker: celery -A proj beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

