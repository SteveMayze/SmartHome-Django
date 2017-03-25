from django.conf.urls import url
from energy import views

app_name = 'energy'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^usage-graph/summary.png$', views.summary, name="energy-summary"),

]
