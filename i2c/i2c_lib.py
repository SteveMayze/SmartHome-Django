
import os
import django
import re
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


def i2c_lighting_sync( address ):
	hexAddr = hex( int(address) ).split('x')[-1]
	print("Synchronising the DB with the actual device at {0} ({0:2x}) state.".format(int(address)))
	i2cLines = os.popen('i2cdump -y -r 0x00-0x08 1 0x20').readlines()
	elems = re.split(r' ', i2cLines[1])
	registers = {}
	registers["status"] = int( "0x" + str(elems[1]), 0);
	registers["config"] = int( "0x" + str(elems[2]), 0);
	registers["UG_on_delay"] = int( "0x" + str(elems[3]), 0);
	registers["EG_on_delay"] = int( "0x" + str(elems[4]), 0);
	registers["OG_on_delay"] = int( "0x" + str(elems[5]), 0);
	registers["firmware"] = int( "0x" + str(elems[6]), 0);
	print("ADDRESS={0} ({0:2x}) REGISTERS={1}".format(int(address), str(registers)))
	# print("ADDRESS= " + address + " ( 0x" + hexAddr + ") REGISTERS=" + str(registers))
	return registers




