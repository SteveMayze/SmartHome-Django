import os
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ourhouse_site.settings')

import django

django.setup()
from energy.models import  ResourceEntry
from datetime import datetime

def populate():


    elec = pd.read_csv('/Users/steve/Dropbox/EA/HomeAutomation/web/django/ourhouse_site/energy_data/Electricity Readings-Electricity Readings.csv', index_col=0)
    gas = pd.read_csv('/Users/steve/Dropbox/EA/HomeAutomation/web/django/ourhouse_site/energy_data/Gas Readings-Gas Readings.csv', index_col=0)
    water = pd.read_csv('/Users/steve/Dropbox/EA/HomeAutomation/web/django/ourhouse_site/energy_data/Water Readings-Water Readings.csv', index_col=0)
    gFactor = pd.read_csv('/Users/steve/Dropbox/EA/HomeAutomation/web/django/ourhouse_site/energy_data/Resource Usage-Gas Conversion Factors.csv', index_col=0)


    resourceEntries = [
        { "time_stamp": datetime(2015,01,01), "water_usage": 345.3434, "elec_usage": 4543.45, "gas_usage": 234.4532, "lighting_usage": 1.23, "lighting_rec_time": 2592000, "lighting_on_time": 1728000, "comment": None } ,
        { "time_stamp": datetime(2015,02,01), "water_usage": 545.3434, "elec_usage": 5543.45, "gas_usage": 534.4532, "lighting_usage": 1.23, "lighting_rec_time": 2592000, "lighting_on_time": 1728000, "comment": None } ,
        { "time_stamp": datetime(2015,03,01), "water_usage": 745.3434, "elec_usage": 6543.45, "gas_usage": 834.4532, "lighting_usage": 1.23, "lighting_rec_time": 2592000, "lighting_on_time": 1728000, "comment": None } ,
        { "time_stamp": datetime(2015,04,01), "water_usage": 945.3434, "elec_usage": 7543.45, "gas_usage": 934.4532, "lighting_usage": 1.23, "lighting_rec_time": 2592000, "lighting_on_time": 1728000, "comment": "Heating turned off" } ,
        { "time_stamp": datetime(2015,05,01), "water_usage":1145.3434, "elec_usage": 8543.45, "gas_usage":1034.4532, "lighting_usage": 1.23, "lighting_rec_time": 2592000, "lighting_on_time": 1728000, "comment": None } ,
        { "time_stamp": datetime(2015,06,01), "water_usage":1235.3434, "elec_usage": 9543.45, "gas_usage":1134.4532, "lighting_usage": 0.05, "lighting_rec_time": 2592000, "lighting_on_time": 1728000, "comment": None } ,
        { "time_stamp": datetime(2015,07,01), "water_usage":1345.3434, "elec_usage":10543.45, "gas_usage":1234.4532, "lighting_usage": 0.05, "lighting_rec_time": 2592000, "lighting_on_time": 1728000, "comment": "Holiday in the carribic" } ,
        { "time_stamp": datetime(2015,08,01), "water_usage":1545.3434, "elec_usage":11543.45, "gas_usage":1434.4532, "lighting_usage": 0.05, "lighting_rec_time": 2592000, "lighting_on_time": 1728000, "comment": None } ,
        { "time_stamp": datetime(2015,09,01), "water_usage":1745.3434, "elec_usage":12543.45, "gas_usage":1634.4532, "lighting_usage": 1.23, "lighting_rec_time": 2592000, "lighting_on_time": 1728000, "comment": "Heating turned on" } ,
        { "time_stamp": datetime(2015,10,01), "water_usage":1845.3434, "elec_usage":13543.45, "gas_usage":1834.4532, "lighting_usage": 1.23, "lighting_rec_time": 2592000, "lighting_on_time": 1728000, "comment": None } ,
        { "time_stamp": datetime(2015,11,01), "water_usage":2045.3434, "elec_usage":14543.45, "gas_usage":2134.4532, "lighting_usage": 1.23, "lighting_rec_time": 2592000, "lighting_on_time": 1728000, "comment": None } ,
        { "time_stamp": datetime(2015,12,01), "water_usage":2245.3434, "elec_usage":15543.45, "gas_usage":2434.4532, "lighting_usage": 1.23, "lighting_rec_time": 2592000, "lighting_on_time": 1728000, "comment": None } ,
        ]

    for resource_entry in resourceEntries:
        print("   RESOURCE ENTRY =" + str(device))            
        add_resource_entry(resource_entry["time_stamp"], resource_entry["water_usage"], resource_entry["elec_usage"], resource_entry["gas_usage"],
                           resource_entry["lighting_usage"], resource_entry["lighting_rec_time"], resource_entry["lighting_on_time"], resource_entry["comment"] )

    for e in ResourceEntry.objects.all():
        print("- {0}".format(str(e)))


def add_resource_entry( time_stamp, water_usage, elec_usage, gas_usage, lighting_usage, lighting_on_time, lighting_rec_time, comment ):
    resource_entry = ResourceEntry.objects.get_or_create( time_stamp=time_stamp )[0]
    resource_entry.water_usage = water_usage
    resource_entry.elec_usage = elec_usage
    resource_entry.gas_usage = gas_usage

    resource_entry.lighting_usage = lighting_usage
    resource_entry.lighting_on_time = lighting_on_time
    resource_entry.lighting_rec_time = lighting_rec_time

    comment 
    resource_entry.save()
    return resource_entry

if __name__ == '__main__':
    print("Starting energy population script...")
    populate()

    
                  
            
