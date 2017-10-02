from django.conf.urls import url
from lighting import views

app_name = 'lighting'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^edit_zone/(?P<zone_slug>[\w\-]+)/$', views.edit_zone, name='edit_zone'),
]
