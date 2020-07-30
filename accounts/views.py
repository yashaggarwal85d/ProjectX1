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
from issues.models import *
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

	message = ''
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			message = 'Username OR password is incorrect'

	context = {'message':message}
	return render(request, 'accounts/login.html', context)

@login_required
def logoutUser(request):
	logout(request)
	return redirect('home')

@login_required
def profile_page(request,pk):
	user = User.objects.get(pk=pk)
	profile = user.profile
	answers = user.answers.all()
	issues = user.issues.all()
	projects = user.projects.all()
	issues_member = Issue.objects.filter( members__pk = user.pk )
	projects_member = Project.objects.filter( members__pk = user.pk )
	reputation_points = int(issues_member.count())*10 + int(projects_member.count())*50 + int(projects.count())*20 + int(issues.count())*5 + int(answers.count())*50
	for project in projects:
		reputation_points += project.members.count()*50 
	for project in projects_member:
		if project.complete == True and project.issues.count() >5:
			reputation_points += 1000
	for issue in issues_member:
		if issue.solve == True:
			reputation_points += 500
	for answer in answers:
		if answer.accepted == True:
			reputation_points += 1000
	profile.reputation_points = reputation_points
	context = {'profile':profile,'answers':answers,'issues':issues,'projects':projects,'projects_member':projects_member,'issues_member':issues_member}
	return render(request,'accounts/profile.html',context)

@login_required
def delete_user(request):

	if request.method == 'POST':
		u= request.user
		u.delete()
		return redirect('/')
	else:
		return render(request,'accounts/confirm_delete.html')