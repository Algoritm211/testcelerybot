from testbot.celery import app
from .models import User
from .views import send_daily_cryptos


@app.task
def send_daily_cryptocurrency():
    send_daily_cryptos()
