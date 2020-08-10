from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ChatSerializer
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from projects.models import *
from issues.models import *

User = get_user_model()

@login_required
def all(request):
	user1 = request.user
	all_users = User.objects.all
	issues = Issue.objects.filter( Q(members__pk = request.user.pk )|Q(user=request.user))
	projects = Project.objects.filter( Q(members__pk = request.user.pk )|Q(user=request.user))
	rooms = ChatRoom.objects.filter(Q(user1=user1)|Q(user2=user1))
	CHAT=False
	PROJECT=False
	ISSUE=False
	context = {'ISSUE':ISSUE,'PROJECT':PROJECT,'CHAT':CHAT,'issues':issues,'projects':projects,'rooms':rooms,'all_users':all_users}
	return render(request, 'chats/chat_base.html',context)


@login_required
def list(request,pk):
	user1 = request.user
	user2 = User.objects.get(pk=pk)
	all_users = User.objects.all
	issues = Issue.objects.filter( Q(members__pk = request.user.pk )|Q(user=request.user))
	projects = Project.objects.filter( Q(members__pk = request.user.pk )|Q(user=request.user))
	rooms = ChatRoom.objects.filter(Q(user1=user1)|Q(user2=user1))
	context = {'issues':issues,'projects':projects,'pk':pk,'rooms':rooms,'user2':user2,'all_users':all_users}
	return render(request, 'chats/chat_base.html',context)

def ProjectChat(request,pk):
	user1 = request.user
	all_users = User.objects.all
	project = Project.objects.get(pk=pk)
	issues = Issue.objects.filter( Q(members__pk = request.user.pk )|Q(user=request.user))
	projects = Project.objects.filter( Q(members__pk = request.user.pk )|Q(user=request.user))
	rooms = ChatRoom.objects.filter(Q(user1=user1)|Q(user2=user1))
	CHAT=False
	PROJECT=True
	ISSUE=False
	context = {'ISSUE':ISSUE,'PROJECT':PROJECT,'CHAT':CHAT,'project':project,'issues':issues,'projects':projects,'rooms':rooms,'all_users':all_users}
	return render(request, 'chats/chat_base.html',context)

def IssueChat(request,pk):
	user1 = request.user
	all_users = User.objects.all
	issue = Issue.objects.get(pk=pk)
	issues = Issue.objects.filter( Q(members__pk = request.user.pk )|Q(user=request.user))
	projects = Project.objects.filter( Q(members__pk = request.user.pk )|Q(user=request.user))
	rooms = ChatRoom.objects.filter(Q(user1=user1)|Q(user2=user1))
	CHAT=False
	PROJECT=False
	ISSUE=True
	context = {'issue':issue,'issues':issues,'projects':projects,'rooms':rooms,'all_users':all_users}
	return render(request, 'chats/chat_base.html',context)


@login_required
@api_view(['GET'])
def chatList(request,pk):
	user1 = request.user
	user2 = User.objects.get(pk=pk)
	try:
		chatroom = ChatRoom.objects.get(user1=user1,user2=user2)
	except ChatRoom.DoesNotExist:
		try:
			chatroom = ChatRoom.objects.get(user1=user2,user2=user1)
		except ChatRoom.DoesNotExist:
			chatroom = ChatRoom.objects.create(user1=user1,user2=user2)

	chats = Chat.objects.filter(chatroom=chatroom).order_by('id')
	serializer = ChatSerializer(chats, many=True)
	return Response(serializer.data)

@login_required
@api_view(['POST','GET'])
def chatCreate(request,pk):
	user1 = request.user
	user2 = User.objects.get(pk=pk)
	try:
		chatroom = ChatRoom.objects.get(user1=user1,user2=user2)
	except ChatRoom.DoesNotExist:
		try:
			chatroom = ChatRoom.objects.get(user1=user2,user2=user1)
		except ChatRoom.DoesNotExist:
			chatroom = ChatRoom.objects.create(user1=user1,user2=user2)

	serializer = ChatSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save(sender=user1,reciever=user2,chatroom=chatroom)
	
	chats = Chat.objects.filter(chatroom=chatroom).order_by('id')
	serializer = ChatSerializer(chats, many=True)
	return Response(serializer.data)

@login_required
@api_view(['POST'])
def chatUpdate(request, pk):
	chat = Chat.objects.get(id=pk)
	serializer = ChatSerializer(instance=chat, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@login_required
@api_view(['DELETE'])
def chatDelete(request, pk):
	chat = Chat.objects.get(id=pk)
	if chat.deleted == False:
		chat.deleted = True
	else :
		chat.deleted = False
	chat.save()
	return Response('Item succsesfully delete!')