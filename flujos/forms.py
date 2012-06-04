from django.forms.models import ModelForm
from flujos.models import Flujo, Paso

class CrearFlujoForm(ModelForm): #esto quiere decir que se extiende a ModelForm
    class Meta:
        model = Flujo
        exclude = ('unidad', 'estado')


#class CopiarFlujoForm()
#class AgregarPasoForm(ModelForm):
#    class Meta:
#        model = Paso
