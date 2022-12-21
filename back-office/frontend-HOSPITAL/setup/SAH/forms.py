from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class newUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']

class doctorProfile(forms.Form):
    specialization = forms.ChoiceField(choices=(('Orthopedy','Orthopedy'), ('Cardiology','Cardiology'),('Dermatology','Dermatology')),required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    id_card = forms.CharField(required=True, label="ID Card")
       

class RoomForm(forms.Form):
    room = forms.CharField(label="room", required=True)
    floor = forms.CharField(label="floor", required=True)
   

class DateTimePickerInput(forms.DateTimeInput):
        input_type = 'datetime'

class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"
 
class DateTimeLocalField(forms.DateTimeField):
    input_formats = [
        "%Y-%m-%dT%H:%M:%S", 
        "%Y-%m-%dT%H:%M:%S.%f", 
        "%Y-%m-%dT%H:%M"
    ]
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")


class ConsultForm(forms.Form):
    consult_date  = DateTimeLocalField()   
    status = forms.ChoiceField( choices=(('WAITING','WAITING'),('ACCEPT','ACCEPT'), ('DONE','DONE')))

class ConsultReservationForm(forms.Form):
    consult_date  = DateTimeLocalField()
    #pacient = forms.ChoiceField(choices=[(x.id, str(x.name) +  " --- ID CARD: " +  str(x.id_card)) for x in Pacient.objects.all()])
    #doctor = forms.ChoiceField(choices=[(x.id, str(x.name) + " --- " + "Specialization: " + str(x.specialization) + " --- ID CARD: " + str(x.id_card)) for x in doctors["doctors"]])
    status = forms.ChoiceField( choices=(('WAITING','WAITING'),('ACCEPT','ACCEPT'), ('DONE','DONE')))
    description = forms.CharField(label="Description", max_length=450, required=True)



"""
class ExternalLabsForm(forms.Form):
    pacient = forms.ChoiceField(choices=[(x.id, str(x.name) +  " --- ID CARD: " +  str(x.id_card)) for x in Pacient.objects.all()])
    doctor = forms.ChoiceField(choices=[(x.id, str(x.name) + " --- " + "Specialization: " + str(x.specialization) + " --- ID CARD: " + str(x.id_card)) for x in Doctor.objects.all()])
    lab_name = forms.CharField(label="Lab name", max_length=200, required=True)
    consult_lab_date  = DateTimeLocalField()
    intro = forms.CharField(label="Intro", max_length=400, required=True)
    materials = forms.CharField(label="Materials", max_length=400, required=True)
    procedure = forms.CharField(label="Procedure", max_length=400, required=True)
    results = forms.CharField(label="Results", max_length=400, required=True)
    hash = forms.CharField(label="Hash value", max_length=2000, required=True)
"""