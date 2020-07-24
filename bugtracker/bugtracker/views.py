from django.shortcuts import render
from projects.models import *
from issues.models import *
import django_filters

# Create your views here.
def home(requests):
    issues = Issue.objects.all()
    projects = Project.objects.all()
    context = {'issues':issues,'projects':projects}
    return render(requests,'dashboard.html',context)

def search(request):
    search_term = request.GET['search']
    issues = Issue.objects.filter(tags__name=search_term)
    projects = Project.objects.filter(tags__name=search_term)

    context = {'issues':issues,'projects':projects,'search_term':search_term}
    return render(request,'search_result.html',context)