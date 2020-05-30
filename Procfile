web: gunicorn testbot.wsgi --log-file -
worker: celery -A testbot worker --loglevel=info
beat: celery -A testbot beat
