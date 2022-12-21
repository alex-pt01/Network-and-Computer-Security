from datetime import datetime
from pyexpat.errors import messages
from django.shortcuts import HttpResponseRedirect, redirect, render
from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from SAH.forms import *
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from django.http import HttpRequest, HttpResponseRedirect
from django.http.response import JsonResponse

from rest_framework.parsers import JSONParser 
import json
import requests
from ratelimit import limits, RateLimitException, sleep_and_retry

ONE_MINUTE = 60
MAX_CALLS_PER_MINUTE = 300

URL_HOSPITAL = "http://127.0.0.1:8004/"
URL = "http://127.0.0.1:8002/"

HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
}

ACCESS_TOKEN_DICT = {}

def user_is_authenticated(request, token):
    params = { "token": token }

    resp = requests.post(URL_HOSPITAL+'jwt/verify/', headers = HEADERS ,data=json.dumps(params))
    
    print("RESP text", resp.text)
    if resp.text == "{}":
        return True
    else:
        print("FALSE")
        del request.session['token']
        del request.session['username']
        return False
    
def home(request):
    if 'username' in request.session:
        context = {'username': request.session['username']}
        return render(request, 'home.html', context)
    else:  
        return render(request, 'home.html', {})

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
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
                resp = requests.post(URL_HOSPITAL+'api/login/', headers = HEADERS ,data=json.dumps(params))
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
                    params = { "username": username }
                    admin_data = requests.get(URL_HOSPITAL+'api/check-is-admin/', headers = HEADERS ,data=json.dumps(params))
                    print("ttt   ", admin_data.json().get("admin"))
                    request.session['admin'] = admin_data.json().get("admin")
                    print("XXXXX ", request.session['admin'])

                    print('Success')
                    print(request.session['username'])
                    messages.success(request, 'Welcome!!! ')
                    context = {'username': username, 'admin': request.session['admin']}

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
                resp = requests.post(URL_HOSPITAL+'api/signup/', headers = HEADERS ,data=json.dumps(params))
                return redirect('profile')
        return render(request, 'signup.html', {'form': form})

def logout(request):    
    print("DDDDDD")
    del request.session['token']
    del request.session['username']
    #del request.session['admin']
    context = {}
    return render(request, 'home.html', context)

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def profile(request):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + request.session['token']
    }      
    if 'token' in request.session and user_is_authenticated(request, request.session.get('token')):
        messages.info(request, 'You are already registered')
        context = {'username': request.session['username']}
        return render(request, 'home.html', context)
    else:
        form = doctorProfile()
        if request.method == 'POST':
            form = doctorProfile(request.POST)
            if form.is_valid():
                specialization = request.POST.get('specialization')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                id_card = request.POST.get('id_card')
                params = {"specialization": specialization, "first_name": first_name, "last_name": last_name, "id_card": id_card}
                resp = requests.post(URL_HOSPITAL+'api/profile/', headers = headers ,data=json.dumps(params))
                context = {}
                return render(request, 'home.html', context)
        return render(request, 'profile.html', {'form': form})


@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def doctor_consults(request):

    print("CONSULTSSSSSS")
    print(request.session['token'])
    if 'token' in request.session and user_is_authenticated(request, request.session['token']):

        headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + request.session['token']
        }      
        print("SSSSS")
        #GET doctor profile      
        params = { "username": request.session['username']}
        doctor = requests.get(URL_HOSPITAL+'api/doctor-profile/',headers = headers,data=json.dumps(params) )
        #Objetc -> enviar como json
        print("doctor  ", doctor.json())

        #GET doctor consults
        params_ = { "username": request.session['username'], "doctor_id_card": doctor.json().get("id_card")}
        response = requests.get(URL_HOSPITAL+'api/doctor-consults/',headers = headers,data=json.dumps(params_) )
        print("OOOOO")
        print("RESPONSE ", response.json())
        new_info = []
        #GET pacient profile      
        for obj in response.json():
            print("OKK ", type(obj))
            params_pacient = { "username": request.session['username'], "id_card": obj.get("pacient_id_card")}
            pacient_profile = requests.get(URL+'api/pacient-profile-by-id/',headers = headers,data=json.dumps(params_pacient) )
            print(pacient_profile.json().get("first_name"))
            obj["first_name"]=pacient_profile.json().get("first_name")
            obj["last_name"]=pacient_profile.json().get("last_name")
            new_info.append(obj)
        print("NEWW!!!!! ", type(new_info))

        print("NEWW ", type(new_info))

        context = {'username': request.session['username'], "consults": new_info}
        return render(request, 'doctor-consults.html', context)
    else:
        context = {}
        return render(request, 'login.html', context)

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def consults_management(request):
    print("CONSULTS MANAGEMENT")
    print(request.session['token'])
    if 'token' in request.session and user_is_authenticated(request, request.session['token']):
        headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + request.session['token']
        }     
        params = { "username": request.session['username']}

        consults = requests.get(URL_HOSPITAL+'api/all-consults/',headers = headers,data=json.dumps(params) )
        new_info = []
        #GET pacient profile      
        for obj in consults.json():
            print("OKK ", obj)
            params_pacient = { "username": request.session['username'], "id_card": obj.get("pacient_id_card")}
            pacient_profile = requests.get(URL+'api/pacient-profile-by-id/',headers = headers,data=json.dumps(params_pacient) )
            print(pacient_profile.json().get("first_name"))
            obj["first_name_pacient"]=pacient_profile.json().get("first_name")
            obj["last_name_pacient"]=pacient_profile.json().get("last_name")
            
            params_doct = { "username": request.session['username'], "id_card": obj.get("doctor_id_card")}
            doctor_profile = requests.get(URL_HOSPITAL+'api/doctor-profile-by-id/',headers = headers,data=json.dumps(params_doct) )
            print(doctor_profile.json().get("first_name"))
            obj["first_name_doctor"]=doctor_profile.json().get("first_name")
            obj["last_name_doctor"]=doctor_profile.json().get("last_name")
            obj["specialization"]=doctor_profile.json().get("specialization")
            new_info.append(obj)

        print("NEWW!!!!! ", type(new_info))
        context = {'username': request.session['username'], "consults": new_info}
        return render(request, 'consults-management.html', context)

    else:
        context = {}
        return render(request, 'login.html', context)

def deleteConsult(request, id):
    if 'token' in request.session and user_is_authenticated(request, request.session['token']):
        headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + request.session['token']
        }     
        params = { "username": request.session['username']}
        resp = requests.delete(URL_HOSPITAL+'api/hosp-consult/'+id, headers = HEADERS ,data=json.dumps(params))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def update_consult(request,id):
    print("IIID ", id)
    headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + request.session['token']
    }        
    if 'token' in request.session and user_is_authenticated(request, request.session['token']):
        if request.method == 'POST':
            form = ConsultForm(request.POST, request.FILES)
            params = { "username": request.session['username']}

            if form.is_valid():
                params_id_cons = { "username": request.session['username'], "id": id}
                consult_data = requests.get(URL_HOSPITAL+'api/hospital-consult-by-id/',headers = headers,data=json.dumps(params_id_cons) )
                print("FFF ", consult_data.json().get("scheduled_date"))
                scheduled_date = consult_data.json().get("scheduled_date")
                consult_date = form.cleaned_data['consult_date']                
                pacient_id_card = consult_data.json().get("pacient_id_card")
                doctor_id_card = consult_data.json().get("doctor_id_card")
                description = consult_data.json().get("description")
                status = form.cleaned_data['status']

                consult = {"scheduled_date":scheduled_date,"consult_date":consult_date,"pacient_id_card":pacient_id_card,"doctor_id_card":doctor_id_card,"status":status,"description":description  }
                
                resp = requests.put(URL_HOSPITAL+'api/hosp-consult/'+id, headers = headers ,data=json.dumps(consult,default=str))
                context = {'username': request.session['username'] }
                return render(request, 'home.html', context)


        else:      
            print("DDDD ",id )
            params_id_cons = { "username": request.session['username'], "id": id}
            consult_data = requests.get(URL_HOSPITAL+'api/hospital-consult-by-id/',headers = headers,data=json.dumps(params_id_cons) )
            context = {'username': request.session['username'], "consult": consult_data.json(), 'form': ConsultForm() }
            return render(request, 'update-consult.html', context)

    else:
        context = {}
        return render(request, 'login.html', context)

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def create_consult(request):
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
                #pacient = requests.get(URL+'api/pacient-profile/',headers = headers,data=json.dumps(params) )
                pacient_id_card = request.POST['selec_pac']

                doctor_id_card = request.POST['selec_doct']
                status = form.cleaned_data['status']   
                description = form.cleaned_data['description']
                
                consult = {"scheduled_date":scheduled_date,"consult_date":consult_date,"pacient_id_card":pacient_id_card,"doctor_id_card":doctor_id_card,"status":status,"description":description  }
                resp = requests.post(URL_HOSPITAL+'api/create-consult/', headers = headers ,data=json.dumps(consult,default=str))
                context = {'username': request.session['username'] }
                return render(request, 'home.html', context)
        else:      
            params = { "username": request.session['username']}
            response_doct = requests.get(URL_HOSPITAL+'api/doctors/',headers = headers,data=json.dumps(params) )
            response_pac = requests.get(URL+'api/pacients/',headers = headers,data=json.dumps(params) )
            context = {'username': request.session['username'], "doctors": response_doct.json(),"pacients": response_pac.json(),  'form': ConsultReservationForm() }
            return render(request, 'create-consult.html', context)
    else:
        context = {}
        return render(request, 'login.html', context)

#---------------------------------------------------------------
#Consults room reservation
@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def rooms_management(request):
    print("ROOMS MANAGEMENT")
    print(request.session['token'])
    if 'token' in request.session and user_is_authenticated(request, request.session['token']):
        headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + request.session['token']
        }     
        params = { "username": request.session['username']}
        print("HHHHHHHHHHH")
        rooms = requests.get(URL_HOSPITAL+'api/all-room-reservations/',headers = headers,data=json.dumps(params) )
        print(rooms.json())
        new_info = []
        for obj in rooms.json():
            print("OKK ", obj)
            print(type(obj.get("consult_id")))
            params_consult = { "username": request.session['username'], "id": obj.get("consult_id")}

            consult = requests.get(URL_HOSPITAL+'api/hospital-consult-by-id/',headers = headers,data=json.dumps(params_consult) )
            print(consult.json())
            obj["consult_date"]=consult.json().get("consult_date")
            obj["pacient_id_card"]=consult.json().get("pacient_id_card")
            obj["doctor_id_card"]=consult.json().get("doctor_id_card")
            obj["status"]=consult.json().get("status")
            new_info.append(obj)
        print("BBB ", new_info)
        context = {'username': request.session['username'], "rooms": new_info}
        return render(request, 'rooms-management.html', context)

    else:
        context = {}
        return render(request, 'login.html', context)



@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def deleteRoom(request, id):
    if 'token' in request.session and user_is_authenticated(request, request.session['token']):
        headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + request.session['token']
        }     
        params = { "username": request.session['username']}
        resp = requests.delete(URL_HOSPITAL+'api/del-room/'+id, headers = HEADERS ,data=json.dumps(params))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def create_room(request):
    headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + request.session['token']
    }        
    if 'token' in request.session and user_is_authenticated(request, request.session['token']):
        if request.method == 'POST':
            form = RoomForm(request.POST, request.FILES)
            params = { "username": request.session['username']}
            print("FFFF") 
            print(form)
            if form.is_valid():
                print("SSSSSSS")
                consult_id = request.POST['selec_consult']   
                floor = form.cleaned_data['floor'] 
                print("YYYYY ", type(floor))  
                room = form.cleaned_data['room']
                
                room_data = {"floor":floor,"room":room,"consult_id":consult_id }
                resp = requests.post(URL_HOSPITAL+'api/create-room-reservation/', headers = headers ,data=json.dumps(room_data))
                context = {'username': request.session['username'] }
                return render(request, 'home.html', context)
            else:
                params = { "username": request.session['username']}
                response_consult = requests.get(URL_HOSPITAL+'api/all-consults/',headers = headers,data=json.dumps(params) )
                context = {'username': request.session['username'], 'consults': response_consult.json(), 'form': RoomForm() }
                return render(request, 'create-room.html', context)
        else:      
            params = { "username": request.session['username']}

            response_consult = requests.get(URL_HOSPITAL+'api/all-consults/',headers = headers,data=json.dumps(params) )
            print(response_consult.json())
            context = {'username': request.session['username'], 'consults': response_consult.json(), 'form': RoomForm() }
            return render(request, 'create-room.html', context)
    else:
        context = {}
        return render(request, 'login.html', context)

#External Labs------------------------
@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def external_labs_info(request):
    print("EXTERNAL MANAGEMENT")
    print(request.session['token'])
    if 'token' in request.session and user_is_authenticated(request, request.session['token']):
        headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + request.session['token']
        }     
        params = { "username": request.session['username']}
        print("RRRRR")
        external_labs = requests.get(URL_HOSPITAL+'api/external-labs/',headers = headers,data=json.dumps(params) )
        print(external_labs.json())        
        context = {'username': request.session['username'], "externalLabs": external_labs.json()}
        return render(request, 'external-lab-info.html', context)
    else:
        context = {}
        return render(request, 'login.html', context)

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def deleteExternalLab(request, id):
    if 'token' in request.session and user_is_authenticated(request, request.session['token']):
        headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + request.session['token']
        }     
        params = { "username": request.session['username']}
        resp = requests.delete(URL_HOSPITAL+'api/del-external-lab/'+id, headers = HEADERS ,data=json.dumps(params))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def external_labs_by_doctor_id_card(request):
    print("external_labs_by_doctor_id_card ")
    print(request.session['token'])
    if 'token' in request.session and user_is_authenticated(request, request.session['token']):
        headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + request.session['token']
        }     
        params = { "username": request.session['username']}
        response_doct = requests.get(URL_HOSPITAL+'api/doctor-profile/',headers = headers,data=json.dumps(params) )
        print("RRRRR", response_doct.json().get("id_card"))
        
        params_ = { "username": request.session['username'], "doctor_id_card": response_doct.json().get("id_card") }
        external_labs = requests.get(URL_HOSPITAL+'api/external-labs-by-doct_id_card/',headers = headers,data=json.dumps(params_) )
        print(external_labs.json())        
        context = {'username': request.session['username'], "externalLabs": external_labs.json()}
        return render(request, 'external-lab-info-doctor.html', context)
    else:
        context = {}
        return render(request, 'login.html', context)
