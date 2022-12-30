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

Our hospital provides urgent care, open 24/7 (24 hours, 7 days a week) as well as speciality consultations, including: orthopedy, cardiology, and dermatology. ##MAIS????

### Built With

In order to create the applications we used the django framework with the SQLite database since it allows rapid development of secure and maintainable websites. In order to develop the CA (Certificate Authority) we used OpenSSL that is free, open-source library used for digital certificates and the libraries used for cryptography were: ##TODO 

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

To setup our project environment to be used with [VirtualBox](https://www.virtualbox.org/), you need to have 6 instances of VMs.

#TODO -> VERIFICAR!
**VM1: Ministry of Health**
```
Network adapter 1 : Internal network , name : sw-1 (Promiscuous MODE : Allow VMS)
IP: 192.168.0.100 
Gateway:192.168.0.10
```

**VM2: ROUTER/FIREWALL**
```
Network adapter 1: Internal Network , name : sw-1 (GENERATE NEW MAC ADDRESSES) (Promiscuous MODE : Allow VMS)
IP:192.168.0.10
Network adapter 2: Internal Network , name sw-2 (Promiscuous MODE : Allow VMS)
IP:192.168.1.254
Adapter 3: associated with NAT.
```

**VM3: Front Office APP**
```
Network adapter 1: Internal network, name sw-2 (Promiscuous MODE: Allow VMS)
IP:192.168.1.3
Gateway:192.168.1.254
```

**VM4: Back Office APP**
```
Network adapter 1: Internal network, name sw-2 (Promiscuous MODE : Allow VMS)
IP:192.168.1.4
Gateway:192.168.1.254
```

**VM5: Front Office DB**
```
Network adapter 1: Internal Network, name sw-2 (PROMISE MODE: Allow VMS)
IP:192.168.1.5
Gateway:192.168.1.254
```

**VM6: Back Office DB **
```
Network adapter 1: Internal Network, name sw-2 (Promiscuous MODE : Allow VMS)
IP:192.168.1.6
Gateway:192.168.1.254
```


### Installing

Give step-by-step instructions on building and running the application on the development environment. 

Describe the step.

```
Give the command example
```

And repeat.

```
until finished
```

You can also add screenshots to show expected results, when relevant.

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

## Deployment

Add additional notes about how to deploy this on a live system e.g. a host or a cloud provider.

Mention virtualization/container tools and commands.

```
Give an example command
```

Provide instructions for connecting to servers and tell clients how to obtain necessary permissions.

## Additional Information

### Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

### Versioning

We use [SemVer](http://semver.org/) for versioning. 
For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

### Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

### Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc


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

**BD Django -> mysql workbench**
```
sudo snap install mysql-workbench-community
sudo apt-get install gnome-keyring
sudo snap connect mysql-workbench-community:password-manager-service :password-manager-service
sudo mysql

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_new_password';

pip install wheel
pip install pymysql

Dentro do django:
no file init na pasta settings meter

import pymysql
pymysql.install_as_MySQLdb(
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




