#!/bin/bash

cd /home/steve/repositories/django/ourhouse_project
. ourhouse_env/bin/activate

cd /home/steve/repositories/django/ourhouse_project/SmartHome-Django
python i2c_pir.py

