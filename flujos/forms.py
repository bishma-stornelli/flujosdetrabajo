from django.forms.models import ModelForm
from django import forms
from flujos.models import Flujo, Paso, Campo, Criterio

class AgregarCaminoForm(ModelForm): #esto quiere decir que se extiende a ModelForm
    class Meta:
        model = Criterio
        exclude = ('campos')

class CrearFlujoForm(ModelForm): #esto quiere decir que se extiende a ModelForm
    class Meta:
        model = Flujo
        exclude = ('estado',)

class AgregarCampoForm(forms.Form):
    nombre= forms.CharField(max_length=20, label="Nombre")
    tipo = forms.ChoiceField(choices=Campo.TIPO_CHOICES, label="Tipo")
    esObligatorio = forms.BooleanField(label="Obligatorio")
    
    

class ModificarPasoForm(ModelForm):
	class Meta:
		model = Paso
		fields= ('nombre', 'tipo', 'descripcion') 
		
    
class ModificarFlujoForm(ModelForm):
	class Meta:
		model = Paso
		fields= ('nombre', 'tipo', 'descripcion')
		 
		


class CopiarFlujoForm(ModelForm):
    class meta:
        model = Paso
        fields = ('nombre')


class AgregarPasoForm(ModelForm):
    class Meta:
        model = Paso
        fields=('nombre', 'tipo', 'descripcion') 
