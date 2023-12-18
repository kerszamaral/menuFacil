#!/bin/bash
# this script is used to install and run the server
python3 -m venv venv &&
source venv/bin/activate &&
pip install -r requirements.txt &&
cd src &&
python manage.py migrate &&
python manage.py create_groups &&
python manage.py createsuperuser &&
python manage.py runserver 0.0.0.0:8000 --insecure