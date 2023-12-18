#!/bin/bash
# this script is used to install and run the server
ip_address=$(hostname -I | awk '{print $1}')
python3 -m venv venv &&
source venv/bin/activate &&
pip install -r requirements.txt &&
cd src &&
python manage.py migrate &&
python manage.py create_groups &&
python manage.py createsuperuser &&
echo "The server is running at http://$ip_address:8000" &&
python manage.py runserver 0.0.0.0:8000 --insecure