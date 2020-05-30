web: gunicorn testbot.wsgi
worker: celery -A bot.tasks worker -B --loglevel=info
