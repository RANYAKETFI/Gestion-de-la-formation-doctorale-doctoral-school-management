
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import path,include
from gestion_FD import views as login_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('gestion_FD/', include('gestion_FD.urls')),
    path('login/', include('gestion_FD.urls')),
    path('', include('gestion_FD.urls')),
    path('cal', include('gestion_FD.urls')),


]
