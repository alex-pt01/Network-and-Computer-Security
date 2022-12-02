# SIRS


python3 -m venv django_env
source django_env/bin/activate
python -m pip install django
python -m pip install django-allauth
pip3 install django-debug-toolbar
pip install django-createsuperuser
python manage.py createsuperuser
pip3 install django-multi-form-view

---------

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py rumserver

-----
ADMIN
username: sirs
password: as@123

USER
username: usertest
password: @luso123

---
Kill port
npx kill-port 8000