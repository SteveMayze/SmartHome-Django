from django.conf.urls import url
from i2c import views

app_name = 'i2c'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^edit_device/(?P<device_address_slug>[0-9]{1,3})/$', views.edit_device, name='edit_device'),
    url(r'^refresh$', views.refresh, name='refresh'),
    url(r'^api/1.0/lighting/(?P<device_address>[0-9]{1,3})/$', views.lighting_details, name='lighting_detailslighting')
]
