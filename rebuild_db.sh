#!/bin/bash

sudo systemctl stop tl2c.service

# rm db.sqlite3 
# rm energy/migrations/[0-9]{4}_\w.py 
# rm i2c/migrations/[0-9]{4}_\w.py 
# rm main/migrations/[0-9]{4}_\w.py 
# rm lighting/migrations/[0-9]{4}_\w.py 


python manage.py migrate

python manage.py createsuperuser
python manage.py makemigrations main
python manage.py makemigrations i2c
python manage.py makemigrations energy
python manage.py makemigrations lighting
python manage.py migrate

python populate_i2c.py
python populate_energy.py 
python populate_lighting.py

sudo systemctl start tl2c.service
