from django.conf.urls import url
from . import views

app_name='Issues'

urlpatterns = [
    url(r"^$", views.IssueList.as_view(), name="all"),
    url(r"new/$", views.CreateIssue.as_view(), name="create"),
    url(r"by/(?P<pk>\d+)/$",views.IssueDetail,name="single"),
    url(r"delete/(?P<pk>\d+)/$",views.DeleteIssue.as_view(),name="delete"),
    url(r"join/(?P<pk>\d+)/$",views.JoinIssue.as_view(),name="join"),
    url(r"leave/(?P<pk>\d+)/$",views.LeaveIssue.as_view(),name="leave"),   
    url(r"solve/(?P<pk>\d+)/$",views.SolveIssue,name="solve"),
    url(r"update/(?P<pk>\d+)/$",views.UpdateIssue,name="update"),  
    url(r'add_like/(?P<pk>\d+)/$', views.add_like, name='add_like'),
    url(r"accept/(?P<pk>\d+)/$", views.accept_answer, name="accept"),
    
    url(r"issues_list_api/$", views.issues_list_api, name="issues_list_api"),
    url(r"answers_list_api/$", views.answers_list_api, name="answers_list_api"),
    

]