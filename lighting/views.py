from django.shortcuts import render
from django.http import HttpResponse
from lighting.forms import ZoneForm
from django.contrib.auth.decorators import login_required

from lighting.models import Zone

# Create your views here.


def index( request, new_found=-1 ):

        zone_list = Zone.objects.order_by('name')
        context_dict = {'pagetitle': 'Our House','pagename': 'Lighting', 'titlebar': 'Lighting zones', "zones": zone_list}
        if new_found >= 0:
                context_dict["new_found"] = new_found

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
				return index(request)
			else:
				print(form.errors)
	except Zone.DoesNotExist:
		zone = None
	context_dict = {'pagetitle': 'Our House', 
			'pagename': 'Lighting', 
			'titlebar': 'Lighting', 'zone_form': form}
	return render (request, 'lighting/edit_zone.htm', context_dict)



def about( request ):
        if request.session.test_cookie_worked():
                print("THE TEST COOKIE WORKED")
                request.session.delete_test_cookie()
        context_dict = {'pagetitle': 'Our House',
                        'pagename' : 'Our Hourse - About'}
        return render(request, 'about.htm', context=context_dict)


