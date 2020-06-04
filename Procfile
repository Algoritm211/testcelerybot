web: gunicorn testbot.wsgi
worker: celery -A testbot worker --beat --scheduler celery.beat.PersistentScheduler --loglevel=info
