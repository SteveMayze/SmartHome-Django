from django.shortcuts import render
from i2c.models import Device

# Create your views here.


def index( request, new_found=-1 ):

        devices_list = Device.objects.order_by('address')
        context_dict = {'pagetitle': 'Our House','pagename': 'I2C Devices',
                        'titlebar': 'I<sup>2</sup>C Devices',
                        "devices": devices_list}
        if new_found >= 0:
                context_dict["new_found"] = new_found

        return render(request, 'lighting/index.htm', context=context_dict)



def about( request ):
        if request.session.test_cookie_worked():
                print("THE TEST COOKIE WORKED")
                request.session.delete_test_cookie()
        context_dict = {'pagetitle': 'Our House',
                        'pagename' : 'Our Hourse - About'}
        return render(request, 'about.htm', context=context_dict)


