# Healthcare: SAH
<p align="center">
  <img src="logo.png" style="width: 40%;
    height: auto;" />
</p>

Saint Acutis hospital has operated in Portugal since 2020. It provides Urgent Care, open 24/7 (24 hours, 7 days a week). It also provides Specialty Consultations, including: Orthopedic, Cardiology, and Dermatology.

The front-office of the hospital offers both a public web site, for displaying general information, and a customer web site, where patients can check their appointments and make new ones. There is also a mobile application that provides the same functionality.

The back-office is used to manage the schedule, the room reservations, and the medical records. The system has integrations with external institutions, namely, the Ministry for Health, and several exam facilities and laboratories.

Briefly in this document you can find general information about the problems that our project solves as well as the technologies used in its creation, then everything you need to know to test our project, memsom deployment demo and additional information about the authors, contributions and acknowledgments.

## General Information

This section expands on the introductory paragraph to give readers a better understanding of your project. 
Include a brief description and answer the question, "what problem does this project solve?"

Our hospital provides urgent care, open 24/7 (24 hours, 7 days a week) as well as speciality consultations, including: orthopedy, cardiology, and dermatology. 

### Built With

In order to create the applications we used the django framework with the SQLite database since it allows rapid development of secure and maintainable websites. In order to develop the CA (Certificate Authority) we used OpenSSL that is free, open-source library used for digital certificates and the libraries used for cryptography were: 

* [Django](https://www.djangoproject.com/) - Python web framework
* [SQLite](https://www.sqlite.org/index.html) - SQL database engine
* [OpenSSL](https://www.openssl.org/) -  Programming library used to implement encryption and authentication

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

In order to use our system you need to use an electronic device such as a computer that has the [Linux](https://www.linux.com/what-is-linux/) operating system.
Open the Terminal program. This is usually found under Utilities or Accessories.
To use the **django framework** you need to use the following requirements:

Install the virtualenv package
```
pip3 install virtualenv
```

Create the virtual environment
```
virtualenv django
```

Activate the virtual environment
```
source django/bin/activate
```

Install the Django code
```
python3 -m pip install django
```

Install django-allauth that deals with account authentication, registration, management, and third-party (social) account authentication.
```
python3 -m pip install django-allauth
```

Install django-sslserver that helps to run the server with the certificate we are to create.
```
pip3 install django-sslserver
```

Install debug-toolbar is a configurable set of panels that display various debug information about the current request/response and when clicked, display more details about the panel's content.
```
pip3 install django-debug-toolbar
```

Create superuser if you need a new one or use (username: adminsirs; password: @adsirs123)the one who can log into admin page and who can have permissions to add, edit, delete objects in thru admin page
```
pip3 install django-createsuperuser
```

To create an API endpoints (code that allows two software programs to communicate with each other)
```
pip3 install djangorestframework
pip3 install django-cors-headers
pip3 install serializers
pip3 install djangorestframework-simplejwt
```

Install ratelimit. Rate limiting blocks users, bots, or applications that are over-using or abusing a web property. 
```
pip3 install ratelimit
```

Install pyOpenSSL. The following modules are defined: Elliptic curves. Serialization and deserialization. Signing and verifying signatures.
```
pip3 install pyOpenSSL
```

Install RSA library. It supports encryption and decryption, signing and verifying signatures, and key generation 
```
pip3 install rsa
```

Install OS module. The OS module in python provides functions for interacting with the operating system´´´
```
pip3 install os-sys
```

To setup our project environment to be used with [SEED-Ubuntu20.04](https://seedsecuritylabs.org/labsetup.html) (username: seeds, password: dees), you need to have 4 instances of VMs. For each machine, after editing the file mentioned below run:
```
sudo netplan try
sudo netplan apply
```
and
```
sudo apt install iptables-persistent
```
to make the iptables rules persistent.

**VM1: Ministry of Health**
```
Network adapter 1 : Internal network , name : sw-1 (Promiscuous MODE : Allow VMS)
IP: 192.168.0.100 
Gateway:192.168.0.10
```

Then you need to copy the contents of the file [vm1.yml](VMs%20config/vm1.yml)
 and paste into /etc/netplan/01-network-manager-all.yaml on VM1.
 
**VM2: Router/Firewall**
```
Network adapter 1: Internal Network , name : sw-1 (GENERATE NEW MAC ADDRESSES) (Promiscuous MODE : Allow VMS)
IP:192.168.0.10
Network adapter 2: Internal Network , name sw-2 (Promiscuous MODE : Allow VMS)
IP:192.168.1.254
Adapter 3: associated with NAT.
```
Then you need to copy the contents of the file [vm2.yml](VMs%20config/vm2.yml)
 and paste into /etc/netplan/01-network-manager-all.yaml on VM2.
 
**VM3: Front-Office app**
```
Network adapter 1: Internal network, name sw-2 (Promiscuous MODE: Allow VMS)
IP:192.168.1.3
Gateway:192.168.1.254
```
Then you need to copy the contents of the file [vm3.yml](VMs%20config/vm3.yml)
 and paste into /etc/netplan/01-network-manager-all.yaml on VM3.
 
**VM4: Back-Office app**
```
Network adapter 1: Internal network, name sw-2 (Promiscuous MODE : Allow VMS)
IP:192.168.1.4
Gateway:192.168.1.254
```
Then you need to copy the contents of the file [vm4.yml](VMs%20config/vm4.yml)
 and paste into /etc/netplan/01-network-manager-all.yaml on VM4.
 



#TODO -> alterar os files e os links

Then you need to configure the **firewalls** using the following configuration files:

* [Firewall configuration file for VM2](Firewalls%20config/firewall_VM2.txt)
* [Firewall configuration file for VM3](Firewalls%20config/firewall_VM3.txt)
* [Firewall configuration file for VM4](Firewalls%20config/firewall_VM4.txt)


### Installing

For each machine, follow the next steps:
(**NOTE**: do not change the name of the certificates!)

**VM1: Ministry of Health**

Create 2 folders with the name **CA** and **lab**
In **CA** folder:
```
openssl genrsa -out CA.key
openssl rsa -in CA.key -pubout > public.key
openssl req -new -key CA.key -out CA.csr 
openssl x509 -req -days 365 -in CA.csr -signkey CA.key -out CA.crt
echo 01 > CA.srl
```
In **lab** folder:
```
openssl genrsa -out Labex.key
openssl rsa -in Labex.key -pubout > Lab_public.key
openssl req -new -key Labex.key -out Labex.csr  
openssl x509 -req -days 365 -in Labex.csr -CA ../CA/CA.crt -CAkey ../CA/CA.key -out Labex.crt
```
Go back to folder **CA** again:

Copy the get_keys.py file and run it simulating the CA
```
python3 get_keys.py 
```
open another terminal.


**VM3: Front-Office app**

Open a terminal and put:

cd front-office/backend/setup/
```
openssl genrsa -out FrontBack.key
openssl rsa -in FrontBack.key -pubout > FrontBack_public.key
openssl req -new -key FrontBack.key -out FrontBack.csr  
python3 receive_signatures.py FrontBack.csr (assumes mkcert is already installed)
mkcert -cert-file cert.pem -key-file key.pem 192.168.1.3 frontoffice  192.168.1.3 ::1
python3 manage.py runsslserver 192.168.1.3:8002 --certificate cert.pem --key key.pem
```

Open a **new** terminal and put:

cd front-office/frontend/setup/
```
openssl genrsa -out FrontFront.key
openssl rsa -in FrontFront.key -pubout > FrontFront_public.key
openssl req -new -key FrontFront.key -out FrontFront.csr  
python3 receive_signatures.py FrontFront.csr (assumes mkcert is already installed)
mkcert -cert-file cert.pem -key-file key.pem 192.168.1.3 frontoffice  192.168.1.3  ::1
python3 manage.py runsslserver 192.168.1.3:8000 --certificate cert.pem --key key.pem
```

**VM4: Back-Office app**

Open a terminal and put:

cd backoffice/frontend-HOSPITAL/setup
```
openssl genrsa -out BackOffice.key
openssl rsa -in BackOffice.key -pubout > BackOffice_public.key
openssl req -new -key BackOffice.key -out BackOffice.csr  
python3 receive_signatures.py BackOffice.csr
mkcert -cert-file cert.pem -key-file key.pem 192.168.1.4 frontoffice  192.168.1.4 ::1
python3 manage.py runsslserver 192.168.1.4:8001 --certificate cert.pem --key key.pem
```

Open a **new** terminal and put:

cd backoffice/backend-HOSPITAL/setup
```
mkdir keys
openssl genrsa -out server.key
openssl rsa -in server.key -pubout > server_public.key
openssl req -new -key server.key -out server.csr 
python3 receive_signatures.py server.csr
cd .. (setup directory)
mkcert -cert-file cert.pem -key-file key.pem 192.168.1.4 frontoffice  192.168.1.4 ::1
python3 manage.py runsslserver 192.168.1.4:8003 --certificate cert.pem --key key.pem
```


### Testing

Explain how to run the automated tests for this system.

Give users explicit instructions on how to run all necessary tests. 
Explain the libraries, such as JUnit, used for testing your software and supply all necessary commands.

Explain what these tests test and why

```
Give an example command
```

## Demo

Give a tour of the best features of the application.
Add screenshots when relevant.


## Additional Information

### Authors

* **Alexandre Serras** - [alexandreserras](https://github.com/alexandreserras)
* **Alexandre Rodrigues** - [alex-pt01](https://github.com/alex-pt01)
* **Ricardo Antunes** - [tunes2000]()

### Versioning

Our version is 1.0.0

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

### Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

### Acknowledgments

We would like to thank all the teachers who helped us in the development of this project, namely:
* **André Mendes** - andre.i.mendes@tecnico.ulisboa.pt
* **Miguel de Oliveira Guerreiro** - oliveira.guerreiro@tecnico.ulisboa.pt
* **Ricardo Chavess** - ricardo.chaves@tecnico.ulisboa.pt












# **5. Healthcare: SAH**

## **Website**
```
ADMIN
username: adminsirs
password: @adsirs123

DOCTOR
username: doctorAlex
password: @sirs1234

PACIENT
username: peter 
password: @sirs1234
```


**Requirements**
```
virtualenv django
source django/bin/activate
python3 -m pip install django
python3 -m pip install django-allauth
pip3 install django-sslserver
pip3 install django-debug-toolbar
pip3 install django-createsuperuser
pip3 install djangorestframework
pip3 install django-cors-headers
pip3 install serializers
pip3 install djangorestframework-simplejwt
pip3 install ratelimit
pip3 install pyOpenSSL
pip install rsa


```

**START working**
```
source ~/.bash_profile
conda activate django

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
npx kill-port 8000
```




**HELP**
```
1. Remove all the migration files
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

2. Delete db.sqlite3
rm db.sqlite3

3. Create and run the migrations:
python manage.py makemigrations
python manage.py migrate

4. Sync the database:
manage.py migrate --run-syncdb
```




