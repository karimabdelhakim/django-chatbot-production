from django.conf.urls import url
from .views import (register_view,login_view,logout_view)
urlpatterns = [
   
	url(r'^register/$', register_view, name='register'),   
	url(r'^login/$', login_view, name='login'),
	url(r'^logout/$', logout_view, name='logout'),
	]