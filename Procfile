web: gunicorn testbot.wsgi
worker: celery -A prj worker --beat --scheduler celery.beat.PersistentScheduler --loglevel=info
