# Generated by Django 4.1.4 on 2022-12-17 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SAH', '0006_externallabs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consult',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='consult',
            name='pacient',
        ),
        migrations.RemoveField(
            model_name='externallabs',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='externallabs',
            name='pacient',
        ),
        migrations.AddField(
            model_name='consult',
            name='doctor_id_card',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='consult',
            name='pacient_id_card',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='externallabs',
            name='doctor_id_card',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='externallabs',
            name='pacient_id_card',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Doctor',
        ),
        migrations.DeleteModel(
            name='Specialization',
        ),
    ]
