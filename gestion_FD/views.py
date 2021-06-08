from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Doctorant, Eval_module, Fiche_evaluation, Presentation,User,Employe,Etat_avancement,PieceJointe, Module
from django.contrib import messages
from django.template import RequestContext
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import  User,auth
from .forms import LoginForm
from datetime import datetime
import pandas as pd

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

def evaluation_jury(request):

       # Préparation des paramètres à passer
       employe=Employe.objects.all()
       jury=False
       mydocs=[]
       for emp in employe: 
          if (emp.compte==request.user):
                 this_emp=emp
                 roles=this_emp.role.all()
                 for role in roles:
                        if (role.nom=='JURY'):
                                jury=True
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
                        'doctorants':mydocs
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
                        'doctorants':mydocs
                        })
       else : 
          return render(request,'gestion_FD/fiches_evaluation_employee.html',context) 
              
         
def valider_eval(request):
    
   employe=Employe.objects.all()
   cs=False
   for emp in employe: 
          if (emp.compte==request.user):
                 this_emp=emp
                 roles=this_emp.role.all()
                 for role in roles:
                        if (role.nom=='CS'):
                                cs=True
   fiches_nouvelles=Fiche_evaluation.objects.filter(valide__isnull=True).order_by('-date_eval')
   archive=Fiche_evaluation.objects.filter(valide__isnull=False).order_by('-date_eval')
   context={
        'cs':cs,
         'new': fiches_nouvelles,
         'archive': archive
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
             'archive' : Fiche_evaluation.objects.filter(valide__isnull=False).order_by('-date_eval')
          }
          return render(request,'gestion_FD/valider_evaluation.html', context2 )   
   else :
          return render(request,'gestion_FD/valider_evaluation.html',context)
          
def notes_prof(request):
 employe=Employe.objects.all()
 for emp in employe: 
          if (emp.compte==request.user):
                 this_emp=emp
 modules=Module.objects.filter(prof=this_emp)
 mydocs=[]
 for m in modules:
        docs=m.etudiants.all()
        for d in docs:
               mydocs.append(d)
 mydocs= list(dict.fromkeys(mydocs))
 evals=Eval_module.objects.filter(module__in=modules,etudiant__in=mydocs).order_by('module')
 
 context={'modules': modules, 'evals':evals}
 if request.method == 'POST' :
        if request.POST.get('modif') :
               id_eval=request.POST['id_eval']
               modif=request.POST['modif']
               Eval_module.objects.filter(id=id_eval).update(Note=modif)
               evals2=Eval_module.objects.filter(module__in=modules,etudiant__in=mydocs).order_by('module')
               return render(request,'gestion_FD/notes_prof.html',{'modules':modules,'evals': evals2})
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
                           'evals' : evals
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