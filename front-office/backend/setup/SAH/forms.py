from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from SAH.models import  *

class newUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class updateUserForm(forms.Form):
    first_name = forms.CharField(label='First Name', required=True)
    last_name = forms.CharField(label='Last Name', required=True)
    username = forms.CharField(label='Username', required=True)
    email = forms.EmailField(label='Your Email', required=True)
    currentPassword = forms.CharField(label='Current Password', widget=forms.PasswordInput(), required=True)
    newPassword = forms.CharField(label='New Password', widget=forms.PasswordInput(), required=True)
    repeatNewPassword = forms.CharField(label='Repeat New Password', widget=forms.PasswordInput(), required=True)


                          
      
class PacientForm(forms.Form):
    name = forms.CharField(label="Name", max_length=150, required=True)
    gender = forms.ChoiceField(choices=(('Female','Female'), ('Male','Male'),('Other','Other')),required=True)
    address = forms.CharField(label="Address", max_length=400, required=True)
    phone_number = forms.IntegerField( label="Phone number", help_text='Must have 9 numbers', required=True)
    birth_date = forms.DateField(label="Birth Date", help_text='Required. Format: YYYY-MM-DD', required=True)
    id_card = forms.IntegerField(label="ID Card", help_text='Must have 9 numbers', required=True)


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
    #doctor = forms.ChoiceField(choices=[(x.id, str(x.name) + " --- " + "Specialization: " + str(x.specialization) + " --- ID CARD: " + str(x.id_card)) for x in Doctor.objects.all()])
    status = forms.ChoiceField( choices=(('WAITING','WAITING'),('ACCEPT','ACCEPT'), ('DONE','DONE')))
    description = forms.CharField(label="Description", max_length=450, required=True)

class ConsultPacientForm(forms.Form):
    consult_date  = DateTimeLocalField()
    #doctor = forms.ChoiceField(choices=[(x.id, str(x.name) + " --- " + "Specialization: " + str(x.specialization) + " --- ID CARD: " + str(x.id_card)) for x in Doctor.objects.all()])
    description = forms.CharField(label="Description", max_length=450, required=True)

