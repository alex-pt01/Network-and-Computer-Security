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
    del request.session['token']
    del request.session['username']
    context = {}
    return render(request, 'home.html', context)

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
        resp = requests.post(URL_HOSPITAL+'api/deleteConsult/', headers = HEADERS ,data=json.dumps(params))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def update_consult(request,id):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


"""
def consults(request):
    print(request.session['token'])
    if 'token' in request.session and user_is_authenticated(request, request.session['token']):

        headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + request.session['token']
        }            
        params = { "username": request.session['username']}
        response = requests.get(URL_HOSPITAL+'api/consults/',headers = headers,data=json.dumps(params) )
        context = {'username': request.session['username'], "consults": response.json()}
        return render(request, 'consults.html', context)
    else:
        context = {}
        return render(request, 'login.html', context)

def home(request):
    if 'username' in request.session:
        context = {'username': request.session['username']}
        return render(request, 'home.html', context)
    else:  
        return render(request, 'home.html', {})
"""



"""
def create_consult(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            form = ConsultForm(request.POST, request.FILES)
            if form.is_valid():
                consult = Consult()
                consult.scheduled_date = datetime.now()
                consult.consult_date = form.cleaned_data['consult_date']
                consult.pacient = Pacient.objects.get(id=form.cleaned_data['pacient'])
                #consult.doctor = Doctor.objects.get(id=form.cleaned_data['doctor'])
                consult.description = form.cleaned_data['description']
                consult.status = form.cleaned_data['status']
                consult.save()
                return redirect('consults-management')
            else:
                print(form.errors)
        else:
            form = ConsultForm()
        return render(request, 'create-consult.html', {'form': form})
    return redirect('login')

"""






    

"""
def update_consult(request,id):
    consult = Consult.objects.get(id=id)
    if request.method == "POST":
        form = ConsultForm(request.POST)
        if form.is_valid():
            consult.scheduled_date = datetime.now()
            consult.consult_date = form.cleaned_data['consult_date']
            consult.pacient = Pacient.objects.get(id=form.cleaned_data['pacient'])
            #consult.doctor = Doctor.objects.get(id=form.cleaned_data['doctor'])
            consult.description = form.cleaned_data['description']
            consult.status = form.cleaned_data['status']
            consult.save()
            return redirect('consults-management')
    else:
        form = ConsultForm(initial={"scheduled_date": consult.scheduled_date,
                                      "consult_date": consult.consult_date,
                                      "pacient": consult.pacient,
                                      "doctor": consult.doctor,
                                      "status":consult.status,
                                      "description":consult.description
                                      })
    return render(request, "update-consult.html", {"form": form})

def rooms_management(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'rooms-management.html', {'rooms': Room.objects.all()})
    return redirect('login')

def deleteRoom(request, id):
    room = Room.objects.get(id=id)
    room.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def update_room(request,id):
    room = Room.objects.get(id=id)
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == "POST":
            form = RoomForm(request.POST)
            if form.is_valid():
                room.number = form.cleaned_data['number']
                room.floor = id=form.cleaned_data['floor']
                room.save()
                return redirect('rooms-management')
        else:
            form = RoomForm(initial={"number": room.number,
                                        "floor": room.floor,
                                        })
                     
        return render(request, "update-room.html", {"form": form})    
    return redirect('login')

def create_room(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            form = RoomForm(request.POST, request.FILES)
            if form.is_valid():
                room = Room()
                room.number = form.cleaned_data['number']
                room.floor = id=form.cleaned_data['floor']
                room.save()
                return redirect('rooms-management')
            else:
                print(form.errors)
        else:
            form = RoomForm()
        return render(request, 'create-room.html', {'form': form})
    return redirect('login')



def room_consult_management(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'room-consult-management.html', {'consultRoomReservations': ConsultRoomReservation.objects.all()})
    return redirect('login')

def create_room_consult(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            form = ConsultRoomReservationForm(request.POST, request.FILES)
            if form.is_valid():
                consultReservationForm = ConsultRoomReservation()
                consultReservationForm.room = Room.objects.get(id=form.cleaned_data['room'])
                consultReservationForm.consult = Consult.objects.get(id=form.cleaned_data['consult'])

                consultReservationForm.save()
                return redirect('room-consult-management')
            else:
                print(form.errors)
        else:
            form = ConsultRoomReservationForm()
        return render(request, 'create-room-consult.html', {'form': form})
    return redirect('login')

def deleteRoomConsult(request, id):
    consultReservation = ConsultRoomReservation.objects.get(id=id)
    consultReservation.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def update_room_consult(request,id):
    assert isinstance(request, HttpRequest)
    consultReservationForm = ConsultRoomReservation.objects.get(id=id)

    if request.user.is_authenticated and request.user.is_superuser:

        if request.method == "POST":
            form = ConsultRoomReservationForm(request.POST)
            if form.is_valid():
                consultReservationForm.room = Room.objects.get(id=form.cleaned_data['room'])
                consultReservationForm.consult = Consult.objects.get(id=form.cleaned_data['consult'])
                consultReservationForm.save()
                return redirect('room-consult-management')
        else:
            form = ConsultRoomReservationForm(initial={"room": consultReservationForm.room,
                                        "consult": consultReservationForm.consult,
                                
                                        })
                                        
        return render(request, "update-room-consult.html", {"form": form})    
    return redirect('login')
"""


"""
def external_lab_info(request):
    if request.user.is_authenticated and request.user.is_superuser:
        externalLabs = ExternalLabs.objects.all()
        return render(request, "external-lab-info.html", {"externalLabs": externalLabs})    
    return redirect('login')

def create_external_lab_info(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            form = ExternalLabsForm(request.POST, request.FILES)
            if form.is_valid():
                externalLabs = ExternalLabs()
                externalLabs.pacient = Pacient.objects.get(id=form.cleaned_data['pacient'])
                #externalLabs.doctor = Doctor.objects.get(id=form.cleaned_data['doctor'])
                externalLabs.lab_name = form.cleaned_data['lab_name']
                externalLabs.consult_lab_date = form.cleaned_data['consult_lab_date']
                externalLabs.form_update_date = datetime.now()
                externalLabs.intro = form.cleaned_data['intro']
                externalLabs.materials = form.cleaned_data['materials']
                externalLabs.procedure = form.cleaned_data['procedure']
                externalLabs.results = form.cleaned_data['results']
                externalLabs.hash = form.cleaned_data['hash']
                externalLabs.save()

                return redirect('external-lab-info')
            else:
                print(form.errors)
        else:
            form = ExternalLabsForm()
        return render(request, 'create-external-lab-info.html', {'form': form})
    return redirect('login')
"""


















"""
def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def update_user(request):
    tparams = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = updateUserForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                username = data['username']
                email = data['email']
                curPass = data['currentPassword']
                newPass = data['newPassword']
                newRepeatedPass = data['repeatNewPassword']
                firstName = data['first_name']
                lastName = data['last_name']
                if newPass != newRepeatedPass:
                    form = updateUserForm()
                    tparams['form'] = form
                    tparams['error'] = "Inserted Passwords Are Not The Same"
                    return render(request, 'update-user.html', tparams)
                if request.user.check_password(curPass):

                    user = request.user
                    user.username = username
                    user.first_name = firstName
                    user.last_name = lastName
                    user.email = email
                    user.set_password(raw_password=newPass)
                    user.save()
                else:
                    form = updateUserForm()
                    tparams['form'] = form
                    tparams['error'] = "Incorrect Password"
                    return render(request, 'update-user.html', tparams)
                return redirect('login')
        else:
            form = updateUserForm()
        tparams['form'] = form
        return render(request, 'update-user.html', tparams)
    return redirect('login')



def doctor_signup(request):
    if not request.user.is_superuser:
        if request.method == 'POST':
            form = DoctorForm(request.POST, request.FILES)
            if form.is_valid():
                doct = Doctor(user = User.objects.all().last(),
                specialization = Specialization.objects.get(id= form.cleaned_data['specialization']),
                gender= form.cleaned_data['gender'],
                name = form.cleaned_data['name'], 
                address = form.cleaned_data['address'],
                phone_number = form.cleaned_data['phone_number'],
                birth_date = form.cleaned_data['birth_date'],
                id_card = form.cleaned_data['id_card'],
                )
                doct.save()
                return redirect('home')
            else:
                print(form.errors)
        else:
            form = DoctorForm()
        return render(request, 'doctor-signup.html', {'form': form})
    return redirect('login')

"""


"""
def account(request):
    if request.user.is_authenticated:

        if Doctor.objects.filter(user_id=request.user.id).exists():
            print("DOCTOR")
            doctor = Doctor.objects.get(user_id=request.user.id)
            return render(request, 'account.html', {"user_type": "D", "doctor" : doctor})
        else:
            if request.user.is_superuser:
                return redirect('account')
    return redirect('login')

def update_doctor(request, doctor_id):
    if request.user.is_authenticated:
        doctor = Doctor.objects.get(id=doctor_id)
        if request.method == 'POST':
            form = DoctorForm(request.POST)
            if form.is_valid():
                doctor.specialization = Specialization.objects.get(id=form.cleaned_data['specialization'])
                doctor.gender= form.cleaned_data['gender']
                doctor.name = form.cleaned_data['name']
                doctor.address = form.cleaned_data['address']
                doctor.phone_number = form.cleaned_data['phone_number']
                doctor.birth_date = form.cleaned_data['birth_date']
                doctor.id_card = form.cleaned_data['id_card']
                doctor.save()
                return redirect("home")
        else:
            form = DoctorForm(initial={
                    "specialization": doctor.specialization,
                                        "gender": doctor.gender,
                                        "name": doctor.name,
                                        "address": doctor.address,
                                        "phone_number": doctor.phone_number,
                                        "birth_date": doctor.birth_date,
                                        "id_card": doctor.id_card,
                                        })             
        return render(request, "update-doctor.html", {"form": form})
"""


"""
def users_management(request):
    if request.user.is_authenticated and request.user.is_superuser:
        pacients = Pacient.objects.all()
        doctors = Doctor.objects.all()
        return render(request, 'user-management.html', {"pacients": pacients, "doctors" : doctors})
    return redirect('login')

def deletePacient(request, id):
    pacient = Pacient.objects.get(id=id)
    pacient.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def deleteDoctor(request, id):
    doctor = Doctor.objects.get(id=id)
    doctor.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
"""


"""
class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        if request.user.is_authenticated:
            messages.info(request, 'You are already registered')
            return redirect('home')
        else:
            form = newUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('doctor-signup')
            return render(request, 'signup.html', {'form': form}, status=status.HTTP_400_BAD_REQUEST )

    def get(self, request: Request):
        if request.user.is_authenticated:
            messages.info(request, 'You are already registered')
            return redirect('home')
        else:
            form = newUserForm()
            return render(request, 'signup.html', {'form': form})
        

class LoginView(APIView):
    permission_classes = []
    def post(self, request: Request):
        username = request.POST.get('user')
        password = request.POST.get('pass')

        user = authenticate(username=username, password=password)
        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response = {"message": "Login Successfull", "tokens": tokens}
            return render(request, 'home.html', response, status=status.HTTP_200_OK)
        else:
            return render(request, 'login.html', {"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST )

    def get(self, request: Request):
        if request.user.is_authenticated:
            messages.info(request, 'You are already registered')
            return redirect('home')
        else:
            context = {}
            return render(request, 'login.html', context)
"""