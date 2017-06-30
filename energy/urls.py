from django.conf.urls import url
from energy import views

app_name = 'energy'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^usage-graph/summary.png$', views.summary, name="energy-summary"),
    url(r'^usage-graph/resource.png$', views.graph_for_resource, name="energy-resource"),
    url(r'^resource-graph$', views.resource_graph, name="resource_graph_form"),
    url(r'^resource-entry$', views.resource_usage_entry, name="resource_usage_entry"),

]
