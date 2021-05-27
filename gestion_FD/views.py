from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Doctorant,User,Employe,Etat_avancement,PieceJointe
from django.contrib import messages
from django.template import RequestContext
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import  User,auth
from .forms import LoginForm
from datetime import datetime

def home(request):
   doctorants=Doctorant.objects.all()
   context={
        'doctorants':doctorants
    }
   return render(request,'gestion_FD/home.html',context)
def doctorant(request):
   return render(request,'gestion_FD/index_doctorant.html')
def employee(request):
 
   return render(request,'gestion_FD/index_employee.html')
def dpgr(request):
 
   return render(request,'gestion_FD/index_dpgr.html')   
def planifier_pres(request):
 
   return render(request,'gestion_FD/presentations.html')    
def archive(request):
   doctorants=Doctorant.objects.all()

   for doc in doctorants:
            if (doc.compte==request.user) :   
              d=doc
   etats=Etat_avancement.objects.all().filter(doctorant=d)
   return render(request,'gestion_FD/archive_doc.html',context={'etats':etats})   
def deposer_etat(request):
   if request.method == 'POST' and request.FILES['etat']:
        myfile = request.FILES['etat']
        pj=PieceJointe(lien= myfile)
        pj.save()
        doctorants=Doctorant.objects.all()
        for doc in doctorants:
            if (doc.compte==request.user) :   
               et=Etat_avancement(date_etat_avancement=datetime.now(),doctorant=doc,etat=pj) 
               et.save()
                
        return render(request, 'gestion_FD/deposer_etat_doc.html', {
            'uploaded_file_url': "succés "
        })
   
   return render(request,'gestion_FD/deposer_etat_doc.html')   
def login(request):
     
     if (request.method=='POST'):
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None :
          auth.login(request,user)
          doctorants=Doctorant.objects.all()
          employees=Employe.objects.all() 
          for doc in doctorants:
             if (doc.compte==user) :    
                return redirect("/doctorant")
             else :
                for emp in employees:
                   if(emp.compte==user) :
                      return redirect("/employee") 
                   else :
                      redirect("login")
                redirect("login") 
          else :
            redirect("login")          
        else : 
          messages.info(request,'login ou mot de passe invalide ')  
          return redirect("login")

     else :
        return render(request,'gestion_FD/login.html')



def logout(request):
   auth.logout(request)
   return redirect('login')
