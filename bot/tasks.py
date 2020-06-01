from testbot.celery import app
from .models import User
from .views import bot


@app.task
def send_daily_cryptocurrency():
    all_users = User.objects.all()
    for user in all_users:
        if not user.send_daily_prices:
            bot.send_message(user.user_id, 'У не вас стоит напоминание')
