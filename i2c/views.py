from django.shortcuts import render
from django.http import HttpResponse
from i2c.models import Device
from i2c.forms import DeviceForm
from django.contrib.auth.decorators import login_required
## from i2c.i2c_devices import i2c_refresh
from i2c.i2c_load import i2c_refresh

def index( request, new_found=-1 ):

        devices_list = Device.objects.order_by('address')
        context_dict = {'pagetitle': 'Our House','pagename': 'I2C Devices',
                        'titlebar': 'I<sup>2</sup>C Devices',
                        "devices": devices_list}
        if new_found >= 0:
                context_dict["new_found"] = new_found

        return render(request, 'i2c/index.htm', context=context_dict)

@login_required
def edit_device( request, device_address_slug ):
        try:
                device = Device.objects.get(slug=device_address_slug)

                print("DEVICE=" + str(device))
                context_dict = {'device': device}
                
                form = DeviceForm(auto_id=False, initial={'address': device.address, 'name': device.name, 'description': device.description, 'slug': device_address_slug})
                if request.method == 'POST':
                        form = DeviceForm( request.POST, instance=device, auto_id=False)
                        if form.is_valid():
                                device = form.save(commit=False)
                                device.slug = device_address_slug
                                print("SAVING DEVICE=" + str(device))
                                device.save()
                                return index( request )
                        else:
                                print(form.errors)
               
        except Device.DoesNotExist:
                device = None
        context_dict = {'pagetitle': 'Our House','pagename': 'I2C Devices',
                        'titlebar': 'I<sup>2</sup>C Devices',
                        'device_form': form}
        return render(request, 'i2c/edit_device.htm', context_dict)



@login_required
def refresh( request ):
        # TODO - call the system script to run refresh the database
        new_found = i2c_refresh()
        return index ( request, new_found )

def about( request ):
        if request.session.test_cookie_worked():
                print("THE TEST COOKIE WORKED")
                request.session.delete_test_cookie()
        context_dict = {'pagetitle': 'Our House',
                        'pagename' : 'Our Hourse - About'}
        return render(request, 'about.htm', context=context_dict)


