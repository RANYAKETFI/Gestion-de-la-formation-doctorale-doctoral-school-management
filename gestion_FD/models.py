from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User

class PieceJointe(models.Model):
    TYPES= (
     ('PDF','PDF')
     ,('EXCEL','EXCEL'),
     ('IMAGE','IMAGE'),
     ('LIEN','LIEN'))
    lien=models.FileField(null=True)
    type_piece=models.CharField(max_length=40,choices=TYPES)
class Dossier_Doctorant(models.Model):
    pieces=models.ManyToManyField(PieceJointe)


class Doctorant(models.Model):
    SEXES= (('F','F'),('M','M'))
    LABOS=(('MCS','MCS'),('LCSI','LCSI'))
    matricule=models.IntegerField()
    nom =models.CharField(max_length=100,default='SOME STRING')
    prenom =models.CharField(max_length=100,default='SOME STRING')
    email=models.EmailField(default='')	
    date_inscription=models.DateField(default=datetime.now())
    date_naissance=models.DateField(default=datetime.now())
    wilaya_naissance=models.CharField(max_length=30)
    sexe=models.CharField(max_length=1,choices=SEXES)
    classement_concours=models.IntegerField(default=1)
    annee_etude=models.IntegerField(default=1)
    inscrit=models.BooleanField(default=False)
    reinscrit=models.BooleanField(default=False)
    delibere=models.BooleanField(default=False)
    date_deliberation=models.DateField(default=datetime.now())
    date_reinscription=models.DateField(default=datetime.now())
    dossier=models.ForeignKey(Dossier_Doctorant,on_delete=models.CASCADE,default=1)
    compte=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    nom_lab=models.CharField(max_length=20,choices=LABOS) 
    #choix_theses=models.ManyToManyField(These)

class Role(models.Model):
    ROLES=(('CS','CS'),('CFD','CFD'),('JURY','JURY'),('PROF','PROF'),('DT','DT'),('ADPGR','ADPGR'),('DAPGR','DAPGR'))
    nom=models.CharField(max_length=100,choices=ROLES)


class Employe(models.Model):
    SEXES= (('F','F'),('M','M'))
    LABOS=(('MCS','MCS'),('LCSI','LCSI'))
    nom =models.CharField(max_length=100)
    prenom =models.CharField(max_length=100)
    email=models.EmailField()	
    date_naissance=models.DateField(default=datetime.now())
    sexe=models.CharField(max_length=1,choices=SEXES)
    compte=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    nom_lab=models.CharField(max_length=20,choices=LABOS) 
    role=models.ManyToManyField(Role)    
class These(models.Model):
    intitule=models.CharField(max_length=100)
    resume=models.TextField()
    valide_cfd=models.BooleanField(default=False)
    prise=models.BooleanField(default=False)
    dt=models.ManyToManyField(Employe)
    doctorant=models.ForeignKey(Doctorant,on_delete=models.CASCADE,default=None, null=True)
    date=models.DateField(default=None, null=True)
class Etat_avancement(models.Model):
    date_etat_avancement=models.DateField() 
    doctorant=models.ForeignKey(Doctorant,on_delete=models.CASCADE)
    etat=models.ForeignKey(PieceJointe,on_delete=models.CASCADE)


class Fiche_evaluation(models.Model):
    date_eval=models.DateField(default=datetime.now())
    fichier=models.ForeignKey(PieceJointe,on_delete=models.CASCADE)
    jury=models.ManyToManyField(Employe)
    valide=models.BooleanField(default=False)
    doctorant=models.ForeignKey(Doctorant,on_delete=models.CASCADE,default=1)
    

class Reunion(models.Model):
    date_reun=models.DateField()
    heure=models.DateTimeField()
    descriptif=models.TextField()  
    doctorant=models.ForeignKey(Doctorant,on_delete=models.CASCADE,default=1)  
    dt=models.ForeignKey(Employe,on_delete=models.CASCADE,default=1) 
class Eval_module(models.Model):
    Note=models.IntegerField(default=0)
    date_eval=models.DateField(default=datetime.now())
    etudiant=models.ForeignKey(Doctorant,on_delete=models.CASCADE,default=1)
   #piece=models.ForeignKey(PieceJointe,on_delete=models.CASCADE,default=1)
class Module(models.Model):
    nom=models.CharField(max_length=50)
    prof=models.ForeignKey(Employe,on_delete=models.CASCADE,default=1)
    etudiants=models.ManyToManyField(Doctorant)
    credit=models.IntegerField(default=0)
    evaluation=models.ManyToManyField(Eval_module)

class PV(models.Model):
    date_pv=models.DateField(default=datetime.now())
    redacteur=models.ForeignKey(Employe,on_delete=models.CASCADE,default=1)    
    piece =models.ForeignKey(PieceJointe,on_delete=models.CASCADE,default=1)
