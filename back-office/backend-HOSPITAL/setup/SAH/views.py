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
from .DH import DH_Endpoint
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
import rsa

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

User = get_user_model()

#prime_numbers=[5381, 52711, 648391, 2269733, 9737333, 17624813, 37139213, 50728129, 77557187, 131807699, 174440041, 259336153, 326851121, 368345293, 440817757, 563167303, 718064159, 751783477, 997525853, 1107276647, 1170710369, 1367161723,52711, 648391, 9737333, 37139213, 174440041, 326851121, 718064159, 997525853, 1559861749, 2724711961, 3657500101, 5545806481, 7069067389, 8012791231, 9672485827, 12501968177, 16123689073, 16917026909, 22742734291,709, 5381, 52711, 167449, 648391, 1128889, 2269733, 3042161, 4535189, 7474967, 9737333, 14161729, 17624813, 19734581, 23391799, 29499439, 37139213, 38790341, 50728129, 56011909, 59053067, 68425619, 77557187, 87019979, 101146501, 113256643, 119535373, 127065427,	648391, 9737333, 174440041, 718064159, 3657500101, 7069067389, 16123689073, 22742734291, 36294260117, 64988430769, 88362852307, 136395369829, 175650481151, 200147986693, 243504973489, 318083817907, 414507281407]
prime_numbers=[5381, 52711, 648391, 52711, 648391, 709, 5381, 52711, 167449, 648391, 648391, 15299, 87803, 219613, 318211, 506683, 919913, 1787, 8527, 19577, 27457, 42043, 72727, 96797, 112129, 137077, 173867, 239489, 250751, 285191, 352007, 401519, 443419, 464939, 490643, 527623, 683873]


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

import subprocess
from datetime import datetime
from OpenSSL import crypto    
import secrets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

dic_external_labs={}

@api_view(['POST'])
@permission_classes((AllowAny,))
def hello(request):
    if 'certificate' in request.data and 'name' in request.data :
        certificate=(request.data.get("certificate"))
        name =(request.data.get("name"))
        with open(name,'w') as f:
            f.write(certificate)
        #now check certificate 
        verify="openssl verify -verbose -CAfile keys/CA.crt "+name
        output = subprocess.check_output(verify, shell=True)
        outputStr = str(output.decode())

        ## contruir e destruir 
        expected_res=name + ": OK" 
        if outputStr.rstrip()  == expected_res :
            print("CERTIFICADO ACEITE")
            #openssl x509 -pubkey -noout -in keys/server.crt #validar a public key do certificado

            with open(name, "r") as f:
                cert_buf = f.read()

            cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_buf)
            date_format, encoding = "%Y%m%d%H%M%SZ", "ascii"
            not_before = datetime.strptime(cert.get_notBefore().decode(encoding), date_format)
            not_after = datetime.strptime(cert.get_notAfter().decode(encoding), date_format)
            now = datetime.now()

            https_error = "Error using HTTPS: "
            if now < not_before:
                msg = https_error + f"The certificate provided is not valid until {not_before}."
                print(msg)
                return Response({"data": "Invalid Certificate"}, status=status.HTTP_400_BAD_REQUEST)
            if now > not_after:
                msg = https_error + f"The certificate provided expired on {not_after}."
                print(msg)
                return Response({"data": "Invalid Certificate"}, status=status.HTTP_400_BAD_REQUEST)

            ### GET DA CHAVE PÚBLICA
            get_pub_string="openssl x509 -pubkey -noout -in "+name
            pub_key = subprocess.check_output(get_pub_string, shell=True)
            with open("./keys/server.crt", "r") as file:
                server_cert = file.read()

            # Getting the current date and time
            dt = datetime.now()

            # getting the timestamp
            ts = datetime.timestamp(dt)
            nonce = secrets.token_hex(8)  

            #Mas na primeira mensagem de hello, os parametros públicos são logo enviados pelo servidor
            p=secrets.choice(prime_numbers)
            q=secrets.choice(prime_numbers)
            private_key=secrets.choice(prime_numbers)
            external_lab_data=[pub_key,p,q,private_key]
            dic_external_labs[name]=external_lab_data
            return Response({"certicate": server_cert, "name":"server.crt","TS": ts,"nonce":nonce,"p":p,"q":q}, status=status.HTTP_200_OK)
        else:
            print("CERTIFICADO FALSO")

        verify = "rm "+name
        subprocess.check_output(verify, shell=True)
    return Response({"data": "Invalid Certificate"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes((AllowAny,))
def DH(request):
    ## AQUI VAMOS FAZER A PARTE DO DH 
    print(request.data)
    if 'certificate' in request.data and 'name' in request.data and 'partial' in request.data :
        certificate=(request.data.get("certificate"))
        name =(request.data.get("name"))
        with open(name,'w') as f:
            f.write(certificate)
        #now check certificate 
            
        verify="openssl verify -verbose -CAfile keys/CA.crt "+name
        output = subprocess.check_output(verify, shell=True)
        outputStr = str(output.decode())

        ## contruir e destruir 
        expected_res=name + ": OK" 
        if outputStr.rstrip()  == expected_res :
            print("CERTIFICADO ACEITE")
            #openssl x509 -pubkey -noout -in keys/server.crt #validar a public key do certificado

            with open(name, "r") as f:
                cert_buf = f.read()

            cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_buf)
            date_format, encoding = "%Y%m%d%H%M%SZ", "ascii"
            not_before = datetime.strptime(cert.get_notBefore().decode(encoding), date_format)
            not_after = datetime.strptime(cert.get_notAfter().decode(encoding), date_format)
            now = datetime.now()

            https_error = "Error using HTTPS: "
            if now < not_before:
                msg = https_error + f"The certificate provided is not valid until {not_before}."
                print(msg)
                return Response({"data": "Invalid Certificate"}, status=status.HTTP_400_BAD_REQUEST)
            if now > not_after:
                msg = https_error + f"The certificate provided expired on {not_after}."
                return Response({"data": "Invalid Certificate"}, status=status.HTTP_400_BAD_REQUEST)

            ### GET DA CHAVE PÚBLICA
            get_pub_string="openssl x509 -pubkey -noout -in "+name
            pub_key = subprocess.check_output(get_pub_string, shell=True)
            ### START 
            if dic_external_labs[name][0]== pub_key:
                #CONFERE
                lab_dh = DH_Endpoint(dic_external_labs[name][1], dic_external_labs[name][2], dic_external_labs[name][3])
                lab_parcial_key=lab_dh.generate_partial_key()
                external_lab_parcial=request.data.get("partial")
                key_exc=lab_dh.generate_full_key(external_lab_parcial)
                external_lab_data=[pub_key,lab_dh]
                dic_external_labs[name]=external_lab_data
                print("CHAVE ESCOLHIDA ", key_exc)

                return Response({"partial": lab_parcial_key}, status=status.HTTP_200_OK)
            else:
                return Response({"data": "Invalid Certificate"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"data": "Invalid Certificate"}, status=status.HTTP_400_BAD_REQUEST)


class SignUpView_External_Lab(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data
        if "name" in data :
            try:
                values_stored=dic_external_labs[data["name"]]
            except:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            certificate=(data.get("certificate"))
            name =(request.data.get("name"))
            with open(name,'w') as f:
                f.write(certificate)
            #now check certificate 
                
            verify="openssl verify -verbose -CAfile keys/CA.crt "+name
            output = subprocess.check_output(verify, shell=True)
            outputStr = str(output.decode())

            ## contruir e destruir 
            expected_res=name + ": OK" 
            if outputStr.rstrip()  == expected_res :
                ### GET DA CHAVE PÚBLICA
                get_pub_string="openssl x509 -pubkey -noout -in "+name
                pub_key = subprocess.check_output(get_pub_string, shell=True)
                if pub_key ==values_stored[0]:
                    campus=data["data"]
                    campus_dec=values_stored[1].decrypt_message(campus)
                    campus_dec = campus_dec.replace("\'", "\"")
                    campus_dec_final=json.loads(campus_dec)
                    serializer = self.serializer_class(data=campus_dec_final)
                    if serializer.is_valid():
                        serializer.save()
                        response = {"message": "User Created Successfully", "data": "User Created Successfully"}
                        return Response(response,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def fill_profile_external_lab(request):
    new_profile = {}
    data=request.data
    if "name" in request.data :
        try:
            values_stored=dic_external_labs[data["name"]]
        except:
            return Response( status=status.HTTP_400_BAD_REQUEST)
        certificate=(data.get("certificate"))
        name =(request.data.get("name"))
        with open(name,'w') as f:
            f.write(certificate)
        #now check certificate 
            
        verify="openssl verify -verbose -CAfile keys/CA.crt "+name
        output = subprocess.check_output(verify, shell=True)
        outputStr = str(output.decode())

        ## contruir e destruir 
        expected_res=name + ": OK" 
        if outputStr.rstrip()  == expected_res :
            ### GET DA CHAVE PÚBLICA
            get_pub_string="openssl x509 -pubkey -noout -in "+name
            pub_key = subprocess.check_output(get_pub_string, shell=True)
            if pub_key ==values_stored[0]:
                campus=data["data"]
                campus_dec=values_stored[1].decrypt_message(campus)
                campus_dec = campus_dec.replace("\'", "\"")
                campus_dec_final=json.loads(campus_dec)
                user_profile_data =(campus_dec_final)
                user = User.objects.all().last()
                new_profile['username']=user.username
                new_profile.update(user_profile_data)
                print("NEW USER PROFILE  ", new_profile)
                lab_profile_serializer = ExternalLabProfileSerializer(data=new_profile)
                if lab_profile_serializer.is_valid():
                    lab_profile_serializer.save()
                    return JsonResponse({"data": "User Created Successfully"},status=status.HTTP_201_CREATED) 
               


    return JsonResponse(lab_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

global hash
hash="SHA-512"

@api_view(['POST'])
@permission_classes((AllowAny,))
def Login_External_View(request):
    data=request.data
    if "name" in data :
        try:
            values_stored=dic_external_labs[data["name"]]
        except:
            return Response( status=status.HTTP_400_BAD_REQUEST)
        certificate=(data.get("certificate"))
        name =(request.data.get("name"))
        with open(name,'w') as f:
            f.write(certificate)
        #now check certificate 
            
        verify="openssl verify -verbose -CAfile keys/CA.crt "+name
        output = subprocess.check_output(verify, shell=True)
        outputStr = str(output.decode())
        ## contruir e destruir 
        expected_res=name + ": OK" 
        if outputStr.rstrip()  == expected_res :
            ### GET DA CHAVE PÚBLICA
            get_pub_string="openssl x509 -pubkey -noout -in "+name
            pub_key = subprocess.check_output(get_pub_string, shell=True)
            if pub_key ==values_stored[0]:
                campus=data["data"]
                campus_dec=values_stored[1].decrypt_message(campus)
                campus_dec = campus_dec.replace("\'", "\"")
                campus_dec_final=json.loads(campus_dec)
                rsa_pub_key=RSA.importKey(pub_key)
                signature=data["signature"].encode()
                initial_message=str(campus_dec_final).encode()
                try:
                    verify = rsa.verify(initial_message, b64decode(signature), rsa_pub_key)
                    username = campus_dec_final["username"]
                    password = campus_dec_final["password"]
                    dic_external_labs[data["name"]]=[values_stored[0],values_stored[1],username]
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        tokens = create_jwt_pair_for_user(user)

                        with open("./keys/server.key", "r") as key_file:
                            privateKey = rsa.PrivateKey.load_pkcs1(key_file.read())

                        response = str({"message": "Login Successfull", "tokens": tokens})
                        response_encrypted=values_stored[1].encrypt_message(response)
                       
                        campos_encode=response.encode()
                        dt=datetime.now()
                        ts = datetime.timestamp(dt)
                        signature_server = b64encode(rsa.sign(campos_encode, privateKey, "SHA-512"))
                        response={}
                        response["ts"]=ts
                        response["signature"]=signature_server
                        response["response"]=response_encrypted
                        return Response(data=response, status=status.HTTP_200_OK)
                    else:
                        response = str({"message": "Invalid email or password"})
                        response_encrypted=values_stored[1].encrypt_message(response)
                        response={}
                        response["response"]=response_encrypted
                        return Response(data=response, status=status.HTTP_200_OK)
                except:
                    return Response( status=status.HTTP_400_BAD_REQUEST)
  

    return Response( status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def logout_protocol_view(request):
    logoutUser(request)
    if 'certificate' in request.data and 'name' in request.data :
        certificate=(request.data.get("certificate"))
        name =(request.data.get("name"))
        try:
            values_stored=dic_external_labs[data["name"]]
        except:
            return Response(status=status.HTTP_200_OK)

        get_pub_string="openssl x509 -pubkey -noout -in "+name
        pub_key = subprocess.check_output(get_pub_string, shell=True)
        if pub_key == values_stored[0]:
            del dic_external_labs["name"]
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def new_exam(request):
    data=request.data
    if "name" in data :
        try:
            values_stored=dic_external_labs[data["name"]]
        except:
            return Response( status=status.HTTP_400_BAD_REQUEST)
        certificate=(data.get("certificate"))
        name =(request.data.get("name"))
        with open(name,'w') as f:
            f.write(certificate)
        #now check certificate 
            
        verify="openssl verify -verbose -CAfile keys/CA.crt "+name
        output = subprocess.check_output(verify, shell=True)
        outputStr = str(output.decode())
        ## contruir e destruir 
        expected_res=name + ": OK" 
        if outputStr.rstrip()  == expected_res :
            ### GET DA CHAVE PÚBLICA
            get_pub_string="openssl x509 -pubkey -noout -in "+name
            pub_key = subprocess.check_output(get_pub_string, shell=True)
            if pub_key ==values_stored[0]:
                campus=data["data"]
                campus_dec=values_stored[1].decrypt_message(campus)
                campus_dec = campus_dec.replace("\'", "\"")
                campus_dec_final=json.loads(campus_dec)
                rsa_pub_key=RSA.importKey(pub_key)
                signature=data["signature"].encode()
                initial_message=str(campus_dec_final).encode()
                try:
                    verify = rsa.verify(initial_message, b64decode(signature), rsa_pub_key)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                    
                if campus_dec_final["lab_name"] == values_stored[2]:
                    ### AGORA AQUI VAMOS LER TODOS OS EXAMES DESTE HOSPITAL
                    signature= signature.decode()
                    print(signature)
                    campus_dec_final["hash"]=signature
                    user_profile_serializer = ExternalLabsSerializer(data=campus_dec_final)
                    if user_profile_serializer.is_valid():
                        user_profile_serializer.save()
                        with open("./keys/server.key", "r") as key_file:
                            privateKey = rsa.PrivateKey.load_pkcs1(key_file.read())

                        response = str({"status":"ACCEPTED"})
                        response_encrypted=values_stored[1].encrypt_message(response)
                        campos_encode=response.encode()
                        print(campos_encode)
                        dt=datetime.now()
                        ts = datetime.timestamp(dt)
                        signature_server = b64encode(rsa.sign(campos_encode, privateKey, "SHA-512"))
                        response={}
                        response["ts"]=ts
                        response["signature"]=signature_server
                        response["response"]=response_encrypted
                        return Response(data=response, status=status.HTTP_200_OK)
                with open("./keys/server.key", "r") as key_file:
                    privateKey = rsa.PrivateKey.load_pkcs1(key_file.read())
                response = str({"status":"NotACCEPTED"})
                response_encrypted=values_stored[1].encrypt_message(response)
                campos_encode=response.encode()
                print(campos_encode)
                dt=datetime.now()
                ts = datetime.timestamp(dt)
                signature_server = b64encode(rsa.sign(campos_encode, privateKey, "SHA-512"))
                response={}
                response["ts"]=ts
                response["signature"]=signature_server
                response["response"]=response_encrypted
                return Response(data=response, status=status.HTTP_200_OK)

    return JsonResponse(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def get_my_exams(request):
    data=request.data
    if "name" in data :
        try:
            values_stored=dic_external_labs[data["name"]]
        except:
            return Response( status=status.HTTP_400_BAD_REQUEST)
        certificate=(data.get("certificate"))
        name =(request.data.get("name"))
        with open(name,'w') as f:
            f.write(certificate)
        #now check certificate 
            
        verify="openssl verify -verbose -CAfile keys/CA.crt "+name
        output = subprocess.check_output(verify, shell=True)
        outputStr = str(output.decode())
        ## contruir e destruir 
        expected_res=name + ": OK" 
        if outputStr.rstrip()  == expected_res :
            ### GET DA CHAVE PÚBLICA
            get_pub_string="openssl x509 -pubkey -noout -in "+name
            pub_key = subprocess.check_output(get_pub_string, shell=True)
            if pub_key ==values_stored[0]:
                campus=data["data"]
                campus_dec=values_stored[1].decrypt_message(campus)
                campus_dec = campus_dec.replace("\'", "\"")
                campus_dec_final=json.loads(campus_dec)
                rsa_pub_key=RSA.importKey(pub_key)
                signature=data["signature"].encode()
                initial_message=str(campus_dec_final).encode()
                try:
                    verify = rsa.verify(initial_message, b64decode(signature), rsa_pub_key)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

                
                ### AGORA AQUI VAMOS LER TODOS OS EXAMES DESTE HOSPITAL
                username=values_stored[2]
                exams=ExternalLabs.objects.filter(lab_name=username)

                ret_values={}
                for exam in exams:
                    ret_values[str(exam.id)]=exam.intro
                
                ### ver como cifrar uma lista e depois enviar 
                print(ret_values)
                with open("./keys/server.key", "r") as key_file:
                    privateKey = rsa.PrivateKey.load_pkcs1(key_file.read())

                response = str(ret_values)
                response_encrypted=values_stored[1].encrypt_message(response)
                campos_encode=response.encode()
                print(campos_encode)
                dt=datetime.now()
                ts = datetime.timestamp(dt)
                signature_server = b64encode(rsa.sign(campos_encode, privateKey, "SHA-512"))
                response={}
                response["ts"]=ts
                response["signature"]=signature_server
                response["response"]=response_encrypted
                return Response(data=response, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes([TokenAuthentication])
def get_exam(request):
    data=request.data
    if "name" in data :
        try:
            values_stored=dic_external_labs[data["name"]]
        except:
            return Response( status=status.HTTP_400_BAD_REQUEST)
        certificate=(data.get("certificate"))
        name =(request.data.get("name"))
        with open(name,'w') as f:
            f.write(certificate)
        #now check certificate 
            
        verify="openssl verify -verbose -CAfile keys/CA.crt "+name
        output = subprocess.check_output(verify, shell=True)
        outputStr = str(output.decode())
        ## contruir e destruir 
        expected_res=name + ": OK" 
        if outputStr.rstrip()  == expected_res :
            ### GET DA CHAVE PÚBLICA
            get_pub_string="openssl x509 -pubkey -noout -in "+name
            pub_key = subprocess.check_output(get_pub_string, shell=True)
            if pub_key ==values_stored[0]:
                campus=data["data"]
                campus_dec=values_stored[1].decrypt_message(campus)
                campus_dec = campus_dec.replace("\'", "\"")
                campus_dec_final=json.loads(campus_dec)
                rsa_pub_key=RSA.importKey(pub_key)
                signature=data["signature"].encode()
                initial_message=str(campus_dec_final).encode()
                try:
                    verify = rsa.verify(initial_message, b64decode(signature), rsa_pub_key)
                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

                
                ### AGORA AQUI VAMOS LER TODOS OS EXAMES DESTE HOSPITAL
                username=values_stored[2]
                exams=ExternalLabs.objects.get(lab_name=username,id=int(campus_dec_final["id"]))
                ret_values = ExternalLabsSerializer(exams)
                ret_values=ret_values.data                
                ### ver como cifrar uma lista e depois enviar 
                print(ret_values)
                with open("./keys/server.key", "r") as key_file:
                    privateKey = rsa.PrivateKey.load_pkcs1(key_file.read())

                response = str(ret_values)
                response_encrypted=values_stored[1].encrypt_message(response)
                campos_encode=response.encode()
                print(campos_encode)
                dt=datetime.now()
                ts = datetime.timestamp(dt)
                signature_server = b64encode(rsa.sign(campos_encode, privateKey, "SHA-512"))
                response={}
                response["ts"]=ts
                response["signature"]=signature_server
                response["response"]=response_encrypted
                return Response(data=response, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
