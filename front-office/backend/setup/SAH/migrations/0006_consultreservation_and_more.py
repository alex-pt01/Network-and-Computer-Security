# Generated by Django 4.1.4 on 2022-12-17 22:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SAH', '0005_alter_consult_id_alter_consultroomreservation_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_date', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('consult_date', models.DateTimeField(blank=True, null=True)),
                ('pacient_id_card', models.IntegerField(blank=True, null=True)),
                ('doctor_id_card', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('WAITING', 'WAITING'), ('ACCEPT', 'ACCEPT'), ('DONE', 'DONE')], max_length=200)),
                ('description', models.CharField(max_length=150)),
            ],
        ),
        migrations.RemoveField(
            model_name='consultroomreservation',
            name='consult',
        ),
        migrations.RemoveField(
            model_name='consultroomreservation',
            name='room',
        ),
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
            name='Consult',
        ),
        migrations.DeleteModel(
            name='ConsultRoomReservation',
        ),
        migrations.DeleteModel(
            name='Doctor',
        ),
        migrations.DeleteModel(
            name='Pacient',
        ),
        migrations.DeleteModel(
            name='Room',
        ),
        migrations.DeleteModel(
            name='Specialization',
        ),
    ]
