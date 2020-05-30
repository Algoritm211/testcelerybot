web: gunicorn testbot.wsgi --log-file -
worker: celery -A tasks worker --loglevel=info
