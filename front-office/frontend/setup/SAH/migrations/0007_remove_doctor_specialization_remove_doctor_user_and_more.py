# Generated by Django 4.1.4 on 2022-12-17 23:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SAH', '0006_rename_consult_consultreservation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='specialization',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='user',
        ),
        migrations.RemoveField(
            model_name='pacient',
            name='user',
        ),
        migrations.DeleteModel(
            name='ConsultReservation',
        ),
        migrations.DeleteModel(
            name='Doctor',
        ),
        migrations.DeleteModel(
            name='Pacient',
        ),
        migrations.DeleteModel(
            name='Specialization',
        ),
    ]
