#!/bin/bash
# this script is used to install and run the server
ip_address=$(hostname -I | awk '{print $1}')
python3 -m venv venv &&
source venv/bin/activate &&
pip install -r requirements.txt &&
cd src &&
python manage.py migrate &&
python manage.py create_groups &&
if [ ! -f db.sqlite3 ]; then
    python manage.py createsuperuser
fi &&
echo &&
echo "The server is running at http://$ip_address:8000" &&
echo &&
python manage.py runserver_plus --cert cert 0.0.0.0:8000  --insecure