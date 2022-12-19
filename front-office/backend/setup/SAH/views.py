from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from SAH.forms import *
from SAH.models import *
from SAH.serializers import SignUpSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from SAH.serializers import *
from django.http import HttpRequest, HttpResponseRedirect
from time import strptime
from datetime import datetime
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser 
from django.http.response import JsonResponse
from rest_framework_simplejwt.backends import TokenBackend


User = get_user_model()
"""
def get_user_by_token(request, headers):
    token = headers.split(' ')[1]
    data = {'token': token}
    try:
        valid_data = TokenBackend(algorithm='HS256').decode(token,verify=True)
        user = valid_data['user']
        print("### ", user)
        request.user = user
    except ValidationError as v:
        print("validation error", v)
"""        

def create_jwt_pair_for_user(user: User):
    refresh = RefreshToken.for_user(user)
    tokens = {"access": str(refresh.access_token), "refresh": str(refresh)}
    return tokens

class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data
        print("DATA ", data)
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
            return Response(data={"message": "Invalid username or password"})

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}
        return Response(data=content, status=status.HTTP_200_OK)


def home(request):
    return render(request, 'home.html', {"form": "forms"})


    
@api_view([ 'GET', 'POST'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def consults(request):
    try: 
        username = JSONParser().parse(request) 
        pacient_id_card =  UserProfilee.objects.get(username=username["username"]).id_card
        consults = ConsultReservation.objects.get(pacient_id_card=pacient_id_card)
        serializer = ConsultReservationSerializer(consults, many=True, context={"request": request})
        return Response(serializer.data)
 
    except ConsultReservation.DoesNotExist: 
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
        user_profile_serializer = UserProfileSerializer(data=new_profile)
        if user_profile_serializer.is_valid():
            user_profile_serializer.save()
            return JsonResponse(user_profile_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#TODO-------------------------------------------------------------------°
@api_view([ 'GET', 'DELETE'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def consult_reservation_by_id_card(request,pk):
    try: 
        consult = ConsultReservation.objects.get(pk=pk) 
    except ConsultReservation.DoesNotExist: 
        return JsonResponse({'message': 'consult does not exist'}, status=status.HTTP_404_NOT_FOUND) 
    
    if request.method == 'GET': 
            consults_data = JSONParser().parse(request) 
            consult_serializer = ConsultReservationSerializer(consult, data=consults_data) 
            if consult_serializer.is_valid(): 
                consult_serializer.save() 
                return JsonResponse(consult_serializer.data) 
            return JsonResponse(consult_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        consult.delete() 
        return JsonResponse({'message': 'Consult was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'GET': 
        consult.delete() 
        return JsonResponse({'message': 'Consult was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
