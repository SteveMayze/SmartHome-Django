

import os
import time
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ourhouse_site.settings')
import django
django.setup()

import RPi.GPIO as GPIO
from i2c.i2c_lib import i2c_get_status
from i2c.i2c_lib import i2c_get_config


PIR_EVENT = 7 # G04

def pir_handler(pin):
	status = i2c_get_status( 32 )
	config = i2c_get_config( 32 )
	print("{0}: PIN {1}. STATUS={2:08b} CONFIG={3:08b}".format(datetime.datetime.now(), pin, status, config))
	time.sleep(1)
	registers = i2c_get_status( 32 )
	
	



def main():
	print("Starting the PIR event checking")
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(PIR_EVENT, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	GPIO.add_event_detect(PIR_EVENT, GPIO.RISING, pir_handler)
	print("Sleeping")	
	status = i2c_get_status( 32 )
	while True:
		time.sleep(1e6)


if __name__ == "__main__":
	main()
