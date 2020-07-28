from django.conf.urls import url
from . import views

app_name = 'projects'

urlpatterns = [
    url(r"^$", views.ListProjects, name="all"),
    url(r"^new/$", views.CreateProject.as_view(), name="create"),
    url(r"^issues/in/(?P<pk>\d+)/$",views.SingleProject.as_view(),name="single"),
    url(r"join/(?P<pk>\d+)/$",views.JoinProject.as_view(),name="join"),
    url(r"leave/(?P<pk>\d+)/$",views.LeaveProject.as_view(),name="leave"),
    url(r"delete/(?P<pk>\d+)/$",views.DeleteProject.as_view(),name="delete"),
    url(r"tagged/(?P<pk>\d+)/$",views.tagged,name="tagged"),
    url(r"complete/(?P<pk>\d+)/$",views.CompleteProject,name="complete"),
]