from django.conf.urls import url
from . import views,response_error_views

urlpatterns = [
 url(r'^register/$', views.UserRegister.as_view()),
 url(r'^login/$', views.login,name='login'),
 url(r'^index/$', views.index, name='index'),
 url(r'^not_authenticated/$', response_error_views.not_authenticated, name='not_authenticated')
]
