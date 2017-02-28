#from django.db.models import Q
from django.contrib.auth import get_user_model 

from rest_framework.response import Response 
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

#from rest_framework.filters import ( SearchFilter, OrderingFilter)
#from rest_framework.mixins import DestroyModelMixin,UpdateModelMixin
from rest_framework.generics import (ListAPIView, RetrieveAPIView,
	UpdateAPIView,DestroyAPIView,CreateAPIView,RetrieveUpdateAPIView)
#from rest_framework.permissions import (AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly)
#from rest_framework.renderers import JSONRenderer

#from posts.api.permissions import IsOwnerOrReadOnly
#from posts.api.pagination import PostLimitOffsetPagination,PostPageNumberPagination
from .serializers import (UserCreateSerializer,UserLoginSerializer)

User = get_user_model()


class UserCreateAPIView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserCreateSerializer
	#permissions_classes = [AllowAny] #default

class UserLoginAPIView(APIView):
	#permissions_classes = [AllowAny] #default
	#renderer_classes = [JSONRenderer] #you can use this at production
	serializer_class = UserLoginSerializer
	
	def post(self,request,*args,**kwargs):
		data = request.data #means request.POST(data coming from post method)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data = serializer.data
			return Response(new_data, status=HTTP_200_OK)
		return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)	
