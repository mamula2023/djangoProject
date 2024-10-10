# Django Project

Django project for practice

## Prerequisites 
ensure you have installed 
- Python 3.x
- Django 4.x

## Installation
1. `git clone https://github.com/mamula2023/djangoProject.git`
2. `cd djangoProject`
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py runserver`

Application works on port 8000. Open website on http://127.0.0.1:8000/

## Usage
To use application for own use, you should create superuser and you will have access to admin panel. there you would be able to 
create/delete/modify data in database.
- Note: there is already test data in database that you can remove manually from admin panel

### To login as admin
1. Create superuser.
`python manage.py createsuperuser`
and follow instructions in command prompt
2. Log in to admin panel.
Once superuser is created, browse http://127.0.0.1:8000/admin/ and enter credentials
3. Use GUI to modify data

