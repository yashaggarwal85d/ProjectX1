from django.shortcuts import render
from projects.models import *
from issues.models import *
import django_filters
# Create your views here.
def home(requests):
    return render(requests,template_name='dashboard.html')

def search(request):
    search_term = request.GET['search']
    issues = Issue.objects.filter(tags__name__startswith=search_term)
    projects = Project.objects.filter(tags__name__startswith=search_term)

    context = {'issues':issues,'projects':projects,'search_term':search_term}
    return render(request,'search_result.html',context)