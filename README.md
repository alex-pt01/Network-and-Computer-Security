**SAH**

ADMIN
username: adminsirs
password: @adsirs123

DOCTOR
username: doctor3
password: @sirs1234

PACIENT
username: pacient 
password: @sirs1234

**START working**
source ~/.bash_profile
conda activate django

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
npx kill-port 8000



**Requirements**
conda create --name django
python3 -m pip install django
python3 -m pip install django-allauth
pip3 install django-debug-toolbar
pip3 install django-createsuperuser


**HELP**
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




