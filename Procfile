web: gunicorn testbot.wsgi --log-file -
worker: celery -A testbot.tasks worker -B --loglevel=info
