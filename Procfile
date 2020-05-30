web: gunicorn testbot.wsgi --log-file -
worker: celery -A bot.tasks worker -B --loglevel=info
python manage.py celeryd -v 2 -B -s celery -E -l INFO
