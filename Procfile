web: gunicorn testbot.wsgi --log-file -
worker: celery -A testbot worker -B --loglevel=info
