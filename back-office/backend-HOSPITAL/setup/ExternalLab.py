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
prime_numbers=[5381, 52711, 648391, 52711, 648391, 709, 5381, 52711, 167449, 648391, 648391, 15299, 87803, 219613, 318211, 506683, 919913, 1787, 8527, 19577, 27457, 42043, 72727, 96797, 112129, 137077, 173867, 239489, 250751, 285191, 352007, 401519, 443419, 464939, 490643, 527623, 683873]


HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
}


URL_HOSPITAL = "http://192.168.1.4:8003/"

hospital_data={}


with open("./keys/server.crt", "r") as f:
        cert_buf = f.read()


#name é o nome do certicado com o .crt
params={"certificate" : cert_buf, "name": "server.crt"}

resp = requests.post(URL_HOSPITAL+'protocol/hello/', headers = HEADERS ,data=json.dumps(params))
resp=json.loads(resp.text)
name=resp["name"]

with open(resp["name"],'w') as f:
    f.write(resp["certicate"])
#now check certificate 
verify="openssl verify -verbose -CAfile keys/CA.crt "+name
output = subprocess.check_output(verify, shell=True)
outputStr = str(output.decode())

## contruir e destruir 
expected_res=name + ": OK" 
if outputStr.rstrip()  == expected_res :
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
lab_dh = DH_Endpoint(p, q, private_key)
lab_parcial_key=lab_dh.generate_partial_key()
#agora mandar o parcial para o servidor
params={"partial":lab_parcial_key,"certificate" : cert_buf, "name": "server.crt"}
resp = requests.post(URL_HOSPITAL+'protocol/dh/', headers = HEADERS ,data=json.dumps(params))
resp=json.loads(resp.text)
hospital_key=resp["partial"]
s_full=lab_dh.generate_full_key(hospital_key)
print("CHAVE ESCOLHIDA ", s_full)
##### IF RUNNING FOR THE FIRST TIME YOU NEED TO SIGNUP
"""
campos=str({"email":"lab_externo@gmail.com","password":"LAB123xxxx...","username":"lab_externo"})
campos_cipher=lab_dh.encrypt_message(campos)
params={"certificate" : cert_buf, "name": "server.crt","data":campos_cipher}
resp = requests.post(URL_HOSPITAL+'protocol/signup/', headers = HEADERS ,data=json.dumps(params))

campos=str({"phone_number":"965432111","address": "Rua do Horácio 123","lab_name":"Laboratório Horácio"})
campos_cipher=lab_dh.encrypt_message(campos)
params={"certificate" : cert_buf, "name": "server.crt","data":campos_cipher}
resp = requests.post(URL_HOSPITAL+'protocol/profileExternal/', headers = HEADERS ,data=json.dumps(params))
"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
import rsa


####
with open("./keys/server.key", "r") as key_file:
    privateKey = rsa.PrivateKey.load_pkcs1(key_file.read())


### NOW LET'S LOGIN 
campos=str({"password":"LAB123xxxx...","username":"lab_externo"})
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
campos_cipher=lab_dh.encrypt_message(campos)
params={"certificate" : cert_buf, "name": "server.crt","data":campos_cipher,"signature":(signature.decode()),"hash":"SHA-512","ts":ts}
resp = requests.post(URL_HOSPITAL+'protocol/login/', headers = HEADERS ,data=json.dumps(params))
resp=json.loads(resp.text)
HEADERS["Authorization"]="Bearer "+resp["tokens"]["access"]


#####Testes 

