# Healthcare: SAH


Saint Acutis hospital has operated in Portugal since 2020. It provides Urgent Care, open 24/7 (24 hours, 7 days a week). It also provides Specialty Consultations, including: Orthopedic, Cardiology, and Dermatology.
The front-office of the hospital offers both a public web site, for displaying general information, and a customer web site, where patients can check their appointments and make new ones. There is also a mobile application that provides the same functionality.
The back-office is used to manage the schedule, the room reservations, and the medical records. The system has integrations with external institutions, namely, the Ministry for Health, and several exam facilities and laboratories.


## General Information

This section expands on the introductory paragraph to give readers a better understanding of your project. 
Include a brief description and answer the question, "what problem does this project solve?"

### Built With

Include an outline of the technologies in the project, such as framework (Rails/iOS/Android), as well as programming language, database,  links to any related projects (for example, whether this API has corresponding iOS or Android clients), links to online tools related to the application (such as the project web site, the shared file storage).
If you mention something, please provide links.

* [Java](https://openjdk.java.net/) - Programming Language and Platform
* [Maven](https://maven.apache.org/) - Build Tool and Dependency Management
* ...

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What kind of **hardware** device and which **operating system** do you need to have to install the software.

In this section also include detailed instructions for installing additiona software the application is dependent upon (such as PostgreSQL database, for example). 

```
Give installation command examples
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




