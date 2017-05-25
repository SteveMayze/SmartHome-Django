

import os
import time
import logging
import json


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ourhouse_site.settings')
import django
django.setup()

import RPi.GPIO as GPIO
from i2c.i2c_lib import i2c_get_status
from i2c.i2c_lib import i2c_get_config
from lighting.models import LightHistory, LightHistoryBinding
from django.utils import timezone
from django.core import serializers

from channels.asgi import get_channel_layer
#import ourhouse_site.asgi.channel_layer

channel_layer = get_channel_layer()


PIR_EVENT = 7 # G04
last_status = 0

def pir_handler(pin):
	global last_status
	status = i2c_get_status( 32 )
	config = i2c_get_config( 32 )
	if status != last_status:
                # logging.info("Creating ...")
                history = LightHistory.objects.create(timestamp=timezone.now(),
                                                      status = status, config = config)
                # LightHistoryBinding.create(history)
                history.save()
                logging.info(str(history))
                channel_layer.send("tl2c_state", {"LightHistory": serializers.serialize("json", [history, ])})
                # consumer_finished.send(sender=None)
                # Channel("tl2c_state").send({"LightHistory": serializers.serialize("json", [history, ]})
                logging.info("TIMESTAMP {0}: CH STATUS={1:08b} CONFIG={2:08b}".format(history.timestamp, history.status, history.config))
                last_status = status


def main():
        FORMAT='%(asctime)s  %(message)s'
        logging.basicConfig(filename="/tmp/tl2c_pir.log", format=FORMAT, level=logging.INFO)
        logger = logging.getLogger(__name__)
        global last_status
        logging.info("Starting the TL2C PIR event checking")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIR_EVENT, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.add_event_detect(PIR_EVENT, GPIO.RISING, pir_handler)
        status = i2c_get_status( 32 )
        last_status = 0
        try:
                # Channel("tl2c_state").send({})
                while True:
                        time.sleep(1e6)
        except KeyboardInterrupt:
                logging.info("TL2C Ending")



if __name__ == "__main__":
	main()

