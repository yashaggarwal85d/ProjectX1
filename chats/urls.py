from django.conf.urls import url
from . import views
from django.urls import path,include

app_name='Chats'

urlpatterns = [
	path('<str:pk>/', views.list, name="list"),
    path('chat-list/<str:pk>/', views.chatList, name="chat-list"),
	path('chat-create/<str:pk>/', views.chatCreate, name="chat-create"),
	path('chat-update/<str:pk>/', views.chatUpdate, name="chat-update"),
	path('chat-delete/<str:pk>/', views.chatDelete, name="chat-delete"),
]