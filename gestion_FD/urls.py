
from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home', views.home,name="home"),
        path('', views.login,name="login"),
        path('login', views.login,name="login"),
        path('doctorant/deposer_etat', views.deposer_etat,name="deposer_etat"),
        path('doctorant/archive', views.archive,name="archive"),
        path('dpgr', views.dpgr,name="dpgr"),
        path('dpgr/planifier_pres', views.planifier_pres,name="planifier_pres"),
        path('employee', views.employee,name="emplpoyee"),
        path('doctorant', views.doctorant,name="doctorant"),
        path('logout', views.logout,name="logout"),
        path('doctorant/reinscription', views.reinscription,name="reinscription"),
        path('employee/reinsc_prof', views.reins_prof,name="reinscription"),
        path('employee/reinsc_cfd', views.reins_cfd,name="reinscription"),
        path('employee/reinsc_cs', views.reins_cs,name="reinscription"),



]
if settings.DEBUG: 
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
