from django.conf.urls import url
from lighting import views

app_name = 'lighting'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
