from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from django.conf import settings    
from django.contrib.auth.models import User


class Pacient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=150, choices=(('Female','Female'), ('Male','Male'),('Other','Other')))
    address = models.CharField(max_length=400)
    phone_number = models.IntegerField( blank=True, null=True)
    birth_date = models.DateField( blank=True, null=True)
    id_card = models.IntegerField( blank=True, null=True)
    def __str__(self):
        return self.name



"""
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=150, choices=(('Orthopedy','Orthopedy'), ('Cardiology','Cardiology'),('Dermatology','Dermatology')))
    name = models.CharField(max_length=200)

    address = models.CharField(max_length=400)
    phone_number = models.IntegerField( blank=True, null=True)
    birth_date = models.DateField( blank=True, null=True)
    id_card = models.IntegerField( blank=True, null=True)

    def __str__(self):
        return self.name
"""

class Consult(models.Model):
    scheduled_date = models.DateTimeField(default=datetime.now, null=True)
    consult_date = models.DateTimeField( blank=True, null=True)
    pacient_id_card = models.IntegerField( blank=True, null=True)
    doctor_id_card = models.IntegerField( blank=True, null=True)
    status = models.CharField(choices=(('WAITING','WAITING'),('ACCEPT','ACCEPT'), ('DONE','DONE')), max_length=200)
    description = models.CharField(max_length=150)
    def __str__(self):
        return "Consult Date: " + str(self.consult_date) +  " --- Status: " + str(self.status) + " --- Doctor:    " + self.doctor.name + " --- Pacient: " + self.pacient.name

class Room(models.Model):
    number = models.IntegerField( blank=True, null=True)
    floor = models.IntegerField( blank=True, null=True)
    def __str__(self):
        return "Floor: " + str(self.floor) + " --- Number: " + str(self.number)

class ConsultRoomReservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    consult = models.ForeignKey(Consult, on_delete=models.CASCADE)
    def __str__(self):
        return self.consult.doctor.specialization.name


class ExternalLabs(models.Model):
    pacient_id_card = models.IntegerField( blank=True, null=True)
    doctor_id_card = models.IntegerField( blank=True, null=True)
    lab_name = models.CharField(max_length=200)
    consult_lab_date  = models.DateTimeField( blank=True, null=True)
    form_update_date = models.DateTimeField(default=datetime.now, null=True)
    intro = models.CharField(max_length=400)
    materials = models.CharField(max_length=400)
    procedure = models.CharField(max_length=400)
    results = models.CharField(max_length=400)
    hash = models.CharField(max_length=2000)
    def __str__(self):
        return self.lab_name


class Meta:
    app_label  = 'SAH'
