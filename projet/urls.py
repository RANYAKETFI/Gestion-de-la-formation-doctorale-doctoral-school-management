
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gestion_FD/', include('gestion_FD.urls')),
    path('', include('gestion_FD.urls')),

]
