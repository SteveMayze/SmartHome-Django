import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ourhouse_site.settings')

import django

django.setup()

from i2c.models import Device
from lighting.models import Zone

def populate():
	zones = [
	{"name":"UG", "pir_enabled":True, "test_active":False, "on_delay":10}, 
	{"name":"EG", "pir_enabled":True, "test_active":False, "on_delay":10}, 
	{"name":"OG", "pir_enabled":True, "test_active":False, "on_delay":10}, 
	]

	device = Device.objects.get(address=32) 
	for zone in zones:
		print("    DEVICE={0}, ZONE={1}".format(str(device), zone["name"]))
		add_zone(device, zone["name"], zone["pir_enabled"], zone["test_active"], zone["on_delay"])

	for z in Zone.objects.all():
		print("- {0}".format(str(z)))



def add_zone( device, name, pir_enabled, test_active, on_delay ):
	print("Adding zone {0} to device {1} pir_enabled={2} ".format( name, str(name), pir_enabled))
	zone = Zone.objects.get_or_create(device=device, name=name)[0]
	zone.pir_enabled = pir_enabled
	zone.test_active=test_active
	zone.on_delay=on_delay
	zone.save()
	return zone



if __name__ == '__main__':
	print('Starting Zone population script...')
	populate()
