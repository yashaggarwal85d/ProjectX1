from django.conf.urls import url

from . import views

app_name = 'projects'

urlpatterns = [
    url(r"^$", views.ListProjects.as_view(), name="all"),
    url(r"^new/$", views.CreateProject.as_view(), name="create"),
    url(r"^issues/in/(?P<slug>[-\w]+)/$",views.SingleProject.as_view(),name="single"),
    url(r"join/(?P<slug>[-\w]+)/$",views.JoinProject.as_view(),name="join"),
    url(r"leave/(?P<slug>[-\w]+)/$",views.LeaveProject.as_view(),name="leave"),
]
