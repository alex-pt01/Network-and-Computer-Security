# Generated by Django 4.1.3 on 2022-12-01 19:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SAH', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='consult',
            name='date_now',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
