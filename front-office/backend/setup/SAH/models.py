from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from django.conf import settings    
from django.contrib.auth.models import User




class ConsultReservation(models.Model):
    scheduled_date = models.DateTimeField(default=datetime.now, null=True)
    consult_date = models.DateTimeField( blank=True, null=True)
    pacient_id_card = models.IntegerField( blank=True, null=True)
    doctor_id_card = models.IntegerField( blank=True, null=True)
    status = models.CharField(choices=(('WAITING','WAITING'),('ACCEPT','ACCEPT'), ('DONE','DONE')), max_length=200)
    description = models.CharField(max_length=150)
    def __str__(self):
        return "Consult Date: " + str(self.consult_date) +  " --- Status: " + str(self.status) + " --- Doctor:    " + self.doctor.name + " --- Pacient: " + self.pacient.name

class Meta:
    app_label  = 'SAH'
