from django.forms.models import ModelForm
from flujos.models import Flujo, Paso

class CrearFlujoForm(ModelForm): #esto quiere decir que se extiende a ModelForm
    class Meta:
        model = Flujo
        exclude = ('unidad', 'estado')



class ModificarPasoForm(ModelForm):
	class Meta:
		model = Paso
		fields= ('nombre', 'tipo', 'descripcion') 
		
    
class ModificarFlujoForm(ModelForm):
	class Meta:
		model = Paso
		fields= ('nombre', 'tipo', 'descripcion')
		 
		

#class CopiarFlujoForm()
#class AgregarPasoForm(ModelForm):
#    class Meta:
#        model = Paso
