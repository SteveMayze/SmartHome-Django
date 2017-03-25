import os
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ourhouse_site.settings')

import django

django.setup()
from energy.models import  ResourceEntry
from energy.models import Resource
from energy.models import ResourceValueFactor
from datetime import datetime

def populate():

    # Load the resources i.e. the Parent definitions
    resource_data = [{"name": "Water"},
                     {"name": "Electricity"},
                     {"name": "Gas"},
                     ]

    for resource in resource_data:
        print(" RESOURCE =" + str(resource))
        add_resource(resource["name"])

    # Now load the resource entries, each for Water, Electricity and Gas
    
    elec = pd.read_csv('/home/pi/web/django/ourhouse_site/energy_data/elec.csv')
    res = Resource.objects.get(name="Electricity")
    populate_resource_entry( res, elec)

    gas = pd.read_csv('/home/pi/web/django/ourhouse_site/energy_data/gas.csv')
    res = Resource.objects.get(name="Gas")
    populate_resource_entry( res, gas)
    water = pd.read_csv('/home/pi/web/django/ourhouse_site/energy_data/water.csv')
    res = Resource.objects.get(name="Water")
    populate_resource_entry( res, water)

    # Lastly, the gas factor table.
    ##    
    gFactor = pd.read_csv('/home/pi/web/django/ourhouse_site/energy_data/gf.csv')

    ## gas_factors = pd.read_csv('d:\Dropbox\EA\HomeAutomation\web\django\ourhouse_site\energy_data\gf.csv')
    res = Resource.objects.get(name="Gas")
    populate_gas_factor( res, gFactor )

    for e in ResourceEntry.objects.all():
        print("- {0}".format(str(e)))


def populate_gas_factor( res, df ):
    for index, row in df.iterrows():
        f_year = row['Start_Year']
        f_billing_factor = row['Billing_Factor']
        f_status_number = row['Status_Number']
        f_gas_factor = row['Gas_Factor']
        
        
        gf = add_factor(res, f_year-1, f_year, f_billing_factor, f_status_number, f_gas_factor)
        print(str(gf))

        
def add_factor( res, start_year, end_year, billing, status, factor):
    resource_factor = ResourceValueFactor.objects.get_or_create(resource=res, 
                                                      billing_factor=billing, status_value=status,
                                                      factor=factor)[0]
    resource_factor.start_year = start_year
    resource_factor.end_year = end_year
    resource_factor.save()
    return resource_factor
        

def populate_resource_entry( resource, df ):
    for index, row in df.iterrows():
        print("Creating " + resource.name + "for " + str(row['time_stamp']))
        r_date = row['time_stamp']
        r_open = float(str(row['open']).strip(' "').replace(",", ""))
        r_close = float(str(row['close']).strip(' "').replace(",", ""))
        r_adj = float(str(row['adjust']).strip(' "').replace(",", ""))
        r_comment = str(row['comment']).strip(' "')
        r_usage = (r_close + r_adj) - r_open

        r = add_resource_entry(resource, r_date, r_open, r_close,
                               r_adj, r_usage, r_comment)
        print("Created " + str(r))


def add_resource( name ):
    res = Resource.objects.get_or_create(name=name)[0]
    res.save
    return res;
    
def add_resource_entry( resource, r_date, r_open, r_close, r_adj, r_usage, r_comment ):
    print( "{0} {1} {2} {3} {4} {5}".format(str(resource), str(r_date), str(r_open), str(r_close), str(r_adj), str(r_usage)))
    resource_entry = ResourceEntry.objects.get_or_create( resource=resource, time_stamp=r_date,
                                                          value_open=r_open, value_close=r_close,
                                                          value_adjust=r_adj, value_usage=r_usage)[0]
    resource_entry.comment = r_comment

    resource_entry.save()
    return resource_entry

if __name__ == '__main__':
    print("Starting energy population script...")
    populate()

    
                  
            
