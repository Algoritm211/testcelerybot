web: gunicorn testbot.wsgi --log-file -
worker: celery worker --app=tasks.app