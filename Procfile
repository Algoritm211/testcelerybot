web: gunicorn testbot.wsgi
worker: celery -A testbot worker --beat --scheduler django --loglevel=info
