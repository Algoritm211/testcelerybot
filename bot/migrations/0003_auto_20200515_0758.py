# Generated by Django 3.0.3 on 2020-05-15 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_user_date_pubs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
