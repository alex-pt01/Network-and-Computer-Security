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
    if request.method == 'GET':
        try: 
            params = JSONParser().parse(request) 
            doctor_id_card = params["doctor_id_card"]
            consults = Consult.objects.filter(doctor_id_card=doctor_id_card)
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
def hospital_consult(request,id):
    try: 
        consult = Consult.objects.get(id=id) 
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



@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def hospital_consult_by_id(request):
    print("SSSSSSS")
    if request.method == 'GET':
        try: 
            id = JSONParser().parse(request) 
            print("OOOOOOOOO ", id["id"])
            consult =  Consult.objects.get(id=str(id["id"]))
            print("11111111 ")
            serializer = ConsultSerializer(consult, many=False, context={"request": request})
            return Response(serializer.data)
    
        except DoctorProfilee.DoesNotExist: 
            return Consult({'message': 'consult does not exist'}, status=status.HTTP_200_OK) 



@api_view([ 'GET'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def all_room_reservations(request):
    try: 
        consultRoomReservation = ConsultRoomReservation.objects.all()
        consultRoomReservation_serializer = ConsultRoomReservationSerializer(consultRoomReservation, many=True)
        return Response(consultRoomReservation_serializer.data)
    except ConsultRoomReservation.DoesNotExist: 
        return JsonResponse({'message': 'ConsultRoomReservation does not exist'}, status=status.HTTP_200_OK) 




@api_view(['DELETE'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def del_room_reservation(request,id):
    try: 
        consultRoomReservation = ConsultRoomReservation.objects.get(id=id) 
    except ConsultRoomReservation.DoesNotExist: 
        return JsonResponse({'message': 'consultRoomReservation does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    if request.method == 'DELETE': 
        consultRoomReservation.delete() 
        return JsonResponse({'message': 'consultRoomReservation was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def create_room_reservation(request):
    print("CREATE")
    if request.method == 'POST':
        consult_room_data = JSONParser().parse(request)
        consult_room_serializer = ConsultRoomReservationSerializer(data=consult_room_data)
        if consult_room_serializer.is_valid():
            consult_room_serializer.save()
            return JsonResponse(consult_room_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(consult_room_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view([ 'GET'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def external_labs_report(request):
    try: 
        externalLabs = ExternalLabs.objects.all()
        pacient_serializer_serializer = ExternalLabsSerializer(externalLabs, many=True)
        return Response(pacient_serializer_serializer.data)
    except ExternalLabs.DoesNotExist: 
        return JsonResponse({'message': 'pacient does not exist'}, status=status.HTTP_200_OK) 


@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def create_external_labs_report(request):
    if request.method == 'POST':
        labs_data = JSONParser().parse(request)
        labs_serializer = ExternalLabsSerializer(data=labs_data)
        if labs_serializer.is_valid():
            labs_serializer.save()
            return JsonResponse(labs_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(labs_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def del_lab(request,id):
    try: 
        externalLabs = ExternalLabs.objects.get(id=id) 
    except ExternalLabs.DoesNotExist: 
        return JsonResponse({'message': 'ExternalLabs does not exist'}, status=status.HTTP_404_NOT_FOUND) 

    if request.method == 'DELETE': 
        externalLabs.delete() 
        return JsonResponse({'message': 'ExternalLabs was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def external_labs_by_doctor_id_card(request):
    print("SSSSSSS")
    if request.method == 'GET':
        try: 
            data = JSONParser().parse(request) 
            print("87654535478 ", data)
            consult =  ExternalLabs.objects.filter(doctor_id_card=data["doctor_id_card"])
            print("11111111 ")
            serializer = ExternalLabsSerializer(consult, many=True, context={"request": request})
            return Response(serializer.data)
    
        except DoctorProfilee.DoesNotExist: 
            return Consult({'message': 'consult does not exist'}, status=status.HTTP_200_OK) 


@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def check_is_admin(request):
    if request.method == 'GET':
       
        username = JSONParser().parse(request) 
        user =  DoctorProfilee.objects.filter(username=username["username"])
        print("USER ", user)
        if not user:
            
            return Response({"admin": True}, status=status.HTTP_200_OK)
        else:
            return Response({"admin": False}, status=status.HTTP_200_OK)





















