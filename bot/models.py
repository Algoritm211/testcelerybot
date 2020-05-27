from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=200, unique=True)
    date_pubs = models.DateTimeField(auto_now_add=True)
    coins = models.TextField(blank=True)
    send_daily_prices = models.BooleanField(default=False)

    def __str__(self):
        return self.user_id
