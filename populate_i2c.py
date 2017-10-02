import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ourhouse_site.settings')

import django

django.setup()
from i2c.models import  Device

def populate():

    devices = [ 
        { "address": 0, "name":"Undefined", "description":"Not allocated"} ,
        { "address": 32, "name":"Lighting", "description":"Stairwell lighting"},
        { "address": 150, "name":"Temp: Out", "description": "Outside Temperature"},
        { "address": 160, "name":"MP3 Sound", "description":"Raspi-Alarm unit"}
        ]

    for device in devices:
        print("   DEVICE=" + str(device))            
        add_device(device["address"], device["name"], device["description"] )

    for d in Device.objects.all():
        print("- {0}".format(str(d)))


def add_device( address, name, desc):
    device = Device.objects.get_or_create( address=address )[0]
    device.name = name
    device.description = desc
    device.save()
    return device

if __name__ == '__main__':
    print("Starting i2c population script...")
    populate()

    
                  
            
