from django.shortcuts import render

from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from SAH.forms import *
from SAH.models import *
from django.http import HttpRequest, HttpResponseRedirect
from time import strptime
from datetime import datetime
import json
import requests

URL = "http://127.0.0.1:8002/"

HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

ACCESS_TOKEN = None
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('user')
            password = request.POST.get('pass')
            
            params = { "username": username, "password": password }
            resp = requests.post(URL+'api/login/', headers = HEADERS ,data=json.dumps(params))
            tk = json.loads(resp.text)['tokens']['access']
            if resp.status_code != 200:
                print('error: ' + str(resp.status_code))
                messages.info(request, 'Username OR password is incorrect')

            else:
                print('token: ' + str(tk))
                ACCESS_TOKEN = str(tk)
                print('Success')
                messages.success(request, 'Welcome!!! ')
                return redirect('home')
        context = {}
        return render(request, 'login.html', context)



def signup(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already registered')
        return redirect('home')
    else:
        form = newUserForm()
        if request.method == 'POST':
            form = newUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('home')
        return render(request, 'signup.html', {'form': form})


def logout(request):
    logoutUser(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html', {"form": "forms"})

def consults(request):
    consults = None
    user_type = None
    if request.user.is_authenticated:

        if Pacient.objects.filter(user_id=request.user.id).exists():
            print("Pacient")
            pacient = Pacient.objects.get(user__id= request.user.id)
            consults = ConsultReservation.objects.filter(pacient=pacient)
            user_type= 'P'

        return render(request, 'consults.html', {'consults': consults, 'user_type': user_type})
    return redirect('login')

def consult_reservation(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ConsultPacientForm(request.POST, request.FILES)
            if form.is_valid():
                consult = ConsultReservation()
                consult.scheduled_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                consult.consult_date = form.cleaned_data['consult_date']
                consult.pacient = Pacient.objects.get(user__pk=request.user.id)
                consult.doctor = Doctor.objects.get(id=form.cleaned_data['doctor'])
                consult.description = form.cleaned_data['description']
                consult.status = "WAITING"
                consult.save()
                return redirect('consults')
            else:
                print("USER ID  ", Pacient.objects.get(user__pk=request.user.id).id)
                print(form.errors)
        else:
            form = ConsultPacientForm()
        return render(request, 'consult-reservation.html', {'form': form})
    return redirect('login')

def account(request):
    if request.user.is_authenticated:
        if Pacient.objects.filter(user_id=request.user.id).exists():
            print("PACIENT")
            return render(request, 'account.html', {"user_type":"P","pacient": Pacient.objects.get(user_id=request.user.id)})
        elif Doctor.objects.filter(user_id=request.user.id).exists():
            print("DOCTOR")
            doctor = Doctor.objects.get(user_id=request.user.id)
            return render(request, 'account.html', {"user_type": "D", "doctor" : doctor})
        else:
            if request.user.is_superuser:
                return redirect('account')
    return redirect('login')



def update_pacient(request, pacient_id):
    if request.user.is_authenticated:
        pacient = Pacient.objects.get(id=pacient_id)
        if request.method == 'POST':
            form = PacientForm(request.POST)
            if form.is_valid():
                pacient.name = form.cleaned_data['name'] 
                pacient.gender= form.cleaned_data['gender']
                pacient.address = form.cleaned_data['address']
                number = form.cleaned_data['phone_number']
                pacient.birth_date = form.cleaned_data['birth_date']
                pacient.phone_number = number
                pacient.save()
                return redirect("home")
        else:
            form = PacientForm(initial={ "name": pacient.name,
                                        "gender": pacient.gender,
                                        "address": pacient.address,
                                        "phone_number": pacient.phone_number,
                                        "birth_date": pacient.birth_date,
                                        "id_card": pacient.id_card,
                                        })                
        return render(request, "update-pacient.html", {"form": form})


def doctor_info(request, id):
    if request.user.is_authenticated:
        doctor = Doctor.objects.get(id=id)
        return render(request, "doctor-info.html", {"doctor": doctor})    
    return redirect('login')
