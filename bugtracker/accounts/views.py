from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.views import generic
from .models import *
from projects.models import *
from braces.views import SelectRelatedMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import DeleteView 

def register(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			p=Profile(user=user)
			p.save()
			form.save_m2m()
			login(request, user)
			messages.success(request, 'Account was created')
			return redirect('set')
		else:
			messages.info(request, 'Username or email already registered')
			context = {'form':form}
			return render(request, 'accounts/register.html', context)

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

# def create_profile(request):
# 	profile = request.user.profile
# 	form = CreateProfileForm(instance=profile)

# 	if request.method == 'POST':
# 		form = CreateProfileForm(request.POST,instance=profile)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('/')
# 		else:
# 			context = {'form':form,'message':"error"} 
# 			return render(request,'accounts/profile_form.html',context)		
			
# 	context = {'form':form}
# 	return render(request,'accounts/profile_form.html',context)

def loginUser(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

@login_required
def logoutUser(request):
	logout(request)
	return redirect('home')

@login_required
def profile_page(request):
	profiles = Profile.objects.all()
	for profile in profiles:
		if profile.user == request.user:
			context = {'profile':profile}
	return render(request,'accounts/profile.html',context)

@login_required
def delete_user(request):

	if request.method == 'POST':
		u= request.user
		u.delete()
		return redirect('/')
	else:
		return render(request,'accounts/confirm_delete.html')