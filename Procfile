web: gunicorn testbot.wsgi
worker: celery -A testbot worker -l info --beat --scheduler django_celery_beat.schedulers:DatabaseScheduler

