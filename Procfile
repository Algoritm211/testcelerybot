web: gunicorn testbot.wsgi --log-file -
worker: celery -A bot.tasks worker -B --loglevel=info
