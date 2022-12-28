from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from django.conf import settings    
from django.contrib.auth.models import User



class DoctorProfilee(models.Model):
    username = models.CharField(max_length=100)
    specialization = models.CharField(max_length=150, choices=(('Orthopedy','Orthopedy'), ('Cardiology','Cardiology'),('Dermatology','Dermatology')))
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    id_card = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.username

class ExternalLabProfilee(models.Model):
    username = models.CharField(max_length=100)
    lab_name = models.CharField(max_length=100)
    phone_number = models.CharField( max_length=9,blank=True, null=True)
    address = models.CharField(max_length=300)
    def __str__(self):
        return self.username


class Consult(models.Model):
    scheduled_date = models.DateTimeField(default=datetime.now, null=True)
    consult_date = models.DateTimeField( blank=True, null=True)
    pacient_id_card = models.IntegerField( blank=True, null=True)
    doctor_id_card = models.IntegerField( blank=True, null=True)
    status = models.CharField(choices=(('WAITING','WAITING'),('ACCEPT','ACCEPT'), ('DONE','DONE')), max_length=200)
    description = models.CharField(max_length=150)
    def __str__(self):
        return self.status




class ConsultRoomReservation(models.Model):
    floor = models.IntegerField( blank=True, null=True)
    room = models.IntegerField( blank=True, null=True)
    consult_id = models.IntegerField( blank=True, null=True)
    def __str__(self):
        return str(self.floor)


class ExternalLabs(models.Model):
    pacient_id_card = models.IntegerField( blank=True, null=True)
    doctor_id_card = models.IntegerField( blank=True, null=True)
    lab_name = models.CharField(max_length=200)
    consult_lab_date  = models.CharField( max_length=400)
    form_update_date = models.CharField(max_length=400)
    intro = models.CharField(max_length=400)
    materials = models.CharField(max_length=400)
    procedure = models.CharField(max_length=400)
    results = models.CharField(max_length=400)
    hash = models.CharField(max_length=10000)

    def __str__(self):
        return self.lab_name


class Meta:
    app_label  = 'SAH'
