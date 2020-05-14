from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=200)
    date_pubs = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id + '--------' + self.date_pubs
