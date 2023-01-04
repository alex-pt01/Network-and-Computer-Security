import json
import requests
from datetime import datetime
from OpenSSL import crypto        
import subprocess
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import rsa
import secrets
from DH import DH_Endpoint
#prime_numbers=[5381, 52711, 648391, 2269733, 9737333, 17624813, 37139213, 50728129, 77557187, 131807699, 174440041, 259336153, 326851121, 368345293, 440817757, 563167303, 718064159, 751783477, 997525853, 1107276647, 1170710369, 1367161723,52711, 648391, 9737333, 37139213, 174440041, 326851121, 718064159, 997525853, 1559861749, 2724711961, 3657500101, 5545806481, 7069067389, 8012791231, 9672485827, 12501968177, 16123689073, 16917026909, 22742734291,709, 5381, 52711, 167449, 648391, 1128889, 2269733, 3042161, 4535189, 7474967, 9737333, 14161729, 17624813, 19734581, 23391799, 29499439, 37139213, 38790341, 50728129, 56011909, 59053067, 68425619, 77557187, 87019979, 101146501, 113256643, 119535373, 127065427,	648391, 9737333, 174440041, 718064159, 3657500101, 7069067389, 16123689073, 22742734291, 36294260117, 64988430769, 88362852307, 136395369829, 175650481151, 200147986693, 243504973489, 318083817907, 414507281407]
#prime_numbers=[5381, 52711, 648391, 2269733, 9737333, 52711, 648391, 9737333, 709, 5381, 52711, 167449, 648391, 1128889, 2269733, 3042161, 4535189, 7474967, 9737333, 648391, 9737333, 15299, 87803, 219613, 318211, 506683, 919913, 1254739, 1471343, 1828669, 2364361, 3338989, 3509299, 4030889, 5054303, 5823667, 6478961, 6816631, 1787, 8527, 19577, 27457, 42043, 72727, 96797, 112129, 137077, 173867, 239489, 250751, 285191, 352007, 401519, 443419, 464939, 490643, 527623, 683873]
prime_numbers=[5381, 52711, 648391, 52711, 648391, 709, 5381, 52711, 167449, 648391, 648391, 15299, 87803, 219613, 318211, 506683, 919913, 1787, 8527, 19577, 27457, 42043, 72727, 96797, 112129, 137077, 173867, 239489, 250751, 285191, 352007, 401519, 443419, 464939, 490643, 527623, 683873,1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091,359, 383, 431, 439, 479, 503, 719, 839, 863, 887, 983, 1103, 1319, 1367, 1399, 1433, 1439, 1487, 1823, 1913, 2039, 2063, 2089, 2207, 2351, 2383, 2447, 2687, 2767, 2879, 2903, 2999, 3023, 3119, 3167, 3343]

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

global hash
hash="SHA-512"

HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
}


URL_HOSPITAL = "https://192.168.1.4:8003/"

hospital_data={}


with open("./Labex.crt", "r") as f:
        cert_buf = f.read()


#name é o nome do certicado com o .crt
params={"certificate" : cert_buf, "name": "Labex.crt"}
print(params)
resp = requests.post(URL_HOSPITAL+'protocol/hello/', headers = HEADERS ,data=json.dumps(params),verify=False)
resp=json.loads(resp.text)
name=resp["name"]

with open(resp["name"],'w') as f:
    f.write(resp["certicate"])
#now check certificate 
verify="openssl verify -verbose -CAfile ../CA/CA.crt "+name
output = subprocess.check_output(verify, shell=True)
outputStr = str(output.decode())

## contruir e destruir 
expected_res=name + ": OK" 
if outputStr.rstrip()  == expected_res :
    #openssl x509 -pubkey -noout -in keys/server.crt #validar a public key do certificado

    with open(name, "r") as f:
        server_buf = f.read()


    cert = crypto.load_certificate(crypto.FILETYPE_PEM, server_buf)
    date_format, encoding = "%Y%m%d%H%M%SZ", "ascii"
    not_before = datetime.strptime(cert.get_notBefore().decode(encoding), date_format)
    not_after = datetime.strptime(cert.get_notAfter().decode(encoding), date_format)
    now = datetime.now()

    https_error = "Error using HTTPS: "
    if now < not_before:
        msg = https_error + f"The certificate provided is not valid until {not_before}."
        verify = "rm "+name
        subprocess.check_output(verify, shell=True)

        print(msg)
        print("SERVIDOR FALSO")
        exit()

    if now > not_after:
        msg = https_error + f"The certificate provided expired on {not_after}."
        print(msg)
        verify = "rm "+name
        subprocess.check_output(verify, shell=True)
        print("SERVIDOR FALSO")
        exit()

    ### GET DA CHAVE PÚBLICA
    get_pub_string="openssl x509 -pubkey -noout -in "+name
    pub_key = subprocess.check_output(get_pub_string, shell=True)
    hospital_data["pub"]=pub_key
    verify = "rm "+name
    subprocess.check_output(verify, shell=True)

else:
    verify = "rm "+name
    subprocess.check_output(verify, shell=True)
    print("SERVIDOR FALSO")
    exit()

##### DH PART  ##########
p=resp["p"]
q=resp["q"]
private_key=secrets.choice(prime_numbers)
while private_key!= p and private_key != q :
    private_key=secrets.choice(prime_numbers)
lab_dh = DH_Endpoint(p, q, private_key)
lab_parcial_key=lab_dh.generate_partial_key()
#agora mandar o parcial para o servidor
params={"partial":lab_parcial_key,"certificate" : cert_buf, "name": "Labex.crt"}
resp = requests.post(URL_HOSPITAL+'protocol/dh/', headers = HEADERS ,data=json.dumps(params),verify=False)
resp=json.loads(resp.text)
hospital_key=resp["partial"]
s_full=lab_dh.generate_full_key(hospital_key)
print("CHAVE ESCOLHIDA ", s_full)
##### IF RUNNING FOR THE FIRST TIME YOU NEED TO SIGNUP
"""
campos=str({"email":"lab_externo1111@gmail.com","password":"LAB123xxxx...","username":"lab_externo1111"})
campos_cipher=lab_dh.encrypt_message(campos)
params={"certificate" : cert_buf, "name": "Labex.crt","data":campos_cipher}
resp = requests.post(URL_HOSPITAL+'protocol/signup/', headers = HEADERS ,data=json.dumps(params),verify=False)

campos=str({"phone_number":"965432111","address": "Rua do Horácio 123","lab_name":"Laboratório FERNANDES"})
campos_cipher=lab_dh.encrypt_message(campos)
params={"certificate" : cert_buf, "name": "Labex.crt","data":campos_cipher}
resp = requests.post(URL_HOSPITAL+'protocol/profileExternal/', headers = HEADERS ,data=json.dumps(params),verify=False)

"""
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
import rsa


####
with open("./Labex.key", "r") as key_file:
    privateKey = rsa.PrivateKey.load_pkcs1(key_file.read())


### NOW LET'S LOGIN 
campos=str({"password":"LAB123xxxx...","username":"lab_externo1111"})
campos_encode=campos.encode()

signature = b64encode(rsa.sign(campos_encode, privateKey, "SHA-512"))
"""
rsa_pub_key=RSA.importKey(pub_key)
verify = rsa.verify(campos_encode, b64decode(signature), rsa_pub_key)

"""
# Getting the current date and time
dt = datetime.now()

# getting the timestamp
ts = datetime.timestamp(dt)
print("login parametros pré cifra ",campos)
campos_cipher=lab_dh.encrypt_message(campos)
print("Login campos_cifrados ", campos_cipher)
params={"certificate" : cert_buf, "name": "Labex.crt","data":campos_cipher,"signature":(signature.decode()),"hash":"SHA-512","ts":ts}
print("login parametros " , params)
resp = requests.post(URL_HOSPITAL+'protocol/login/', headers = HEADERS ,data=json.dumps(params),verify=False)
resp=json.loads(resp.text)
print("Resposta ao login ", resp)
signature=resp["signature"].encode()
rsa_pub_key=RSA.importKey(pub_key)
campus=resp["response"]
campus_dec=lab_dh.decrypt_message(campus)
campus_dec = campus_dec.replace("\'", "\"")
campus_dec_final=json.loads(campus_dec)
initial_message=str(campus_dec_final).encode()
try:
    verify = rsa.verify(initial_message, b64decode(signature), rsa_pub_key)
except:
    print("fake server")
    exit()
###CHECK SERVER SIGNATURE
print("resposta descodificada " , initial_message)
if campus_dec_final["message"] == "Login Successfull":
    HEADERS["Authorization"]="Bearer "+campus_dec_final["tokens"]["access"]
else:
    print("SOMETHING WRONG HAPPEN")
    exit()
print("AUTHENTICATION SUCCESS NOW YOU CAN INTERACT")

while True:
    print("Options : ")
    print("0: EXIT")
    print("1: Get an Exam")
    print("2: Post an Exam")
    option = input("Which action you want to take? (1/2)")

    if option=="1":
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        params=str({"msg":"get_my_exams"})
        campos_encode=params.encode()
        signature = b64encode(rsa.sign(campos_encode, privateKey, "SHA-512"))
        campos_cipher=lab_dh.encrypt_message(params)
        params={"certificate" : cert_buf, "name": "Labex.crt","data":campos_cipher,"signature":(signature.decode()),"hash":"SHA-512","ts":ts}
        resp = requests.get(URL_HOSPITAL+'protocol/get-my-exams/', headers = HEADERS ,data=json.dumps(params),verify=False)
        resp=json.loads(resp.text)
        signature=resp["signature"].encode()
        rsa_pub_key=RSA.importKey(pub_key)
        campus=resp["response"]
        campus_dec=lab_dh.decrypt_message(campus)
        campus_dec = campus_dec.replace("\'", "\"")
        campus_dec_final=json.loads(campus_dec)
        initial_message=str(campus_dec_final).encode()
        try:
            verify = rsa.verify(initial_message, b64decode(signature), rsa_pub_key)
        except:
            print("fake server")
            exit()


        #### NEED TO CONTINUE THIS with print the possible tests from this lab 

        for k, v in campus_dec_final.items():
            print("ID: ",k, ".  Title: ", v)

        choose_number=input("CHOOSE DE REPORT HOW WANT TO SEE: (SELECT THE ID THE NUMBER)") 
        if choose_number in campus_dec_final.keys():
            choose=campus_dec_final[choose_number]
            choose_id = choose_number
            dt = datetime.now()
            ts = datetime.timestamp(dt)
            params=str({"id":choose_id})
            campos_encode=params.encode()
            signature = b64encode(rsa.sign(campos_encode, privateKey, "SHA-512"))
            campos_cipher=lab_dh.encrypt_message(params)
            print("CIFRADOS OS PARAMETROS " , campos_cipher)
            
            params={"certificate" : cert_buf, "name": "Labex.crt","data":campos_cipher,"signature":(signature.decode()),"hash":"SHA-512","ts":ts}
            resp = requests.get(URL_HOSPITAL+'protocol/get-exam/', headers = HEADERS ,data=json.dumps(params),verify=False)
            resp=json.loads(resp.text)
            print("DADOS PRÉ DECIFRAR " , resp)
            signature=resp["signature"].encode()
            rsa_pub_key=RSA.importKey(pub_key)
            campus=resp["response"]
            campus_dec=lab_dh.decrypt_message(campus)
            campus_dec = campus_dec.replace("\'", "\"")
            campus_dec_final=json.loads(campus_dec)
            initial_message=str(campus_dec_final).encode()

            try:
                verify = rsa.verify(initial_message, b64decode(signature), rsa_pub_key)
            except:
                print("fake server")
                exit()
            hash_=campus_dec_final["hash"].encode()
            del campus_dec_final["hash"]
            del campus_dec_final["id"]
            print("O MEU RELATÓRIO ", campus_dec_final)
            validate_values=str(campus_dec_final)
            campos_encode=validate_values.encode()
            signature = b64encode(rsa.sign(campos_encode, privateKey, "SHA-512"))
            if signature == hash_:
                print("The hash is right")
                print(campus_dec_final)
            
            else:
                print("This was not signed by us")
        else: 
            print("That options doesn't exist")
    elif option=="2":
        try:
            # 1234567890
            pacient_id_card=int(input("Insert the patient id card number :"))
            # 123456785
            doctor_id_card=int(input("Insert the doctor id card number :"))
            lab_name="lab_externo1111"
            consult_date=input("Insert the consult date  in the format(DD-MM-YYYY) :")
            update_date=input("Insert the update date  in the format(DD-MM-YYYY) :")
            intro=input("Insert a title for this exam:")
            materials=input("Materials used:")
            procedure=input("Procedure done:")
            results=input("Results of this exam:")
        except:
            print("ERROR SOMETHING WAS WRONG")
        dt = datetime.now()
        ts = datetime.timestamp(dt)
        params=str({"pacient_id_card":pacient_id_card,"doctor_id_card":doctor_id_card, "lab_name":lab_name, "consult_lab_date": consult_date,
        "form_update_date": update_date, "intro": intro, "materials": materials, "procedure": procedure, "results": results })
        campos_encode=params.encode()
        signature = b64encode(rsa.sign(campos_encode, privateKey, "SHA-512"))
        campos_cipher=lab_dh.encrypt_message(params)
        params={"certificate" : cert_buf, "name": "Labex.crt","data":campos_cipher,"signature":(signature.decode()),"hash":"SHA-512","ts":ts}
        resp = requests.post(URL_HOSPITAL+'protocol/new-exam/', headers = HEADERS ,data=json.dumps(params),verify=False)
        resp=json.loads(resp.text)
        signature=resp["signature"].encode()
        rsa_pub_key=RSA.importKey(pub_key)
        campus=resp["response"]
        campus_dec=lab_dh.decrypt_message(campus)
        campus_dec = campus_dec.replace("\'", "\"")
        campus_dec_final=json.loads(campus_dec)
        initial_message=str(campus_dec_final).encode()
        try:
            verify = rsa.verify(initial_message, b64decode(signature), rsa_pub_key)
        except:
            print("fake server")
            exit()
        if campus_dec_final["status"] == "ACCEPTED":
            print("CREATE SUCCESS")
        else:
            print("CREATE NOT SUCCESS")

    elif option == "0":
        break
    else:
        print("WRONG OPTION")

params={"certificate" : cert_buf, "name": "Labex.crt"}
resp = requests.post(URL_HOSPITAL+'protocol/logout/', headers = HEADERS ,data=json.dumps(params),verify=False)

#####Testes 



