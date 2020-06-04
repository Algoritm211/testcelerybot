web: gunicorn testbot.wsgi
worker: celery -A testbot worker --beat --scheduler django_celery_beat.schedulers:DatabaseScheduler --loglevel=info
