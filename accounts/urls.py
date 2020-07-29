from django.contrib import admin
from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r"^register/$",views.register,name='register'),
    url(r"^login/$",views.loginUser,name='login'),
    url(r"^logout/$",views.logoutUser,name='logout'),
    url(r"^profile/(?P<pk>\d+)/$",views.profile_page,name='profile'),
    url(r"^deluser/$",views.delete_user,name="deluser"),
]