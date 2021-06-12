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

class Bourse(models.Model):
    duree=models.IntegerField()
    types_bourse= (('PNE','PNE'),('PROFAS','PROFAS'),('Autres','Autre'))
    type_bourse=models.CharField(max_length=100,choices=types_bourse)
class Role(models.Model):
    ROLES=(('CS','CS'),('CFD','CFD'),('JURY','JURY'),('PROF','PROF'),('DT','DT'),('ADPGR','ADPGR'),('DAPGR','DAPGR'))
    nom=models.CharField(max_length=100,choices=ROLES)
    def __str__(self):
     return self.nom

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
    co_tut=models.BooleanField(default=False)    
    
class These(models.Model):
    intitule=models.CharField(max_length=100)
    resume=models.TextField()
    valide_cfd=models.BooleanField(default=False)
    prise=models.BooleanField(default=False)
    dt=models.ManyToManyField(Employe)
    date=models.DateField(default=None,null=True)
    etab_part=models.CharField(max_length=100,default=None)    
class Reinscription(models.Model):
    date_reinscription=models.DateField(default=datetime.now())
    declarations= (('le doctorant accuse un retard important dans ses travaux','le doctorant accuse un retard important dans ses travaux'),('le doctorant accuse un retard peu important dans ses travaux','le doctorant accuse un retard peu important dans ses travaux'),('les travaux du doctorant avancent conformément à l’échéancier établi','les travaux du doctorant avancent conformément à l’échéancier établi'))
    declaration=models.CharField(max_length=100,choices=declarations)
    avis=models.BooleanField(default=False)
    valide_cfd=models.BooleanField(null=True)
    valide_dt=models.BooleanField(default=False)
    valide_cs=models.BooleanField(null=True)
    prof=models.ManyToManyField(Employe)
    dt=models.BooleanField(default=None)

class Doctorant(models.Model):
    SEXES= (('F','F'),('M','M'))
    LABOS=(('MCS','MCS'),('LCSI','LCSI'))
    matricule=models.IntegerField()
    nom =models.CharField(max_length=100,default='SOME STRING')
    prenom =models.CharField(max_length=100,default='SOME STRING')
    adresse =models.CharField(max_length=100,default='SOME STRING')
    situation_familiale=models.CharField(max_length=100,default='SOME STRING')
    profession =models.CharField(max_length=100,default='SOME STRING')
    employeur =models.CharField(max_length=100,default='SOME STRING')
    telephone =models.CharField(max_length=100,default='00')
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
    dossier=models.ForeignKey(Dossier_Doctorant,on_delete=models.CASCADE,null=True,blank=True)
    compte=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    nom_lab=models.CharField(max_length=20,choices=LABOS) 
    choix=models.ManyToManyField(These,null=True,blank=True)
    Bourse=models.ForeignKey(Bourse,on_delete=models.CASCADE,blank=True,null=True)
    reinscription=models.ManyToManyField(Reinscription,null=True,blank=True)
    choixfinal =models.CharField(max_length=100,default='Pas Encore')
    rein_envo=models.BooleanField(default=False)
class Etat_avancement(models.Model):
    date_etat_avancement=models.DateField() 
    doctorant=models.ForeignKey(Doctorant,on_delete=models.CASCADE)
    etat=models.ForeignKey(PieceJointe,on_delete=models.CASCADE)

class Presentation(models.Model):
    date_pres=models.DateField(default=datetime.now())
    doctorant=models.ForeignKey(Doctorant,on_delete=models.CASCADE,default=1)
    jury=models.ManyToManyField(Employe)
    heure_debut=models.TimeField()
    heure_fin=models.TimeField()
class Fiche_evaluation(models.Model):
    date_eval=models.DateField(default=datetime.now())
    fichier=models.ForeignKey(PieceJointe,on_delete=models.CASCADE)
    jury=models.ManyToManyField(Employe)
    valide=models.BooleanField(null=True)
    doctorant=models.ForeignKey(Doctorant,on_delete=models.CASCADE,default=1)

class Reunion(models.Model):
    date_reun=models.DateField()
    heure=models.DateTimeField()
    descriptif=models.TextField()  
    doctorant=models.ForeignKey(Doctorant,on_delete=models.CASCADE,default=1)  
    dt=models.ForeignKey(Employe,on_delete=models.CASCADE,default=1) 
class Module(models.Model):
    nom=models.CharField(max_length=50)
    prof=models.ForeignKey(Employe,on_delete=models.CASCADE,default=1)
    etudiants=models.ManyToManyField(Doctorant)
    credit=models.IntegerField(default=0)
    
class Eval_module(models.Model):
    Note=models.IntegerField(default=0)
    date_eval=models.DateField(default=datetime.now())
    etudiant=models.ForeignKey(Doctorant,on_delete=models.CASCADE,default=1)
    module=models.ForeignKey(Module,on_delete=models.CASCADE,default=1)
    appreciation=models.TextField(default='')  
    type=models.TextField(default='')


