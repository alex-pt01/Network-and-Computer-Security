# Generated by Django 4.1.4 on 2022-12-19 20:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SAH', '0009_doctorprofile'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DoctorProfile',
            new_name='DoctorProfilee',
        ),
    ]
