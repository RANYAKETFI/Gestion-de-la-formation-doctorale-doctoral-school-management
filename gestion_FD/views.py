from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Doctorant,User,Employe,Etat_avancement,PieceJointe,Presentation
from django.contrib import messages
from django.template import RequestContext
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import  User,auth
from .forms import LoginForm
from datetime import datetime,date

def home(request):
   doctorants=Doctorant.objects.all()
   context={
        'doctorants':doctorants
    }
   return render(request,'gestion_FD/home.html',context)
def doctorant(request):
   all_events = Presentation.objects.all()
   context = {
        "events":all_events,
        "today":date.today(),
    }
   return render(request,'gestion_FD/index_doctorant.html',context)
def employee(request):
 
   return render(request,'gestion_FD/index_employee.html')
def dpgr(request):
    all_events = Presentation.objects.all()
    etats=Etat_avancement.objects.all()
    context = {
        "events":all_events,
        "today":date.today(),
        "etats":etats,
    }
    return render(request,'gestion_FD/index_dpgr.html',context)   
def planifier_pres(request):
   titre=""
   doctorants=Doctorant.objects.all()
   employes=Employe.objects.all()
   a=date.today()
   
   if request.method == 'POST' :
     titre=request.POST['titre']
     date_pres=request.POST['date']
     heured=request.POST['heured']
     heuref=request.POST['heuref']
     doc=request.POST['doctorant']
     jury=request.POST.getlist('jury')
     docto=Doctorant.objects.all()[0]
     for d in doctorants:
        if d.id==doc:
         docto=d
         
     
     i=0
     presentation=Presentation(date_pres=date_pres,heure_debut=heured,heure_fin=heuref,doctorant=docto)
     presentation.save()
     for j in jury:
          for e in employes : 
             if  (e.id==int(jury[i])) :
                presentation.jury.add(e)
          i=i+1
     presentation.save()      
     return redirect("/dpgr")
    
   return render(request,'gestion_FD/presentations.html',{'doctorants':doctorants,'employes':employes,'titre':titre, "today":a,})    
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
        d=PieceJointe.objects.all()
        for doc in doctorants:
            if (doc.compte==request.user) :   
               et=Etat_avancement(date_etat_avancement=datetime.now(),doctorant=doc,etat=pj) 
               et.save()
                
        return render(request, 'gestion_FD/deposer_etat_doc.html', {
            'uploaded_file_url': "succés ",'d':d})
   
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
                      roles=emp.role.all()
                      for r in roles : 
                       if r.nom!="DAPGR" and r.nom!="DAPGR":
                         return redirect("/employee")  
                       else :   
                         return redirect("/dpgr") 
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
