from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('search',views.search,name='search'),
    path('accounts/',include('accounts.urls')),
    url(r"^projects/", include("projects.urls", namespace="projects")),
    url(r"^issues/",include("issues.urls", namespace="issues")),
]
