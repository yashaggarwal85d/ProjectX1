from django.shortcuts import render,redirect
from projects.models import *
from issues.models import *
from accounts.models import *
from accounts.forms import CreateProfileForm
import django_filters
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    context = {}
    if request.user.is_authenticated:
        request.user.profile.online = True
        request.user.profile.save()
        issues = request.user.issues.all()
        projects = request.user.projects.all()
        pending_issues = request.user.issues.filter(solve=False).count
        solved_issues = request.user.issues.filter(solve=True).count
        pending_projects = request.user.projects.filter(complete=False).count
        solved_projects = request.user.projects.filter(complete=True).count
        issues_member = Issue.objects.filter( members__pk = request.user.pk )
        projects_member = Project.objects.filter( members__pk = request.user.pk )
        context = {'issues':issues,'projects':projects,'projects_member':projects_member,'issues_member':issues_member,'pending_issues':pending_issues,'solved_issues':solved_issues,'pending_projects':pending_projects,'solved_projects':solved_projects}
    return render(request,'dashboard.html',context)

@login_required
def search(request):
    search_term = request.POST.get('search')
    issues = Issue.objects.filter(tags__name__iexact=search_term)
    projects = Project.objects.filter(tags__name__iexact=search_term)

    context = {'issues':issues,'projects':projects,'search_term':search_term}
    return render(request,'search_result.html',context)

@login_required
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

@login_required
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
