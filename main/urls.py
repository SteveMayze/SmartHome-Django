from django.conf.urls import url, include
from main import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^about$', views.about, name = 'about'),
  #  url(r'^login$', views.user_login, name = 'login'),
  #  url(r'^logout$', views.user_logout, name = 'logout'),
  #  url(r'^register$', views.register, name = 'register')
    ]
