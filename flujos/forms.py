from django.forms.models import ModelForm
from flujos.models import Flujo, Paso

class CrearFlujoForm(ModelForm): #esto quiere decir que se extiende a ModelForm
    class Meta:
        model = Flujo
        exclude = ('unidad', 'estado')

#<<<<<<< HEAD
#class CopiarFlujoForm()
#=======
#class AgregarPasoForm(ModelForm):
#    class Meta:
#        model = Paso
 
    
#>>>>>>> 27032f4d98f0d01a76cb0f3046b40806a2eb017e
