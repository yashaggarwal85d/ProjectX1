from django.conf.urls import url
from . import views
from django.urls import path,include

app_name='Chats'

urlpatterns = [
	path('all/', views.all, name="all"),
	path('<str:pk>/', views.list, name="list"),
	path('project/<str:pk>/', views.ProjectChat, name="project"),
	path('issue/<str:pk>/', views.IssueChat, name="issue"),
    
	path('chat-list/<str:pk>/', views.chatList, name="chat-list"),
	path('chat-create/<str:pk>/', views.chatCreate, name="chat-create"),
	path('chat-update/<str:pk>/', views.chatUpdate, name="chat-update"),
	path('chat-delete/<str:pk>/', views.chatDelete, name="chat-delete"),

	path('Projectchat-list/<str:pk>/', views.ProjectchatList, name="Projectchat-list"),
	path('Projectchat-create/<str:pk>/', views.ProjectchatCreate, name="Projectchat-create"),
	
	path('Issuechat-list/<str:pk>/', views.IssuechatList, name="Issuechat-list"),
	path('Issuechat-create/<str:pk>/', views.IssuechatCreate, name="Issuechat-create"),
	
]