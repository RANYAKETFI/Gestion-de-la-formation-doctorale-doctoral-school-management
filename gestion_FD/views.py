from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Doctorant,User,Employe,Bourse,Reinscription,Etat_avancement,PieceJointe,Presentation
from django.contrib import messages
from django.template import RequestContext
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import  User,auth
from .forms import LoginForm
from datetime import datetime,date
from django.http import JsonResponse
def home(request):
   doctorants=Doctorant.objects.all()
   context={
        'doctorants':doctorants
    }
   return render(request,'gestion_FD/home.html',context)
def reins_prof(request):
   doctorants=Doctorant.objects.all()
   docs=[]
   declaration=""
   valide=""
   note="" 
   employee=Employe.objects.all()
   emp=None
   ri=False
   for e in employee:
      if e.compte==request.user:
         emp=e   
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
        'r':ri
    })
   context={
        'docs':docs,
        'declaration':declaration,
        'r':ri
    }
   return render(request,'gestion_FD/reinsc_prof.html',context)  
def reins_cfd(request):
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
        'done':done
    })
   context={
        'docs':docs,
        'r':r,
        'reins':reins,
        'done':done
    }
   return render(request,'gestion_FD/reinscription_cfd.html',context)   
def reins_cs(request):
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
        'done':done
    })
   context={
        'docs':docs,
        'r':r,
        'reins':reins,
        'done':done
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
 
   return render(request,'gestion_FD/index_employee.html')

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
