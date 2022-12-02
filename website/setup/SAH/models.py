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

class Specialization(models.Model):
    name = models.CharField(max_length=150, choices=(('Orthopedy','Orthopedy'), ('Cardiology','Cardiology'),('Dermatology','Dermatology')))
    description = models.CharField(max_length=400)
    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    gender = models.CharField(max_length=150, choices=(('Female','Female'), ('Male','Male'),('Other','Other')))
    name = models.CharField(max_length=200)

    address = models.CharField(max_length=400)
    phone_number = models.IntegerField( blank=True, null=True)
    birth_date = models.DateField( blank=True, null=True)
    id_card = models.IntegerField( blank=True, null=True)

    def __str__(self):
        return self.name


class Consult(models.Model):
    pacient = models.ForeignKey(Pacient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_now = models.DateTimeField(default=datetime.now)

    consult_date = models.DateField( blank=True, null=True)
    description = models.CharField(max_length=150)
    def __str__(self):
        return self.user.get_username

class Room(models.Model):
    number = models.IntegerField( blank=True, null=True)
    floor = models.IntegerField( blank=True, null=True)
    def __str__(self):
        return self.number

class ConsultReservation(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    consult = models.OneToOneField(Consult, on_delete=models.CASCADE)
    def __str__(self):
        return self.consult.doctor.speciality.name


class Meta:
    app_label  = 'SAH'
