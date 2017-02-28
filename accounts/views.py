from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)
from django.shortcuts import render,redirect
from .forms import UserLoginForm,UserRegisterForm
#from django.contrib import messages

# Create your views here.
def login_view(request):
	next = request.GET.get('next')
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username,password=password)
		login(request, user)
		if next:
			return redirect(next)
		print request.user.is_authenticated()
		return redirect("/")
		
	return render(request,"registration/form.html",{"form":form,"title":title})

def register_view(request):
	next = request.GET.get('next')
	title = "Register"
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get("password")
		user.set_password(password)
		user.save()#user is registered
		new_user = authenticate(username=user.username,password=password)
		login(request, new_user)
		if next:
			return redirect(next)
		print request.user.is_authenticated()
		return redirect("/")

	return render(request,"registration/form.html",{"form":form,"title":title})

def logout_view(request):
	logout(request)
	return redirect("/")
	

