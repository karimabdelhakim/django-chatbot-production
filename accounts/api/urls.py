from django.conf.urls import url
from rest_framework_jwt.views import refresh_jwt_token
from .views import (UserCreateAPIView,UserLoginAPIView)
urlpatterns = [
   
	url(r'^register/$', UserCreateAPIView.as_view(), name='register'),   
	url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
	url(r'^refresh/', refresh_jwt_token),
	]