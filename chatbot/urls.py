from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url,include
from django.contrib import admin
#from django.contrib.auth.views import login, logout
from chat.views import index,message_to_all
from chat.api.views import index_api

urlpatterns = [
    url(r'^$', index ,name='index'),#home page
	url(r'^broadcast/$', message_to_all, name='broadcast'),
    url(r'^accounts/', include("accounts.urls",namespace='users')),
    url(r'^admin/', admin.site.urls),

    url(r'^api/test/$', index_api, name='jwt-test'),#for testing chat using jwt
    url(r'^api/accounts/', include("accounts.api.urls",namespace='users-api')),
    url(r'^api/chat/', include("chat.api.urls",namespace='chat-api')),
]

#on production static files should be separet from other django files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    