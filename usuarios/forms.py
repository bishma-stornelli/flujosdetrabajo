from django import forms
from models import PerfilDeUsuario
from django.contrib.auth.models import User

class RegistroForm(forms.Form):
	username = forms.CharField(max_length=20)
	nombre = forms.CharField(max_length=20)
	apellido = forms.CharField(max_length=20)
	dni = forms.CharField(max_length=10)
	clave = forms.CharField(min_length=5, max_length=20, widget=forms.PasswordInput)
	confirm = forms.CharField(min_length=5,max_length=20, widget=forms.PasswordInput)
	email = forms.EmailField()

class LoginForm(forms.Form):
	username = forms.CharField(max_length=20)
	clave = forms.CharField(max_length=20, widget=forms.PasswordInput)
	
class UserForm(forms.ModelForm):
	username = forms.CharField (widget=forms.TextInput(attrs={'readonly':'readonly'}))
	first_name = forms.CharField(max_length=20, label='Nombre')
	last_name = forms.CharField(max_length=20, label='Apellido')
	email = forms.EmailField()
	
