from django import forms

class LoginForm(forms.Form):
    nom = forms.CharField(label='Your name', max_length=100)
    mdp= forms.CharField(max_length=100)