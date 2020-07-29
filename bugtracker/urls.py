from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('search',views.search,name='search'),
    path('set',views.set,name="set"),
    path('changepass',views.changepass,name="changepass"),
    url(r"^accounts/",include('accounts.urls',namespace="accounts")),
    url(r"^projects/", include("projects.urls", namespace="projects")),
    url(r"^issues/",include("issues.urls", namespace="issues")),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)