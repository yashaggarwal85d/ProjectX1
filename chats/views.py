from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from projects.models import *
from issues.models import *

User = get_user_model()

@login_required
def all(request):
	user1 = request.user
	all_users = User.objects.all
	issues = Issue.objects.filter(members__pk = request.user.pk )
	projects = Project.objects.filter(members__pk = request.user.pk)
	my_issues = Issue.objects.filter(user=request.user)
	my_projects = Project.objects.filter(user=request.user)
	context = {'my_projects':my_projects,'my_issues':my_issues ,'user':user1,'issues':issues,'projects':projects,'all_users':all_users}
	return render(request, 'chats/chat_base.html',context)