from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Doctorant,User,Employe,Bourse,Reinscription,Fiche_evaluation,Etat_avancement,PieceJointe,Presentation,These,Eval_module,Dossier_Doctorant
from .models import *
from django.contrib import messages
from django.template import RequestContext, context
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import  User,auth
from .forms import LoginForm
from datetime import datetime,date
from django.http import JsonResponse
import pandas as pd

def home(request):
   doctorants=Doctorant.objects.all()
   context={
        'doctorants':doctorants
    }
   return render(request,'gestion_FD/home.html',context)
   
   # def role_employe(request):
   # employee = Employe.objects.all() 
   # cfd=False
   # cs=False
   # jury=False
   # prof=False
   # dt=False
   # for emp in employee:
   #    if (emp.compte==request.user):
   #       this_emp=emp
   #       roles=this_emp.role.all()
   #       for role in roles:
   #          if (role.nom=='CFD'):
   #             cfd=True
   #          if (role.nom=='CS'):
   #             cs=True
   #          if (role.nom=='JURY'):
   #             jury=True
   #          if (role.nom=='PROF'):
   #             prof=True
   #          if (role.nom=='DT'):
   #             dt=True
   # context ={
   #    'CFD':cfd,
   #    'CS':cs,
   #    'JURY':jury,
   #    'PROF':prof,
   #    'DT':dt,
   # }
   # return render(request,'gestion_Fd/base_employe.html',context)

def reins_prof(request):
   doctorants=Doctorant.objects.all()
   docs=[]
   declaration=""
   valide=""
   note="" 
   employee=Employe.objects.all()
   cfd=False
   cs=False
   jury=False
   prof=False
   dt=False
   emp=None
   ri=False
   for e in employee:
      if e.compte==request.user:
         emp=e   
         this_e=e
         roles=this_e.role.all()
         for role in roles:
            if (role.nom=='CFD'):
               cfd=True
            if (role.nom=='CS'):
               cs=True
            if (role.nom=='JURY'):
               jury=True
            if (role.nom=='PROF'):
               prof=True
            if (role.nom=='DT'):
               dt=True
   for d in doctorants :
      
      ch=d.choix.all()
      for t in ch:
         for dt in t.dt.all() : 
            
            if dt.compte==request.user : 
               docs.append(d)
      for r in d.reinscription.all():
         if r.valide_dt :
           ri=True
   if request.method == 'POST' :
      declaration=request.POST['d']
      valide=request.POST['valide']
      doct=request.POST['doct']
      if valide=="accepted" : 
       r=Reinscription(declaration=declaration,avis=True,dt=True,valide_dt=True) 
       r.save()
       r.prof.add(emp)
       r.save()
       do=Doctorant.objects.all().get(pk=doct)
       do.reinscription.add(r)
       do.save()
      else :
       r=Reinscription(declaration=declaration,avis=Flase,dt=True,valide_dt=True)    
       r.save()
       r.prof.add(emp)
       r.save()
       do=Doctorant.objects.all().get(pk=doct)
       do.reinscription.add(r)
       do.save()
      return render(request,'gestion_FD/reinsc_prof.html',{
        'docs':docs,
        'declaration':declaration,
        'r':ri,
        'CFD':cfd,
        'CS':cs,
        'JURY':jury,
        'PROF':prof,
        'DT':dt,
    })
   context={
        'docs':docs,
        'declaration':declaration,
        'r':ri,
        'CFD':cfd,
        'CS':cs,
        'JURY':jury,
        'PROF':prof,
        'DT':dt,
    }
   return render(request,'gestion_FD/reinsc_prof.html',context)  
def reins_cfd(request):
   employee = Employe.objects.all() 
   cfd=False
   cs=False
   jury=False
   prof=False
   dt=False
   for emp in employee:
      if (emp.compte==request.user):
         this_emp=emp
         roles=this_emp.role.all()
         for role in roles:
            if (role.nom=='CFD'):
               cfd=True
            if (role.nom=='CS'):
               cs=True
            if (role.nom=='JURY'):
               jury=True
            if (role.nom=='PROF'):
               prof=True
            if (role.nom=='DT'):
               dt=True
   doctorants=Doctorant.objects.all()
   docs=[]
   done=False
   r=False
   reins=None
   for d in doctorants :
      for re in d.reinscription.all():
           
           if re.valide_dt :
            r=True
            reins=re
            docs.append(d)

   if request.method == 'POST' :
      
      valide=request.POST['valide']
      doct=request.POST['doct']
      if valide=="accepted":
         reins.valide_cfd=True
      
      else:
         reins.valide_cfd=False
      reins.save() 
      done=True
      return render(request,'gestion_FD/reinscription_cfd.html',{
        'docs':docs,
        'r':r,
        'reins':reins,
        'done':done,
        'CFD':cfd,
        'CS':cs,
        'JURY':jury,
        'PROF':prof,
        'DT':dt,
    })
   context={
        'docs':docs,
        'r':r,
        'reins':reins,
        'done':done,
        'CFD':cfd,
        'CS':cs,
        'JURY':jury,
        'PROF':prof,
        'DT':dt,
    }
   return render(request,'gestion_FD/reinscription_cfd.html',context)   
def reins_cs(request):
   employee = Employe.objects.all() 
   cfd=False
   cs=False
   jury=False
   prof=False
   dt=False
   for emp in employee:
      if (emp.compte==request.user):
         this_emp=emp
         roles=this_emp.role.all()
         for role in roles:
            if (role.nom=='CFD'):
               cfd=True
            if (role.nom=='CS'):
               cs=True
            if (role.nom=='JURY'):
               jury=True
            if (role.nom=='PROF'):
               prof=True
            if (role.nom=='DT'):
               dt=True
   doctorants=Doctorant.objects.all()
   docs=[]
   done=False
   r=False
   reins=None
   for d in doctorants :
      for re in d.reinscription.all():
            if re.valide_cfd :
             r=True
             reins=re
             docs.append(d)
   if request.method == 'POST' :
      
      valide=request.POST['valide']
      doct=request.POST['doct']
      if valide=="accepted":
         reins.valide_cs=True
         
         do=Doctorant.objects.all().get(pk=doct)
         do.reinscrit=True
         do.annee_etude=do.annee_etude+1
         do.save()
      else:
         reins.valide_cs=False

      reins.save() 
      done=True
      return render(request,'gestion_FD/reinscription_cs.html',{
        'docs':docs,
        'r':r,
        'reins':reins,
        'done':done,
        'CFD':cfd,
        'CS':cs,
        'JURY':jury,
        'PROF':prof,
        'DT':dt,
    })
   context={
        'docs':docs,
        'r':r,
        'reins':reins,
        'done':done,
        'CFD':cfd,
        'CS':cs,
        'JURY':jury,
        'PROF':prof,
        'DT':dt,
    }
   return render(request,'gestion_FD/reinscription_cs.html',context)        
def reinscription(request):
   doctorants=Doctorant.objects.all()
   reins=False
   for doc in doctorants: 
       if doc.compte==request.user : 
          d=doc
          break 
   reins=d.rein_envo
         
   v=""
   if request.method == 'POST' :
    nom=request.POST['nom']
    prenom=request.POST['prenom']
    sexe=request.POST['sexe']
    daten=request.POST['daten']
    lieun=request.POST['lieun']
    situation=request.POST['situation']
    activite=request.POST['activite']
    employeur=request.POST['employeur']
    adresse=request.POST['adresse']
    tel=request.POST['tel']
    email=request.POST['email']
    titrethese=request.POST['titrethese']
    cotut=request.POST['cotut']
    part=request.POST['part']
    codirect=request.POST['codirec']
    bourse=request.POST['bourse']
    type_bourse=request.POST['typebourse']
    duree=request.POST['duree']

    if cotut=="Oui":
       v="Oui" 
    else :
       v="Non"    
    
    Doctorant.objects.filter(pk=d.pk).update(nom=nom)
    Doctorant.objects.filter(pk=d.pk).update(prenom=prenom)
    Doctorant.objects.filter(pk=d.pk).update(sexe=sexe)
    Doctorant.objects.filter(pk=d.pk).update(date_naissance=daten)
    Doctorant.objects.filter(pk=d.pk).update(wilaya_naissance=lieun)
    Doctorant.objects.filter(pk=d.pk).update(situation_familiale=situation)
    Doctorant.objects.filter(pk=d.pk).update(profession=activite)
    Doctorant.objects.filter(pk=d.pk).update(employeur=employeur)
    Doctorant.objects.filter(pk=d.pk).update(adresse=adresse)
    Doctorant.objects.filter(pk=d.pk).update(telephone=tel)
    Doctorant.objects.filter(pk=d.pk).update(email=email)
    Doctorant.objects.filter(pk=d.pk).update(rein_envo=True) 
    doc=Doctorant.objects.get(pk=d.pk)
    reins=doc.rein_envo

    if duree=="":
       duree=0    
    if bourse=="Oui":
       bourse=Bourse(type_bourse=type_bourse,duree=duree)  
       bourse.save()
       doc.Bourse=bourse
       doc.save()
    v="Vous vous etes réinscrit avec succés , veuillez attendre l'accord de la DPGR "    
 
   context={
      'v':v,
      'reins':reins
   }
   return render(request,'gestion_FD/reinscription_doc.html',context)
      
def doctorant(request):
   ev = Presentation.objects.all()
   doctorants=Doctorant.objects.all()
   all_events=[]
   for doc in doctorants:
            if (doc.compte==request.user) :   
              d=doc
   all_events=Presentation.objects.all().filter(doctorant=d)
  
   context = {
        "events":all_events,
        "today":date.today(),
    }
   return render(request,'gestion_FD/index_doctorant.html',context)
def employee(request):
   employee = Employe.objects.all() 
   cfd=False
   cs=False
   jury=False
   prof=False
   dt=False
   for emp in employee:
      if (emp.compte==request.user):
         this_emp=emp
         roles=this_emp.role.all()
         for role in roles:
            if (role.nom=='CFD'):
               cfd=True
            if (role.nom=='CS'):
               cs=True
            if (role.nom=='JURY'):
               jury=True
            if (role.nom=='PROF'):
               prof=True
            if (role.nom=='DT'):
               dt=True
   events = Presentation.objects.all()
   all_events=[]
   for e in events  :
      for emp in e.jury.all():
         if emp.compte==request.user :
            all_events.append(e)

   events = Presentation.objects.all()
   today= date.today()
   year=today.year-1
   this_year=date(year, 1,1 )
    # if filters applied then get parameter and filter based on condition else return object
   if request.GET:  
        event_arr = []
        
        for i in all_events:
            event_sub_arr = {}
            event_sub_arr['title'] = "presentation"
            start_date = datetime.datetime.strptime(str(i.date_pres.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            event_sub_arr['start'] = start_date
            event_arr.append(event_sub_arr)
        return HttpResponse(json.dumps(event_arr))

   context = {
        "events":all_events,
        "pres":events,
        "today": today,
        "this_year":this_year,
        'CFD':cfd,
        'CS':cs,
        'JURY':jury,
        'PROF':prof,
        'DT':dt, 
    }
   return render(request,'gestion_FD/index_employee.html',context)

def dpgr(request):
   etats=Etat_avancement.objects.all()
   all_events = Presentation.objects.all()
   events = Presentation.objects.all()
   today= date.today()
   year=today.year-1
   this_year=date(year, 1,1 )
    # if filters applied then get parameter and filter based on condition else return object
   if request.GET:  
        event_arr = []
        
        for i in all_events:
            event_sub_arr = {}
            event_sub_arr['title'] = "presentation"
            start_date = datetime.datetime.strptime(str(i.date_pres.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            event_sub_arr['start'] = start_date
            event_arr.append(event_sub_arr)
        return HttpResponse(json.dumps(event_arr))

   context = {
        "events":all_events,
        "pres":events,
        "etats":etats,
        "today": today,
        "this_year":this_year 

    }
   return render(request,'gestion_FD/index_dpgr.html',context)   
def planifier_pres(request):
   titre=""
   dkhl=""
   doctorants=Doctorant.objects.all()
   employes=Employe.objects.all()
   a=date.today()
   ju=False
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
          
          for emp in Employe.objects.all() : 
             
             if  (emp.id==int(jury[i])) :
                
                presentation.jury.add(emp)
                for ro in emp.role.all():
                    
                    if ro.nom=="JURY" :
                      
                       ju==True
                    break
                
                if not ju :
                   
                   for rol in Role.objects.all():
                      if rol.nom=="JURY" :
                         
                         emp.role.add(rol) 
                         emp.save() 
                   
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
                       if r.nom!="DAPGR" and r.nom!="ADPGR":
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
#zeyneb 
def inscription(request):
  #THIS IS INSCRIPTION DOCTORANT
   alltheses= These.objects.all()
   theses=These.objects.all()
   c=[]
  
   vv=""
   d=None
   for d in Doctorant.objects.all():
         if d.compte==request.user:
           vv=""
           break;  
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
   
          
      Doctorant.objects.filter(compte=request.user).update(nom=nom,prenom=prenom,date_naissance=dnaiss,wilaya_naissance=lieunaiss,dossier_id=dd.id,inscrit=True)
      for d in alldoc:
         if d.compte==request.user:
           vv="Vous vous etes inscrit avec succées ! "
           break;        
      i=0
      for ch in choix:
       d.choix.add(ch)
       d.save()
       i=i+1
      context={  
         'vv':vv,
        }

   return render(request, 'gestion_FD/inscription_doc.html',{'alltheses': alltheses,'theses':theses,'c':c,
           'uploaded_file_url': "succés ", 'vv':vv,'d':d,
        })
def affecterthses(request):
    alldoctorants= Doctorant.objects.all()
    allthese=These.objects.all()
    i=1
    for p in allthese:
       p.prise = False  
       p.save()  
    while i<=len(alldoctorants):
      j=0
      for doc in alldoctorants:
         if (i==doc.classement_concours):
            choices=doc.choix.all()
            for t in choices:
               if t.prise == True:
                  continue
               else:
                  t.prise=True
                  t.save()
                  doc.choixfinal=t.intitule
                  doc.save()
                  break
      i=i+1
    return render(request,'gestion_FD/inscription_dpgr.html',{'alldoctorants':alldoctorants,'allthese':allthese,'longeur':len(alldoctorants)})

def archiveetatAvancement(request):
   alldoctorants= Doctorant.objects.all()
   alletat= Etat_avancement.objects.all()
   allpieces= PieceJointe.objects.all()
   return render (request,'gestion_FD/archiveEtatAvancement.html',{'alldoctorants':alldoctorants,'alletat':alletat,'allpieces':allpieces})

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
#lamia 
def deposer_these_cfd(request):
   employee = Employe.objects.all() 
   cfd=False
   cs=False
   jury=False
   prof=False
   dt=False
   for emp in employee:
      if (emp.compte==request.user):
         this_emp=emp
         roles=this_emp.role.all()
         for role in roles:
            if (role.nom=='CFD'):
               cfd=True
            if (role.nom=='CS'):
               cs=True
            if (role.nom=='JURY'):
               jury=True
            if (role.nom=='PROF'):
               prof=True
            if (role.nom=='DT'):
               dt=True
   context ={
      'CFD':cfd,
      'CS':cs,
      'JURY':jury,
      'PROF':prof,
      'DT':dt,
   }
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
      
   return render(request,'gestion_FD/deposer_theses_cfd.html',context)

def lister_theses(request):
   employee = Employe.objects.all() 
   cfd=False
   cs=False
   jury=False
   prof=False
   dt=False
   for emp in employee:
      if (emp.compte==request.user):
         this_emp=emp
         roles=this_emp.role.all()
         for role in roles:
            if (role.nom=='CFD'):
               cfd=True
            if (role.nom=='CS'):
               cs=True
            if (role.nom=='JURY'):
               jury=True
            if (role.nom=='PROF'):
               prof=True
            if (role.nom=='DT'):
               dt=True
   these = These.objects.all()
   theses = []
   for t in these:
      theses.append(t)
   context ={
         'theses':theses, 
         'allemp':employee,
         'CFD':cfd,
         'CS':cs,
         'JURY':jury,
         'PROF':prof,
         'DT':dt,
      }
            
   return render(request,'gestion_Fd/liste_theses.html',context)


def inscription_cfd(request):
   employee = Employe.objects.all() 
   cfd=False
   cs=False
   jury=False
   prof=False
   dt=False
   for emp in employee:
      if (emp.compte==request.user):
         this_emp=emp
         roles=this_emp.role.all()
         for role in roles:
            if (role.nom=='CFD'):
               cfd=True
            if (role.nom=='CS'):
               cs=True
            if (role.nom=='JURY'):
               jury=True
            if (role.nom=='PROF'):
               prof=True
            if (role.nom=='DT'):
               dt=True
   
   doctorants=Doctorant.objects.all()
   theses = []
   for doc in doctorants:
      for t in doc.choix.all(): 
        if (t.prise):
           theses.append(t)

   context ={
      'theses':theses,
      'doc':doctorants,
      'CFD':cfd,
      'CS':cs,
      'JURY':jury,
      'PROF':prof,
      'DT':dt,
   }
   if request.method == 'POST':
      id_these = request.POST['id_th']
      if request.POST.get('accept'):
         These.objects.filter(id=id_these).update(valide_cfd=True)
      else :
         These.objects.filter(id=id_these).update(valide_cfd=False)
      context2 ={
         'theses':theses,
         'nom_doc':doc_name,
         'prenom_doc':doc_prenom,
         'CFD':cfd,
         'CS':cs,
         'JURY':jury,
         'PROF':prof,
         'DT':dt,  
      }
      return render(request,'gestion_Fd/inscription_cfd.html',context2)
   else:
      return render(request,'gestion_Fd/inscription_cfd.html',context)

def inscription_cs(request):

   employee = Employe.objects.all() 
   cfd=False
   cs=False
   jury=False
   prof=False
   dt=False
   for emp in employee:
      if (emp.compte==request.user):
         this_emp=emp
         roles=this_emp.role.all()
         for role in roles:
            if (role.nom=='CFD'):
               cfd=True
            if (role.nom=='CS'):
               cs=True
            if (role.nom=='JURY'):
               jury=True
            if (role.nom=='PROF'):
               prof=True
            if (role.nom=='DT'):
               dt=True
   
   doctorant = Doctorant.objects.filter(inscrit=True)
   doctorants = []
   these = ""
   for doc in doctorant:
      for t in doc.choix.all():
         if (t.prise) and (t.valide_cfd):
            doctorants.append(doc)
            these=t.intitule
   context ={
      'doctorants':doctorants,
      'these':these,
      'CFD':cfd,
      'CS':cs,
      'JURY':jury,
      'PROF':prof,
      'DT':dt,
   }

   if request.method == 'POST':
      id_doc = request.POST['id_doctorant']
      if request.POST.get('accept'):
         Doctorant.objects.filter(id=id_doc).update(inscr_valid_cs=True)
      else :
         Doctorant.objects.filter(id=id_doc).update(inscr_valid_cs=False)
      context2 ={
         'doctorants':doctorants,
         'these':these,
      }
      return render(request,'gestion_FD/inscription_cs.html',context2)
   return render(request,'gestion_FD/inscription_cs.html',context)
   

#sirine 
def evaluation_jury(request):

       # Préparation des paramètres à passer
       employe=Employe.objects.all()
       cfd=False
       cs=False  
       prof=False
       dt=False
       jury=False
       mydocs=[]
       for emp in employe: 
          if (emp.compte==request.user):
                 this_emp=emp
                 roles=this_emp.role.all()
                 for role in roles:
                        if (role.nom=='JURY'):
                                jury=True
                        if (role.nom=='CFD'):
                                cfd=True
                        if (role.nom=='CS'):
                                cs=True
                        if (role.nom=='PROF'):
                                prof=True
                        if (role.nom=='DT'):
                                dt=True
                 #Récupérer les doctorants de ce jury
                 pres=Presentation.objects.all()
                 for p in pres:
                        ju=p.jury.all()
                        doc=p.doctorant
                        for j in ju:
                               if (j.compte==request.user):
                                      mydocs.append(doc)
                 mydocs= list(dict.fromkeys(mydocs))
                        
          
       context={
        'jury':jury,
        'CFD':cfd,
        'CS':cs,
        'JURY':jury,
        'PROF':prof,
        'DT':dt,
        'mydocs': mydocs,
        'doctorants':mydocs
         }
       if request.method == 'POST' :
              if request.POST.get('mydocs'):
                     id1=request.POST['mydocs']
                     d=Doctorant.objects.filter(id=id1).first()
                     evals=Fiche_evaluation.objects.filter(doctorant=d).order_by('-date_eval')
                     return render(request, 'gestion_FD/fiches_evaluation_employee.html', {
                        'fiches': evals,
                        'jury': jury,
                        'mydocs': mydocs,
                        'doctorants':mydocs,
                        'CFD':cfd,
                        'CS':cs,
                        'JURY':jury,
                        'PROF':prof,
                        'DT':dt,
                           })
                     
              if request.POST.get('Date'):
                     myfile = request.FILES['fiche']
                     date_eval=request.POST['Date']
                     id_doc=request.POST['doctorant']
                     doctorant=Doctorant.objects.filter(id=id_doc).first()
                     pj=PieceJointe(lien= myfile)
                     pj.save()
                     employe=Employe.objects.all()
                     for emp in employe: 
                        if (emp.compte==request.user):
                           this_emp=emp
                 
                     fiche=Fiche_evaluation(date_eval=date_eval,fichier=pj,doctorant=doctorant)
                     fiche.save()
                     fiche.jury.add(this_emp)
                     fiche.save()

                     return render(request, 'gestion_FD/fiches_evaluation_employee.html', {
                         'uploaded_file_url': "succés ",
                         'jury': jury,
                         'mydocs': mydocs,
                         'doctorants':mydocs,
                         'CFD':cfd,
                         'CS':cs,
                         'JURY':jury,
                         'PROF':prof,
                         'DT':dt,
                        })
       else : 
          return render(request,'gestion_FD/fiches_evaluation_employee.html',context) 
              
         
def valider_eval(request):
   employe=Employe.objects.all()
   cfd=False
   prof=False
   dt=False
   jury=False
   cs=False
   for emp in employe: 
          if (emp.compte==request.user):
                 this_emp=emp
                 roles=this_emp.role.all()
                 for role in roles:
                        if (role.nom=='CS'):
                                cs=True
                        if (role.nom=='CFD'):
                                cfd=True
                        if (role.nom=='JURY'):
                                jury=True
                        if (role.nom=='PROF'):
                                prof=True
                        if (role.nom=='DT'):
                                dt=True
   fiches_nouvelles=Fiche_evaluation.objects.filter(valide__isnull=True).order_by('-date_eval')
   archive=Fiche_evaluation.objects.filter(valide__isnull=False).order_by('-date_eval')
   context={
        'cs':cs,
         'new': fiches_nouvelles,
         'archive': archive,
         'CFD':cfd,
         'CS':cs,
         'JURY':jury,
         'PROF':prof,
         'DT':dt,
         }
   if request.method == 'POST':
          idf=request.POST['id_fiche']
          if request.POST.get('accept'):
                 Fiche_evaluation.objects.filter(id=idf).update(valide=True)
          else :
                 Fiche_evaluation.objects.filter(id=idf).update(valide=False)
          context2={
             'cs': cs,
             'new': Fiche_evaluation.objects.filter(valide__isnull=True).order_by('-date_eval'),
             'archive' : Fiche_evaluation.objects.filter(valide__isnull=False).order_by('-date_eval'),
             'CFD':cfd,
             'CS':cs,
             'JURY':jury,
             'PROF':prof,
             'DT':dt,
          }
          return render(request,'gestion_FD/valider_evaluation.html', context2 )   
   else :
          return render(request,'gestion_FD/valider_evaluation.html',context)
          
def notes_prof(request):
 employe=Employe.objects.all()
 cfd=False
 prof=False
 dt=False
 jury=False
 cs=False
 this_emp=None
 for emp in employe: 
          if (emp.compte==request.user):
                 this_emp=emp
                 roles=this_emp.role.all()
                 for role in roles:
                        if (role.nom=='CS'):
                                cs=True
                        if (role.nom=='CFD'):
                                cfd=True
                        if (role.nom=='JURY'):
                                jury=True
                        if (role.nom=='PROF'):
                                prof=True
                        if (role.nom=='DT'):
                                dt=True
 modules=Module.objects.filter(prof=this_emp)
 mydocs=[]
 for m in modules:
        docs=m.etudiants.all()
        for d in docs:
               mydocs.append(d)
 mydocs= list(dict.fromkeys(mydocs))
 evals=Eval_module.objects.filter(module__in=modules,etudiant__in=mydocs).order_by('module')
 context={'modules': modules, 'evals':evals, 
             'CFD':cfd,
             'CS':cs,
             'JURY':jury,
             'PROF':prof,
             'DT':dt,}
 if request.method == 'POST' :
        if request.POST.get('modif') :
               id_eval=request.POST['id_eval']
               modif=request.POST['modif']
               Eval_module.objects.filter(id=id_eval).update(Note=modif)
               evals2=Eval_module.objects.filter(module__in=modules,etudiant__in=mydocs).order_by('module')
               return render(request,'gestion_FD/notes_prof.html',{
                  'modules':modules,
                  'evals': evals2, 
                  'CFD':cfd,
                  'CS':cs,
                  'JURY':jury,
                  'PROF':prof,
                  'DT':dt,
               })
        else:
         myfile = request.FILES['notes']
         date_eval=request.POST['Date']
         id_module=request.POST['module']
         type=request.POST['type']
         pj=PieceJointe(lien= myfile)
         pj.save()
         url=pj.lien.url
         if url.lower().endswith('.xlsx') :
                  notes=pd.read_excel(myfile)
                  l1=list(notes.columns)
                  l1.sort()
                  l2=['appreciation', 'matricule', 'nom', 'note', 'prenom']
                  l2.sort()
                  if (l1==l2):
                     mod=Module.objects.filter(id=id_module).first()
                     for i in range(0,len(notes)):
                           matricule=notes.at[i,'matricule']
                           note=notes.at[i,'note']
                           app=notes.at[i,'appreciation']
                           doc=Doctorant.objects.filter(matricule=matricule).first()
                           evaluation=Eval_module(Note=note,date_eval=date_eval,etudiant=doc,module=mod,appreciation=app,type=type)
                           evaluation.save()
                     format='Notes importées avec succés'        
                  else:
                         format='Le fichier excel importé ne respecte pas le modèle, veuillez suivre le modèle fourni ci-dessous'
         else :
                  format='Format erroné, vous devez importer un fichier excel (.xlsx )'
         return render(request, 'gestion_FD/notes_prof.html', {
                           'uploaded_file_url': format,
                           'modules' : modules,
                           'evals' : evals,
                           'CFD':cfd,
                           'CS':cs,
                           'JURY':jury,
                           'PROF':prof,
                           'DT':dt,
                           })
        
 else:     
   return render(request,'gestion_FD/notes_prof.html',context)
           
def notes_doc(request):
   doctorants=Doctorant.objects.all()
   for doc in doctorants:
          if (doc.compte==request.user) :
                 this_doc=doc
                 break
   notes=Eval_module.objects.filter(etudiant=this_doc).order_by('-date_eval')
   context={'notes':notes}          
   return  render(request,'gestion_FD/notes_doctorant.html',context) 
def reins_dpgr(request):
   etats=Etat_avancement.objects.all()
   context={'etats':etats}
   return  render(request,'gestion_FD/reinscription_dpgr.html',context)    