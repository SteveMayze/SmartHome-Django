from django.shortcuts import render
from django.http import HttpResponse
from lighting.forms import ZoneForm
from django.contrib.auth.decorators import login_required

from lighting.models import Zone
from i2c.models import Device

from i2c.i2c_lib import i2c_lighting_sync
from i2c.i2c_lib import i2c_lighting_save_registers



def set_bit(data, index, value):
	print("BEFORE {0:b}, index={1}, value={2}".format(data, index, value))
	mask = 1 << index
	data &= ~mask
	if value:
		data |= mask
	print("AFTER {0:b}, index={1}, value={2}".format(data, index, value))
	return data

# Create your views here.


def index( request ):

        zone_list = Zone.objects.order_by('name')
        context_dict = {'pagetitle': 'Our House','pagename': 'Lighting', 'titlebar': 'Lighting zones', "zones": zone_list}
        return render(request, 'lighting/index.htm', context=context_dict)



@login_required
def edit_zone( request, zone_slug ):
	print("ZONE-SLUG="+zone_slug)
	try:
		zone = Zone.objects.get(slug=zone_slug)
		context_dict = {'zone': zone}

		form = ZoneForm(auto_id=False, initial={'name': zone.name, 'pir_enabled': zone.pir_enabled, 'test_active': zone.test_active, 'on_delay': zone.on_delay, 'slug': zone_slug})
		if request.method == 'POST':
			form = ZoneForm(request.POST, instance=zone, auto_id=False)
			if form.is_valid():
				zone = form.save(commit=False)
				zone.slug = zone_slug
				zone.save()
				registers = i2c_lighting_sync( zone.device.address )
				config = registers["config"]

				nameMap = { "UG":1, "EG":2, "OG":4}
				shiftMap = { "UG":0, "EG":1, "OG":2}

				config = set_bit(config, 4 + shiftMap[zone.name], zone.pir_enabled)
				config = set_bit(config, shiftMap[zone.name], zone.test_active)

				registers["config"] = config
				registers[zone.name+"_on_delay"] = zone.on_delay

				print("SAVING REGISTERS {0}".format(str(registers)))
 
				i2c_lighting_save_registers( zone.device.address, registers )
				return index(request)
			else:
				print(form.errors)
	except Zone.DoesNotExist:
		zone = None
	context_dict = {'pagetitle': 'Our House', 
			'pagename': 'Lighting', 
			'titlebar': 'Lighting', 'zone_form': form}
	return render (request, 'lighting/edit_zone.htm', context_dict)

@login_required
def sync( request, address ):
	registers = i2c_lighting_sync( address )
	print("Lighting: ADDRESS={0} ({0:2x}) REGISTERS={1}".format(int(address), str(registers)))
	pir_config = (0xF0 & registers["config"]) >> 4
	zone_config = 0x0F & registers["config"]
	status = registers["status"]
	config = {}
	config["pir_ug_enabled"] = 0x01 & pir_config
	config["pir_eg_enabled"] = (0x02 & pir_config) >> 1
	config["pir_og_enabled"] = (0x04 & pir_config) >> 2

	config["ug_test_active"] = 0x01 & zone_config
	config["eg_test_active"] = (0x02 & zone_config)>> 1
	config["og_test_active"] = (0x04 & zone_config) >> 2

	print("CONFIG={0}".format(str(config)))

	device = Device.objects.get(address = address)

	updateZone( device=device, name="UG", pir_enabled=config["pir_ug_enabled"], test_active=config["ug_test_active"], on_delay=registers["UG_on_delay"])
	updateZone( device=device, name="EG", pir_enabled=config["pir_eg_enabled"], test_active=config["eg_test_active"], on_delay=registers["EG_on_delay"])
	updateZone( device=device, name="OG", pir_enabled=config["pir_og_enabled"], test_active=config["og_test_active"], on_delay=registers["OG_on_delay"])

	return index( request )


def updateZone(device, name, pir_enabled, test_active, on_delay):
	print("Saving device={0}, name={1}, pir_enabled={2}, test_active={3}, on_delay={4}".format(str(device), name, pir_enabled, test_active, on_delay))
	zone = Zone.objects.get(device=device, name=name)
	zone.pir_enabled=pir_enabled
	zone.test_active=test_active
	zone.on_delay=on_delay
	zone.save()


def about( request ):
        if request.session.test_cookie_worked():
                print("THE TEST COOKIE WORKED")
                request.session.delete_test_cookie()
        context_dict = {'pagetitle': 'Our House',
                        'pagename' : 'Our Hourse - About'}
        return render(request, 'about.htm', context=context_dict)


