from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Doctorant,User,Employe,Etat_avancement,PieceJointe,These,Role
from django.contrib import messages
from django.template import RequestContext, context
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import  User,auth
from .forms import LoginForm
from datetime import date, datetime

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

def lister_theses(request):
   employe=Employe.objects.all()
   doctorants=Doctorant.objects.all()
   doc_name="ll"
   cfd=False
  
   for emp in employe: 
          if (emp.compte==request.user):
                 this_emp=emp
                 roles=this_emp.role.all()
                 for role in roles:
                        if (role.nom=='CFD'):
                                cfd=True

   # theses_prise = These.objects.filter(prise=True)
   theses = []
   for doc in doctorants:
      for t in doc.choix.all(): 
        if (t.prise):
           
           doc_name=doc.nom
           theses.append(t)

   context ={
      'CFD':cfd,
      'theses':theses,
      'nom_doc':doc_name,
   }
   if request.method == 'POST':
      id_these = request.POST['id_th']
      if request.POST.get('accept'):
         These.objects.filter(id=id_these).update(valide_cfd=True)
      else :
         These.objects.filter(id=id_these).update(valide_cfd=False)
      context2 ={
         'CFD':cfd,
         'theses':theses,
         'nom_doc':doc_name,
      }
      return render(request,'gestion_Fd/liste_theses.html',context2)
   else:
      return render(request,'gestion_Fd/liste_theses.html',context)
      

   
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

def try_t(request):
   doctorants=Doctorant.objects.all()
   doc_name=""
   doc_prenom=""

   theses = []
   for doc in doctorants:
      for t in doc.choix.all(): 
        if (t.prise):
           
           doc_name=doc.nom
           doc_prenom = doc.prenom
           theses.append(t)
   context ={
      'theses':theses,
      'nom_doc':doc_name,
      'prenom_doc':doc_prenom,
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
      }
      return render(request,'gestion_FD/advanced_table.html',context2)
   else:
      return render(request,'gestion_FD/advanced_table.html',context)
   

def logout(request):
   auth.logout(request)
   return redirect('login')
