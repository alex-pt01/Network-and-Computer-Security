# Generated by Django 4.1.4 on 2022-12-19 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SAH', '0011_remove_userprofile_user_userprofile_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='dddd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('id_card', models.CharField(max_length=30, unique=True)),
            ],
        ),
    ]
