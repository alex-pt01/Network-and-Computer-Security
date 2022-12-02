from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from SAH.forms import newUserForm, DoctorForm, PacientForm
from SAH.models import *
# Create your views here.

#User = settings.AUTH_PROFILE_MODULE

from time import strptime




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
                # messages (dict)
                messages.success(request, 'Account was created for ' + user)

                return redirect('paciente_or_doctor')

        return render(request, 'signup.html', {'form': form})

def paciente_or_doctor(request):
     return render(request, 'paciente-or-doctor.html', {'form': 's'})

def doctor_signup(request):
    if not request.user.is_superuser:
        if request.method == 'POST':
            form = DoctorForm(request.POST, request.FILES)
            if form.is_valid():
                doct = Doctor(user = User.objects.all().last(),
                specialization = Specialization.objects.get(name=form.cleaned_data['specialization']),
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
    return render(request, 'home.html', {'items': 'c'})

def account(request):
    if request.user.is_authenticated:

        return render(request, 'account.html')
    return redirect('login')


