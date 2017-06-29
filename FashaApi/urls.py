from django.conf.urls import url
from . import views

urlpatterns = [
 url(r'^register/$', views.UserRegister.as_view()),
 url(r'^login/$', views.login,name='login'),
 url(r'^index/$', views.index, name='index'),
]
