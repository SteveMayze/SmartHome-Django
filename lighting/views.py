from django.shortcuts import render
from django.http import HttpResponse
from lighting.forms import ZoneForm
from django.contrib.auth.decorators import login_required

from lighting.models import Zone, LightingState
from i2c.models import Device

from i2c.i2c_lib import i2c_lighting_sync
from i2c.i2c_lib import i2c_lighting_save_registers
from i2c.i2c_lib import i2c_get_config



def set_bit(data, index, value):
	print("BEFORE {0:b}, index={1}, value={2}".format(data, index, value))
	mask = 1 << index
	data &= ~mask
	if value:
		data |= mask
	print("AFTER {0:b}, index={1}, value={2}".format(data, index, value))
	return data


def index( request ):

        context_dict = dashboard_refresh()

        zone_list = Zone.objects.order_by('name')
        # context_dict = {"pagetitle": "Our House", "pagename": "Lighting", "titlebar": "Lighting zones", "zones": zone_list}
        context_dict["pagetitle"] = "Our House"
        context_dict["pagename"] = "Lighting"
        context_dict["titlebar"] = "Lighting zones"
        context_dict["zones"] = zone_list
        
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

				device = Device.objects.get(name="Lighting")
				config = i2c_get_config( device.address )
				state = LightingState.objects.get_or_create(device=device)[0]
				state.config = config
				state.save()

				return index(request)
			else:
				print(form.errors)
	except Zone.DoesNotExist:
		zone = None
	context_dict = {'pagetitle': 'Our House', 
			'pagename': 'Lighting', 
			'titlebar': 'Lighting', 'zone_form': form}
	return render (request, 'lighting/edit_zone.htm', context_dict)


def updateZone(device, name, pir_enabled, test_active, on_delay):
	print("Saving device={0}, name={1}, pir_enabled={2}, test_active={3}, on_delay={4}".format(str(device), name, pir_enabled, test_active, on_delay))
	zone = Zone.objects.get(device=device, name=name)
	zone.pir_enabled=pir_enabled
	zone.test_active=test_active
	zone.on_delay=on_delay
	zone.save()



def dashboard( request , status_dict=None):
        if status_dict == None:
                print("Calling the dashboard refresh for the first time")
                return dashboard_refresh( request )
        print("STATUS_DICT=" + str(status_dict))
        response = render(request, 'main/dashboard.htm', context=status_dict)
        return response

def dashboard_refresh():
        
        device = Device.objects.get(name="Lighting")
        registers = i2c_lighting_sync( device.address )
        state = LightingState.objects.get_or_create(device=device)[0]
        state.status = registers["status"]
        state.config = registers["config"]
        state.save()
        
        history = LightingState.objects.get(device = device)
        status_int = history.status
        config_int = history.config
        print("status {0:08b}, config {1:08b}".format(status_int, config_int))
        status_dict = {"UG_State": "DISABLED", "EG_State": "DISABLED", "OG_State": "DISABLED" }
        
        if config_int & 0b00010000 >= 1:
                print("Setting UG to OFF")
                status_dict["UG_State"]="OFF"
        else:
                print("Setting UG to DISABLED")
                status_dict["UG_State"]="DISABLED"
        if config_int & 0b00100000 >= 1:
                print("Setting EG to OFF")
                status_dict["EG_State"]="OFF"
        else:
                print("Setting EG to DISABLED")
                status_dict["EG_State"]="DISABLED"
        if config_int & 0b01000000 >= 1:
                print("Setting OG to OFF")
                status_dict["OG_State"]="OFF"           
        else:
                print("Setting OG to DISABLED")
                status_dict["OG_State"]="DISABLED"
                
        if status_int & 0b00000001 >= 1:
                print("Setting UG to ON")
                status_dict["UG_State"] = "ON"
        if status_int & 0b00000010 >= 1:
                print("Setting EG to ON")
                status_dict["EG_State"] = "ON"
        if status_int & 0b00000100 >= 1:
                print("Setting OG to ON")
                status_dict["OG_State"] = "ON"

        print("status_refresh status_dict=" + str(status_dict))
                
        return status_dict


def about( request ):
        if request.session.test_cookie_worked():
                print("THE TEST COOKIE WORKED")
                request.session.delete_test_cookie()
        context_dict = {'pagetitle': 'Our House',
                        'pagename' : 'Our Hourse - About'}
        return render(request, 'about.htm', context=context_dict)


