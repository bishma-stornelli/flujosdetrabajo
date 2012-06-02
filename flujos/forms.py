from django.forms.models import ModelForm
from flujos.models import Flujo

class CrearFlujoForm(ModelForm): #esto quiere decir que se extiende a ModelForm
    class Meta:
        model = Flujo
        exclude = ('unidad', 'estado')