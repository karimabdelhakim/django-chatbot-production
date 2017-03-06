from datetime import datetime
from time import time
from django.contrib.contenttypes.models import ContentType 
from django.contrib.auth import get_user_model 
from django.db.models import Q
from django import forms

from rest_framework.serializers  import (ModelSerializer, 
HyperlinkedIdentityField, SerializerMethodField,
HyperlinkedRelatedField,ValidationError,EmailField,CharField,DateTimeField)

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import obtain_jwt_token

User = get_user_model()

# class UserDetailSerializer(ModelSerializer):
# 	class Meta:
# 		model = User
# 		fields = ['username','email','first_name','last_name',]

class UserCreateSerializer(ModelSerializer):
	email = EmailField(label='Email Address')#that lets emailfield be required
	email2 = EmailField(label='Confirm Email')
	class Meta:
		model = User
		fields = ['username','email','email2','password']
		extra_kwargs = {
				"password":{"write_only":True}
				}
	
	# def validate(self,data):
	# 	#you can do general validation here 
	# 	#as well as specific validation
	# 	#same way as done in validating emails
	# 	#use data['email'] as example
	# 	return data
			
	def validate_email(self,value):
		data = self.get_initial()
		email2 = data.get("email2")
		email1 = value
		if email1 != email2:
			raise ValidationError("Emails must match")
		
		user_qs = User.objects.filter(email=email1)
		if user_qs.exists():
			raise ValidationError("This user has already registered")
			
		return value

	def validate_email2(self,value):
		data = self.get_initial()#gets fields data
		email1 = data.get("email")
		email2 = value
		if email1 != email2:
			raise ValidationError("Emails must match")
		return value
			
	def create(self,validated_data):
		username = validated_data['username']
		email = validated_data['email']
		password = validated_data['password']
		user_obj = User(username = username,email = email)
		user_obj.set_password(password)
		user_obj.save()
		return validated_data

class UserLoginSerializer(ModelSerializer):
	token = CharField(allow_blank=True,read_only=True)
	#issued_at_datetime = CharField(allow_blank=True,read_only=True)
	expire_at_datetime = CharField(allow_blank=True,read_only=True)
	#total_expirDate_days = CharField(allow_blank=True,read_only=True)
	username = CharField(required=False,allow_blank=True)
	email = EmailField(label='Email Address',required=False,allow_blank=True)
	password = CharField(write_only=True,style={'base_template': 'input.html','input_type':'password'})
	
	class Meta:
		model = User
		fields = ['username','email','password','token',
				'expire_at_datetime',#'issued_at_datetime',#"total_expirDate_days"
				]

	
	def validate(self,data):
		user_obj = None
		email = data.get("email",None)
		username = data.get("username",None)
		password = data["password"]
		if not email and not username:
			raise ValidationError("A username or email is required to login")
		user = User.objects.filter(
				Q(email=email) |
				Q(username=username)
			).distinct()
		user = user.exclude(email__isnull=True).exclude(email__iexact='')
		if user.exists() and user.count() == 1:
			user_obj = user.first()
		else:
			raise ValidationError("This username/email is not valid.")	
		if user_obj:
			if not user_obj.check_password(password):
				raise ValidationError("Incorrect credentials please try again")
		
			#if user logged in with email only then return username also
			if not username:
				data["username"] = user_obj.username
			#if user logged in with username only then return email also
			if not email:
				data["email"] = user_obj.email

		#handling token
		jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
		jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
		#total_exp_date =  api_settings.JWT_REFRESH_EXPIRATION_DELTA
		payload = jwt_payload_handler(user_obj)
		token = jwt_encode_handler(payload)#new token
		print("payload",payload)
		data["token"] = token
		#data["issued_at_timestamp"] = payload["orig_iat"] #unix timestamp of the date token issued at
		#data["issued_at_datetime"] = datetime.utcfromtimestamp(payload["orig_iat"]).strftime('%Y-%m-%d T %H:%M:%S Z')
		exp_at = datetime.utcfromtimestamp(payload["exp"]).strftime('%Y-%m-%d T %H:%M:%S Z')
		data["expire_at_datetime"] = exp_at #orig_iat + token expiration time
		#data["total_expirDate_days"] = total_exp_date.days
		return data
