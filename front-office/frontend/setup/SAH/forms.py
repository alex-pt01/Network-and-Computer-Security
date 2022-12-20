from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import requests

class newUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']

class userProfile(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    id_card = forms.CharField(required=True, label="ID Card")


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


class ConsultReservationForm(forms.Form):
    consult_date  = DateTimeLocalField()
    #pacient = forms.ChoiceField(choices=[(x.id, str(x.name) +  " --- ID CARD: " +  str(x.id_card)) for x in Pacient.objects.all()])
    #doctor = forms.ChoiceField(choices=[(x.id, str(x.name) + " --- " + "Specialization: " + str(x.specialization) + " --- ID CARD: " + str(x.id_card)) for x in doctors["doctors"]])
    #status = forms.ChoiceField( choices=(('WAITING','WAITING')))
    description = forms.CharField(label="Description", max_length=450, required=True)

