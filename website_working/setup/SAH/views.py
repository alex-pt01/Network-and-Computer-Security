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

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('user')
            password = request.POST.get('pass')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                loginUser(request, user)
                messages.success(request, 'Welcome!!! ')
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')
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
                return redirect('paciente_or_doctor')
        return render(request, 'signup.html', {'form': form})

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

def paciente_or_doctor(request):
     return render(request, 'paciente-or-doctor.html', {'form': 's'})

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

def pacient_signup(request):
    if not request.user.is_superuser:
        if request.method == 'POST':
            form = PacientForm(request.POST, request.FILES)
            
            if form.is_valid():
                pacient = Pacient(user = User.objects.all().last(),
                name = form.cleaned_data['name'], 
                gender= form.cleaned_data['gender'],
                address = form.cleaned_data['address'],
                phone_number = form.cleaned_data['phone_number'],
                birth_date = form.cleaned_data['birth_date'],
                id_card = form.cleaned_data['id_card'],
                )
                pacient.save()
                return redirect('home')
            else:
                print(form.errors)
        else:
            form = PacientForm()
        return render(request, 'pacient-signup.html', {'form': form})
    return redirect('login')

def logout(request):
    logoutUser(request)
    return redirect('home')

def home(request):

    print( Pacient.objects.all().query.__str__())
    return render(request, 'home.html', {"form": "forms"})

def consults(request):
    consults = None
    user_type = None
    if request.user.is_authenticated:
        if request.user.is_superuser:
            print("HOSPITAL")
            consults = Consult.objects.all()
            user_type = 'H'
        elif Pacient.objects.filter(user_id=request.user.id).exists():
            print("Pacient")
            pacient = Pacient.objects.get(user__id= request.user.id)
            consults = Consult.objects.filter(pacient=pacient)
            user_type= 'P'
        elif Doctor.objects.filter(user_id=request.user.id).exists():
            print("DOCTOR")
            doctor = Doctor.objects.get(user__id= request.user.id)
            consults = Consult.objects.filter(doctor=doctor)
            user_type = 'D'
        return render(request, 'consults.html', {'consults': consults, 'user_type': user_type})
    return redirect('login')

def consult_reservation(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ConsultPacientForm(request.POST, request.FILES)
            if form.is_valid():
                consult = Consult()
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


    
#HOSPITAL --------------------------------------------------------------------------------
def consults_management(request):
    if request.user.is_authenticated and request.user.is_superuser:
        consults = None
        if request.user.is_superuser:
            consults = Consult.objects.all()
    return render(request, 'consults-management.html', {'consults': consults})

def create_consult(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            form = ConsultForm(request.POST, request.FILES)
            if form.is_valid():
                consult = Consult()
                consult.scheduled_date = datetime.now()
                consult.consult_date = form.cleaned_data['consult_date']
                consult.pacient = Pacient.objects.get(id=form.cleaned_data['pacient'])
                consult.doctor = Doctor.objects.get(id=form.cleaned_data['doctor'])
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

def deleteConsult(request, id):
    consult = Consult.objects.get(id=id)
    consult.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def update_consult(request,id):
    consult = Consult.objects.get(id=id)
    if request.method == "POST":
        form = ConsultForm(request.POST)
        if form.is_valid():
            consult.scheduled_date = datetime.now()
            consult.consult_date = form.cleaned_data['consult_date']
            consult.pacient = Pacient.objects.get(id=form.cleaned_data['pacient'])
            consult.doctor = Doctor.objects.get(id=form.cleaned_data['doctor'])
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

def pacient_info(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        pacient = Pacient.objects.get(id=id)
        return render(request, "pacient-info.html", {"pacient": pacient})    
    return redirect('login')

def doctor_info(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        doctor = Doctor.objects.get(id=id)
        return render(request, "doctor-info.html", {"doctor": doctor})    
    return redirect('login')
