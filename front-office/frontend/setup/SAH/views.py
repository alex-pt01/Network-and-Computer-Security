
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from SAH.forms import *
from django.http import HttpRequest, HttpResponseRedirect
from time import strptime
from datetime import datetime
import json
import requests
from ratelimit import limits, RateLimitException, sleep_and_retry

ONE_MINUTE = 60
MAX_CALLS_PER_MINUTE = 300

URL = "https://192.168.1.3:8002/"
URL_HOSPITAL = "https://192.168.1.4:8003/"

HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
    
}

ACCESS_TOKEN_DICT = {}
@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def user_is_authenticated(request, token):
    params = { "token": token }

    resp = requests.post(URL+'jwt/verify/', headers = HEADERS ,data=json.dumps(params), verify=False)
    
    print("RESP text", resp.text)
    if resp.text == "{}":
        return True
    else:
        print("FALSE")
        del request.session['token']
        del request.session['username']
        return False
    

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def login(request):
    print(request.session)
    if 'token' in request.session and user_is_authenticated(request, request.session.get('token')):
        context = {'username': request.session['username']}
        return render(request, 'home.html', context)
    else:
        print(request.method)
        if request.method == 'POST':
            username = request.POST.get('user')
            try:
                password = request.POST.get('pass')
                params = { "username": username, "password": password }
                print(password)
                resp = requests.post(URL+'api/login/', headers = HEADERS ,data=json.dumps(params),verify=False)
                print("RESP ", resp)
                tk = json.loads(resp.text)['tokens']['access']
                print(resp.status_code)
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

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
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
                resp = requests.post(URL+'api/signup/', headers = HEADERS ,data=json.dumps(params),verify=False)
                return redirect('profile')
        return render(request, 'signup.html', {'form': form})

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
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
                resp = requests.post(URL+'api/profile/', headers = HEADERS ,data=json.dumps(params),verify=False)
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

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def consults(request):
    print("CONSULTSSSSSS")
    print(request.session['token'])
    if 'token' in request.session and user_is_authenticated(request, request.session['token']):

        headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + request.session['token']
        }      
        #GET pacient profile      
        params = { "username": request.session['username']}
        pacient = requests.get(URL+'api/pacient-profile/',headers = headers,data=json.dumps(params),verify=False )
        #Objetc -> enviar como json
        print("PACIENT  ", pacient.json().get("id_card"))

        #GET pacient consults
        params_ = { "username": request.session['username'], "pacient_id_card": pacient.json().get("id_card")}
        response = requests.get(URL_HOSPITAL+'api/pacient-consults/',headers = headers,data=json.dumps(params_),verify=False )
        print("OOOOO")
        print("RESPONSE ", response.json())
        new_info = []
        #GET doctor profile      
        for obj in response.json():
            print("OKK ", type(obj))
            params_doct = { "username": request.session['username'], "id_card": obj.get("doctor_id_card")}
            doctor_profile = requests.get(URL_HOSPITAL+'api/doctor-profile-by-id/',headers = headers,data=json.dumps(params_doct),verify=False )
            print(doctor_profile.json().get("first_name"))
            obj["first_name"]=doctor_profile.json().get("first_name")
            obj["last_name"]=doctor_profile.json().get("last_name")
            obj["specialization"]=doctor_profile.json().get("specialization")
            new_info.append(obj)
        print("NEWW!!!!! ", type(new_info))

        print("NEWW ", type(new_info))

        context = {'username': request.session['username'], "consults": new_info}
        return render(request, 'consults.html', context)
    else:
        context = {}
        return render(request, 'login.html', context)

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def consult_reservation(request):
    headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + request.session['token']
    }        
    if 'token' in request.session and user_is_authenticated(request, request.session['token']):
        if request.method == 'POST':
            form = ConsultReservationForm(request.POST, request.FILES)
            params = { "username": request.session['username']}

            if form.is_valid():
                scheduled_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                consult_date = form.cleaned_data['consult_date']                
                #GET pacient profile
                pacient = requests.get(URL+'api/pacient-profile/',headers = headers,data=json.dumps(params),verify=False )
                pacient_id_card = pacient.json().get("id_card")

                doctor_id_card = request.POST['selec_doct']
                status = "WAITING"
                description = form.cleaned_data['description']
                consult = {"scheduled_date":scheduled_date,"consult_date":consult_date,"pacient_id_card":pacient_id_card,"doctor_id_card":doctor_id_card,"status":status,"description":description  }
                resp = requests.post(URL_HOSPITAL+'api/create-consult/', headers = headers ,data=json.dumps(consult,default=str),verify=False)
                context = {'username': request.session['username'] }
                return render(request, 'home.html', context)


        else:      
            params = { "username": request.session['username']}
            response = requests.get(URL_HOSPITAL+'api/doctors/',headers = headers,data=json.dumps(params),verify=False )
            context = {'username': request.session['username'], "doctors": response.json(), 'form': ConsultReservationForm() }
            return render(request, 'consult-reservation.html', context)

    else:
        context = {}
        return render(request, 'login.html', context)

