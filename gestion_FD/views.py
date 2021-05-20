from django.shortcuts import render
from django.http import HttpResponse
from .models import Doctorant
def home(request):
   doctorants=Doctorant.objects.all()
   context={
        'doctorants':doctorants
    }
   return render(request,'gestion_FD/home.html',context)