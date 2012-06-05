from django.forms.models import ModelForm
from django import forms
from flujos.models import Flujo, Paso, Campo

class CrearFlujoForm(ModelForm): #esto quiere decir que se extiende a ModelForm
    class Meta:
        model = Flujo
        exclude = ('unidad', 'estado')

        
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
		 
		


#class CopiarFlujoForm()
#=======
#class AgregarPasoForm(ModelForm):
#    class Meta:
#        model = Paso
# 
#    
#>>>>>>> 27032f4d98f0d01a76cb0f3046b40806a2eb017e

