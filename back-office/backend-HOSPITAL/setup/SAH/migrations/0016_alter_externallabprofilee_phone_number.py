# Generated by Django 3.2.16 on 2022-12-26 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SAH', '0015_externallabprofilee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externallabprofilee',
            name='phone_number',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
    ]
