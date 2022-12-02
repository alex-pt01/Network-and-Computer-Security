from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core import validators
from SAH.models import Specialization

class newUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class updateUserForm(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    username = forms.CharField(label='Username')
    email = forms.EmailField(label='Your Email')
    currentPassword = forms.CharField(label='Current Password', widget=forms.PasswordInput())
    newPassword = forms.CharField(label='New Password', widget=forms.PasswordInput())
    repeatNewPassword = forms.CharField(label='Repeat New Password', widget=forms.PasswordInput())


class DoctorForm(forms.Form):
    specialization = forms.ChoiceField(choices=(('Orthopedy','Orthopedy'), ('Cardiology','Cardiology'),('Dermatology','Dermatology')))
    gender = forms.ChoiceField(choices=(('Female','Female'), ('Male','Male'),('Other','Other')),required=True)
    address = forms.CharField(label="Address", max_length=400, required=True)
    phone_number = forms.IntegerField(label="Phone number", help_text='Must have 9 numbers')
    birth_date = forms.DateField(label="birth_date", help_text='Required. Format: YYYY-MM-DD')
    id_card = forms.IntegerField(label="ID Card", help_text='Must have 9 numbers')
                          
        
class PacientForm(forms.Form):
    name = forms.CharField(label="Name", max_length=150, required=True)
    gender = forms.ChoiceField(choices=(('Female','Female'), ('Male','Male'),('Other','Other')),required=True)
    address = forms.CharField(label="Address", max_length=400, required=True)
    phone_number = forms.IntegerField( label="Phone number", help_text='Must have 9 numbers')
    birth_date = forms.DateField(label="Birth Date", help_text='Required. Format: YYYY-MM-DD')
    id_card = forms.IntegerField(label="ID Card", help_text='Must have 9 numbers')
