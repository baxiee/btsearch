#!/bin/sh
sleep 5
python /var/code/manage.py migrate
python /var/code/manage.py runserver 0.0.0.0:8000
