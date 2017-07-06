from django.conf.urls import url
from .views import (UserMessagesListAPIView,MessagesListAPIView,BroadcastMessageSendAPIView,
	UserMessagesDestroyAPIView)

urlpatterns = [
   
	url(r'^messages/$', UserMessagesListAPIView.as_view(),name='list'),
	url(r'^messages/delete$', UserMessagesDestroyAPIView.as_view(),name='delete'),
	url(r'^messages/all$', MessagesListAPIView.as_view(),name='list-all'),
	url(r'^messages/broadcast$', BroadcastMessageSendAPIView.as_view(),name='broadcast'),
]