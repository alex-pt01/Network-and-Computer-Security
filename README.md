ADMIN
username: adminsirs

password: @adsirs123

DOCTOR
username:  doctor & doctor1 & doctor2

password: @sirs1234

PACIENT
username: pacient & pacient1 & pacient2

password: @sirs1234


source ~/.bash_profile

conda activate django

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py runserver

npx kill-port 8000




conda create --name django

python3 -m pip install django

python3 -m pip install django-allauth

pip3 install django-debug-toolbar

pip install django-createsuperuser

python3 manage.py createsuperuser

pip3 install django-multi-form-view

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




