from pyexpat.errors import messages
from django.contrib.auth import authenticate
from django.shortcuts import HttpResponseRedirect, redirect, render
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from SAH.serializers import SignUpSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from SAH.serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from SAH.forms import *
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from django.http import HttpRequest, HttpResponseRedirect
from django.http.response import JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import json
from rest_framework.parsers import JSONParser 


User = get_user_model()

def create_jwt_pair_for_user(user: User):
    refresh = RefreshToken.for_user(user)
    tokens = {"access": str(refresh.access_token), "refresh": str(refresh)}
    return tokens

class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {"message": "User Created Successfully", "data": serializer.data}
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []
    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response = {"message": "Login Successfull", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid email or password"})

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}
        return Response(data=content, status=status.HTTP_200_OK)

@api_view([ 'GET'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def doctors(request):
    try: 
        doctor = DoctorProfilee.objects.all()
        print(doctor)
        doctor_serializer = DoctorProfileSerializer(doctor, many=True)
        return Response(doctor_serializer.data)
    except DoctorProfilee.DoesNotExist: 
        return JsonResponse({'message': 'consult does not exist'}, status=status.HTTP_200_OK) 

@api_view([ 'POST'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def fill_profile(request):
    new_profile = {}
    if request.method == 'POST':
        user_profile_data = JSONParser().parse(request)
        print("USER PROFILE  ", user_profile_data)
        user = User.objects.all().last()
        new_profile['username']=user.username
        new_profile.update(user_profile_data)
        print("NEW USER PROFILE  ", new_profile)
        print()
        user_profile_serializer = DoctorProfileSerializer(data=new_profile)
        if user_profile_serializer.is_valid():
            user_profile_serializer.save()
            return JsonResponse(user_profile_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view([ 'GET'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def all_doctors(request):
    try: 
        consults = Consult.objects.all()
        doctor_serializer = ConsultSerializer(consults, many=True)
        return Response(doctor_serializer.data)
    except Consult.DoesNotExist: 
        return JsonResponse({'message': 'consult does not exist'}, status=status.HTTP_200_OK) 

@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def doctor_profile_by_id(request):

    if request.method == 'GET':
        try: 
            data = JSONParser().parse(request) 
            user =  DoctorProfilee.objects.get(id_card=data["id_card"])
            serializer = DoctorProfileSerializer(user, many=False, context={"request": request})
            return Response(serializer.data)
    
        except DoctorProfilee.DoesNotExist: 
            return DoctorProfilee({'message': 'consult does not exist'}, status=status.HTTP_200_OK)

@api_view([ 'GET'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def pacient_consults(request):
    if request.method == 'GET':
        try: 
            params = JSONParser().parse(request) 
            pacient_id_card = params["pacient_id_card"]
            print("AAAddd", pacient_id_card)
            consults = Consult.objects.filter(pacient_id_card=pacient_id_card)
            print("PACIENTE CONSULTS  ", consults)
            serializer = ConsultSerializer(consults, many=True, context={"request": request})
            return Response(serializer.data)

        except Consult.DoesNotExist: 
            return JsonResponse({'message': 'consult does not exist'}, status=status.HTTP_200_OK) 
@api_view([ 'GET'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def doctor_consults(request):
    print("BBBBBB")
    if request.method == 'GET':
        try: 
            params = JSONParser().parse(request) 
            doctor_id_card = params["doctor_id_card"]
            print("DOCOTR", doctor_id_card)
            consults = Consult.objects.filter(doctor_id_card=doctor_id_card)
            print("DOCOTR CONSULTS  ", consults)
            serializer = ConsultSerializer(consults, many=True, context={"request": request})
            return Response(serializer.data)

        except Consult.DoesNotExist: 
            return JsonResponse({'message': 'consult does not exist'}, status=status.HTTP_200_OK) 

@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def create_consult(request):
    print("CREATE")
    if request.method == 'POST':
        consults_data = JSONParser().parse(request)
        consult_serializer = ConsultSerializer(data=consults_data)
        if consult_serializer.is_valid():
            consult_serializer.save()
            return JsonResponse(consult_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(consult_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def doctor_profile(request):
    if request.method == 'GET':
        try: 
            username = JSONParser().parse(request) 
            print("USERNAME  ", username)
            user =  DoctorProfilee.objects.get(username=username["username"])
            serializer = DoctorProfileSerializer(user, many=False, context={"request": request})
            return Response(serializer.data)
    
        except DoctorProfilee.DoesNotExist: 
            return DoctorProfilee({'message': 'consult does not exist'}, status=status.HTTP_200_OK) 


@api_view(['PUT', 'DELETE'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def hospital_consult(request,pk):
    try: 
        consult = Consult.objects.get(pk=pk) 
    except Consult.DoesNotExist: 
        return JsonResponse({'message': 'consult does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'PUT': 
            consults_data = JSONParser().parse(request) 
            consult_serializer = ConsultSerializer(consult, data=consults_data) 
            if consult_serializer.is_valid(): 
                consult_serializer.save() 
                return JsonResponse(consult_serializer.data) 
            return JsonResponse(consult_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        consult.delete() 
        return JsonResponse({'message': 'Consult was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def rooms(request):
    if request.method == 'GET': #mesmo que hospital_consults
        try:
            rooms = Room.objects.all()
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RoomSerializer(rooms, many=True, context={"request": request})
        return Response(serializer.data)
 
    elif request.method == 'POST':
        rooms_data = JSONParser().parse(request)
        room_serializer = RoomSerializer(data=rooms_data)
        if room_serializer.is_valid():
            room_serializer.save()
            return JsonResponse(room_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(room_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT', 'DELETE'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def room(request,pk):
    try: 
        room = Room.objects.get(pk=pk) 
    except Room.DoesNotExist: 
        return JsonResponse({'message': 'Room does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'PUT': 
            room_data = JSONParser().parse(request) 
            room_serializer = RoomSerializer(room, data=room_data) 
            if room_serializer.is_valid(): 
                room_serializer.save() 
                return JsonResponse(room_serializer.data) 
            return JsonResponse(room_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        room.delete() 
        return JsonResponse({'message': 'Room was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes([TokenAuthentication])
def room_consults(request):
    if request.method == 'GET': #mesmo que hospital_consults
        try:
            consultRoomReservation = ConsultRoomReservation.objects.all()
        except ConsultRoomReservation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ConsultRoomReservationSerializer(ConsultRoomReservation, many=True, context={"request": request})
        return Response(serializer.data)
 
    elif request.method == 'POST':
        cons_room_data = JSONParser().parse(request)
        cons_room_serializer = ConsultRoomReservationSerializer(data=cons_room_data)
        if cons_room_serializer.is_valid():
            cons_room_serializer.save()
            return JsonResponse(cons_room_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(cons_room_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT', 'DELETE'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def room_consult(request,pk):
    try: 
        consultRoomReservation = ConsultRoomReservation.objects.get(pk=pk) 
    except ConsultRoomReservation.DoesNotExist: 
        return JsonResponse({'message': 'ConsultRoomReservation does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'PUT': 
            consultRoomReservation_data = JSONParser().parse(request) 
            consultRoomReservation_serializer = ConsultRoomReservationSerializer(consultRoomReservation, data=consultRoomReservation_data) 
            if consultRoomReservation_serializer.is_valid(): 
                consultRoomReservation_serializer.save() 
                return JsonResponse(consultRoomReservation_serializer.data) 
            return JsonResponse(consultRoomReservation_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        consultRoomReservation.delete() 
        return JsonResponse({'message': 'consultRoomReservation was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes([TokenAuthentication])
def external_labs(request):
    if request.method == 'GET': #mesmo que hospital_consults
        try:
            externalLabs = ExternalLabs.objects.all()
        except ExternalLabs.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ExternalLabsSerializer(ExternalLabs, many=True, context={"request": request})
        return Response(serializer.data)
 
    elif request.method == 'POST':
        externalLabs_data = JSONParser().parse(request)
        externalLabs_serializer = ExternalLabsSerializer(data=externalLabs_data)
        if externalLabs_serializer.is_valid():
            externalLabs_serializer.save()
            return JsonResponse(externalLabs_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(externalLabs_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = ExternalLabsSerializer.objects.all().delete()
        return JsonResponse({'message': '{} Room were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT', 'DELETE'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def external_lab(request,pk):
    try: 
        externalLabs = ExternalLabs.objects.get(pk=pk) 
    except ConsultRoomReservation.DoesNotExist: 
        return JsonResponse({'message': 'External Lab does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'PUT': 
            externalLabs_data = JSONParser().parse(request) 
            externalLabs_data_serializer = ExternalLabsSerializer(externalLabs, data=externalLabs_data) 
            if externalLabs_data_serializer.is_valid(): 
                externalLabs_data_serializer.save() 
                return JsonResponse(externalLabs_data_serializer.data) 
            return JsonResponse(externalLabs_data_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        externalLabs.delete() 
        return JsonResponse({'message': 'External Lab was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)





#def home(request):
#    return render(request, 'home.html', {"form": "forms"})





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

def deleteConsult(request, id):
    consult = Consult.objects.get(id=id)
    consult.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def consults(request):
    consults = None
    user_type = None
    if request.user.is_authenticated:
        if request.user.is_superuser:
            print("HOSPITAL")
            consults = Consult.objects.all()
            user_type = 'H'
        
        elif Doctor.objects.filter(user_id=request.user.id).exists():
            print("DOCTOR")
            doctor = Doctor.objects.get(user__id= request.user.id)
            consults = Consult.objects.filter(doctor=doctor)
            user_type = 'D'
        
        return render(request, 'consults.html', {'consults': consults, 'user_type': user_type})
    return redirect('login')
"""



"""
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
                return redirect('doctor-signup')
        return render(request, 'signup.html', {'form': form})


def logout(request):
    logoutUser(request)
    return redirect('home')
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