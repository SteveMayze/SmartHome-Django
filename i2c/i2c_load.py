
import os
import django
django.setup
from i2c.models import Device


def i2c_refresh():
	found_count = 0
	i2cLines = os.popen('i2cdetect -y 1').readlines()

	i2cSet = set( i2cLines )
	
	for line in i2cSet:
		if ':' in line:
			elements = line.split(' ')
			elementSet = set( elements )
			for element in elementSet:
				element = element.lstrip().rstrip()
				if ( not (':' in element)):
					if ( element != '--' and element != '' ):
                                                address = int( "0x" + str(element), 0)
						found_count = add_device(address, "Undefined", "Not allocated", found_count)
	print("FOUND_COUNT="+str(found_count))
	return found_count


def add_device( address, name, desc, found_count):
	device = Device.objects.get_or_create( address=address)[0]
	print(str(device.address) + " " + device.name)
	if device.name == "" :
		print("ADDING address=" + str(address) + ", Name=" + name + ", Desc=" + desc)
		device.name = name
		device.description = desc
		device.save()
		found_count = found_count +1
	return found_count


