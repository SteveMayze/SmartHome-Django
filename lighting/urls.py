from django.conf.urls import url
from lighting import views

app_name = 'lighting'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    ## url(r'dashboard_refresh', views.dashboard_refresh, name='dashboard_refresh'),
    url(r'^edit_zone/(?P<zone_slug>[\w\-]+)/$', views.edit_zone, name='edit_zone'),
    url(r'^sync/(?P<address>[0-9]+)/$', views.sync, name='sync'),
]
