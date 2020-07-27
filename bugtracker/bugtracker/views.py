from django.shortcuts import render,redirect
from projects.models import *
from issues.models import *
from accounts.models import *
from accounts.forms import CreateProfileForm
import django_filters
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.
def home(requests):
    issues = Issue.objects.all()
    projects = Project.objects.all()
    context = {'issues':issues,'projects':projects}
    return render(requests,'dashboard.html',context)

def search(request):
    search_term = request.POST.get('search')
    issues = Issue.objects.filter(tags__name=search_term)
    projects = Project.objects.filter(tags__name=search_term)

    context = {'issues':issues,'projects':projects,'search_term':search_term}
    return render(request,'search_result.html',context)

def set(request):

    profile = request.user.profile
    profile_form = CreateProfileForm(instance=profile)
    message = ''
    if request.method == 'POST':
        profile_form = CreateProfileForm(request.POST,request.FILES,instance=profile)
        if profile_form.is_valid():
            profile_form.save() 
            message = "Info edited successfully"
        else:
            message = "Info editing failed"
        
    form = PasswordChangeForm(request.user, request.POST)
    context = {'message':message,'form':form,'profile_form':profile_form,'profile':profile}        
    return render(request,'settings.html',context)

def changepass(request):

    profile = request.user.profile
    profile_form = CreateProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)  # Important!
            message = "password changed successfully"
        else:
            message = 'Error occured please check the password again'

    form = PasswordChangeForm(request.user, request.POST)             
    context = {'profile_form':profile_form,'message':message,'form':form,'profile':profile}
    return render(request,'settings.html',context)
