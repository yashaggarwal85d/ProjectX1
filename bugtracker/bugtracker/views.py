from django.shortcuts import render,redirect
from projects.models import *
from issues.models import *
from accounts.models import *
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

    profiles = Profile.objects.all()
    for prof in profiles:
        if prof.user == request.user:
            profile = prof
    
    if request.method == 'POST':
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        country = request.POST.get('country')
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        occupation = request.POST.get('occupation')
        working_at = request.POST.get('working_at')
        
        if first_name != '':
            profile.first_name = first_name
        if last_name != '':
            profile.last_name = last_name
        if country != '':
            profile.country = country
        if location != '':
            profile.location = location
        if phone != '':
            profile.phone = phone
        if occupation != '':
            profile.occupation = occupation
        if working_at != '':
            profile.working_at = working_at
        
        profile.save()  

    form = PasswordChangeForm(request.user, request.POST)
    context = {'profile':profile , 'form':form}        
    return render(request,'settings.html',context)

def changepass(request):

    profiles = Profile.objects.all()
    for prof in profiles:
        if prof.user == request.user:
            profile = prof

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            message = "password changed successfully"
        else:
            message = 'Error occured please check the password again'
            
    context = {'message':message,'form':form,'profile':profile}
    return render(request,'settings.html',context)
