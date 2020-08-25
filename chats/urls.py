from django.conf.urls import url
from . import views
from django.urls import path,include

app_name='Chats'

urlpatterns = [
	path('all/', views.all, name="all"),	
]