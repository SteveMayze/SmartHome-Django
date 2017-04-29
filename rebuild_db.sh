
# rm db.sqlite3 energy/migrations/0001_initial.py i2c/migrations/0001_initial.py main/migrations/0001_initial.py 


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

