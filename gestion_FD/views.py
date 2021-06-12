from django.db.models.aggregates import Count
from django.db.models.fields.related import ManyToManyField
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Doctorant, Fiche_evaluation,User,Employe,Etat_avancement,PieceJointe,Dossier_Doctorant,These
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

def deposer_these_cfd(request):
   if request.method == 'POST':
      intetArr = request.POST.getlist('tnom')
      resArr = request.POST.getlist('tresume')
      print(intetArr,resArr)
      if(intetArr != []):
         for i in range(len(intetArr)):
            if (resArr != []):
               intet = intetArr[i]
               res = resArr[i]
               these = These(intitule = intet, resume = res)
               these.save()
      
   return render(request,'gestion_FD/deposer_theses_cfd.html')

def inscription(request):
  #THIS IS INSCRIPTION DOCTORANT
   alltheses= These.objects.all()
   theses=These.objects.all()
   c=[]
   #c2=[]
   if request.method=="POST":
      nom=request.POST['fname']
      prenom=request.POST['lname']
      dnaiss=request.POST['dnaiss']
      lieunaiss=request.POST['lieunaiss']
      matricule=request.POST['matricule']
      #choix=request.POST.getlist('thesechoisi')
      choix=request.POST.getlist('choix')
      myfile = request.FILES['cv']
      fs=FileSystemStorage()
      fs.save(myfile.name,myfile)
      pj1=PieceJointe(lien= myfile)
      pj1.save()
      myfile1 = request.FILES['lettremotiv']
      fs=FileSystemStorage()
      fs.save(myfile1.name,myfile1)
      pj2=PieceJointe(lien= myfile1)
      pj2.save()  
      myfile2 = request.FILES['photo']
      fs=FileSystemStorage()
      fs.save(myfile2.name,myfile2)
      pj3=PieceJointe(lien= myfile2)
      pj3.save()
      dd= Dossier_Doctorant()
      dd.save()
      dd.pieces.add(pj1)
      dd.pieces.add(pj2)
      dd.pieces.add(pj3)
      dd.save()
      c=choix
      alldoc =Doctorant.objects.all()
      for d in alldoc:
         if d.matricule==matricule:
          d.alter(matricule=matricule,nom=nom,prenom=prenom,date_naissance=dnaiss,wilaya_naissance=lieunaiss,dossier_id=dd.id,compte_id=request.user.id)
          d.save()
          break
      i=0
      for ch in choix:
       d.choix.add(ch)
       d.save()
       i=i+1
      context={  
        }

   return render(request, 'gestion_FD/inscription_doc.html',{'alltheses': alltheses,'theses':theses,'c':c,
           'uploaded_file_url': "succés " 
        })
def affecterthses(request):
    alldoctorants= Doctorant.objects.all()
    i=1
    while i<=len(alldoctorants):
      j=0
      for doc in alldoctorants:
         if (i==doc.classement_concours):
            choices=doc.choix.all()
            for t in choices:
               if(t.prise==False):
                  t.prise==True
                  t.save()
                  doc.choixFinal=t.intitule
                  doc.save()
                  break
      i=i+1
    return render(request,'gestion_FD/inscription_dpgr.html',{'alldoctorants':alldoctorants,'longeur':len(alldoctorants)})
def archiveetatAvancement(request):
   alldoctorants= Doctorant.objects.all()
   alletat= Etat_avancement.objects.all()
   allpieces= PieceJointe.objects.all()
   return render (request,'gestion_FD/archiveEtatAvancementl.html',{'alldoctorants':alldoctorants,'alletat':alletat,'allpieces':allpieces})

def archiveDossierDoctorant(request):
   allpiecesdos=[]
   alldoctorants= Doctorant.objects.all()
   allpieces= PieceJointe.objects.all()
   alldossiers= Dossier_Doctorant.objects.all()
   allpiecesdos=Dossier_Doctorant.pieces.__getattribute__
   return render(request,'gestion_FD/archiveDossierDoctorant.html',{'alldoctorants':alldoctorants,'allpieces':allpieces,'alldossiers':alldossiers,'allpiecesdos':allpiecesdos} )

def archiveFicheEvalution(request):
   alldoctorants= Doctorant.objects.all()
   allpieces= PieceJointe.objects.all()
   allfiches=Fiche_evaluation.objects.all()
   allemploye= Employe.objects.all()
   return render(request,'gestion_FD/archiveFicheEvaluation.html',{'alldoctorants':alldoctorants,'allpieces':allpieces,'allfiches':allfiches,'allemploye':allemploye})