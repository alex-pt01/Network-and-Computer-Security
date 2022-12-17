# **5. Healthcare: SAH**

## **Website**
```
ADMIN
username: adminsirs
password: @adsirs123

DOCTOR
username: doctor3
password: @sirs1234

PACIENT
username: pacient 
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




