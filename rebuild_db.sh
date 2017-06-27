#!/bin/bash

# rm db.sqlite3 
# rm energy/migrations/[0-9]{4}_\w.py 
# rm i2c/migrations/[0-9]{4}_\w.py 
# rm main/migrations/[0-9]{4}_\w.py 
# rm lighting/migrations/[0-9]{4}_\w.py 


python3 manage.py migrate

python3 manage.py createsuperuser
python3 manage.py makemigrations main
python3 manage.py makemigrations i2c
python3 manage.py makemigrations energy
python3 manage.py makemigrations lighting
python3 manage.py migrate

python3 populate_i2c.py
python3 populate_energy.py 
python3 populate_lighting.py

