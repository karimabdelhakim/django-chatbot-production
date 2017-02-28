from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	# called when UserLoginForm() is called in the view.
	# if there are ValidationError here or somewhere built-in in the 
	# form class then form.is_valid() in the view will be False. 
	def clean(self,*args,**kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if username and password:#check user entered username and pass not one of them only
			user_qs = User.objects.filter(username=username)
			if user_qs.count()==1:
				user = user_qs.first()
			else: user = None
			print user
			if not user:
				raise forms.ValidationError("this user does not exist")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password")
			if not user.is_active:#active user means that he is not banned
				raise forms.ValidationError("this user is no longer active")		
		return super(UserLoginForm, self).clean(*args,**kwargs)#return whatever the function already returns by default

class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label='Email address')
	email2 = forms.EmailField(label='Confirm Email')
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username','email','email2','password']
	
	#you can use clean() method instead with same code here.
	#clean() method will give you the error up in the form html. 
	#here clean_email2() will work for email2 field and will give
	#you the error under the email2 field itself.
	#we didn't use email field instead because the cleaned data 
	#wont have email2 data it will get username and email and then stop
	#according to field array arrangment(tarteb ya3ny).
	#the previous problem wont happen with clean() method.
	#we didn't check if username already exist or not because this is
	#a modelform which knows user model fields so it also knows that 
	#username is unique by default so it will check for it by itself.
	def clean_email2(self):
		print self.cleaned_data
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError("Emails must match")
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("this email has already been registered")
		return email
	
			


