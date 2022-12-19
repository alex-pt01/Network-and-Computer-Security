
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from SAH.forms import *
from django.http import HttpRequest, HttpResponseRedirect
from time import strptime
from datetime import datetime
import json
import requests
from localStoragePy import localStoragePy

localStorage = localStoragePy('SAH-frontend', 'SAH-backend')

URL = "http://127.0.0.1:8002/"
URL_HOSPITAL = "http://127.0.0.1:8004/"

HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
    
}

ACCESS_TOKEN_DICT = {}

def user_is_authenticated(request, token):
    params = { "token": token }

    resp = requests.post(URL+'jwt/verify/', headers = HEADERS ,data=json.dumps(params))
    
    print("RESP text", resp.text)
    if resp.text == "{}":
        return True
    else:
        print("FALSE")
        del request.session['token']
        del request.session['username']
        return False
    


def login(request):
    print(request.session)
    if 'token' in request.session and user_is_authenticated(request, request.session.get('token')):
        context = {'username': request.session['username']}
        return render(request, 'home.html', context)
    else:
        if request.method == 'POST':
            username = request.POST.get('user')
            try:
                password = request.POST.get('pass')
                params = { "username": username, "password": password }
                resp = requests.post(URL+'api/login/', headers = HEADERS ,data=json.dumps(params))
                print("RESP ", resp)
                tk = json.loads(resp.text)['tokens']['access']
                if resp.status_code != 200:
                    print('error: ' + str(resp.status_code))
                    messages.info(request, 'Username OR password is incorrect')
                else:
                    print('token: ' + str(tk))
                    ACCESS_TOKEN_DICT[username] = str(tk)
                    request.session['token'] = str(tk)
                    request.session['username'] = username

                    print('Success')
                    print(request.session['username'])
                    messages.success(request, 'Welcome!!! ')
                    context = {'username': username}

                    return render(request, 'home.html', context)
            except: 
                context = {}
                return render(request, 'login.html', context)


        context = {}
        return render(request, 'login.html', context)

def signup(request):
    if 'token' in request.session and user_is_authenticated(request, request.session.get('token')):
        messages.info(request, 'You are already registered')
        context = {'username': request.session['username']}
        return render(request, 'home.html', context)
    else:
        form = newUserForm()
        if request.method == 'POST':
            form = newUserForm(request.POST)
            if form.is_valid():
                username = request.POST.get('username')
                email = request.POST.get('email')

                password1 = request.POST.get('password1')
                #password2 = request.POST.get('password2')
                params = { "username": username, "email": email, "password": password1}
                resp = requests.post(URL+'api/signup/', headers = HEADERS ,data=json.dumps(params))
                return redirect('profile')
        return render(request, 'signup.html', {'form': form})


def profile(request):
    if 'token' in request.session and user_is_authenticated(request, request.session.get('token')):
        messages.info(request, 'You are already registered')
        context = {'username': request.session['username']}
        return render(request, 'home.html', context)
    else:
        form = userProfile()
        if request.method == 'POST':
            form = userProfile(request.POST)
            if form.is_valid():

                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                id_card = request.POST.get('id_card')
                params = {  "first_name": first_name, "last_name": last_name, "id_card": id_card}
                resp = requests.post(URL+'api/profile/', headers = HEADERS ,data=json.dumps(params))
                context = {'username': request.session['username']}
                return render(request, 'home.html', context)
        return render(request, 'profile.html', {'form': form})


def logout(request):
    del request.session['token']
    del request.session['username']
    context = {}
    return render(request, 'home.html', context)

def home(request):
    if 'username' in request.session:
        context = {'username': request.session['username']}
        return render(request, 'home.html', context)
    else:  
        return render(request, 'home.html', {})

def consults(request):
    print(request.session['token'])
    if 'token' in request.session and user_is_authenticated(request, request.session['token']):

        headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + request.session['token']
        }            
        params = { "username": request.session['username']}
        response = requests.get(URL+'api/consults/',headers = headers,data=json.dumps(params) )
        context = {'username': request.session['username'], "consults": response.json()}
        return render(request, 'consults.html', context)
    else:
        context = {}
        return render(request, 'login.html', context)

def consult_reservation(request):
    print(request.session['token'])
    if 'token' in request.session and user_is_authenticated(request, request.session['token']):

        headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + request.session['token']
        }            
        params = { "username": request.session['username']}
        response = requests.get(URL_HOSPITAL+'api/doctors/',headers = headers,data=json.dumps(params) )
        context = {'username': request.session['username'], "doctors": response.json()}
        print(context["doctors"])
        return render(request, 'consult-reservation.html', context["doctors"])

    else:
        context = {}
        return render(request, 'home.html', context)


"""
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

"""