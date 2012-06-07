from unidades.models import SolicitudPrivilegio
from unidades.models import Unidad
from django.forms import ModelForm
from django.db import models
from django.forms import TextInput

class SolicitudPrivilegioForm(ModelForm):
    
    class Meta:
        model = SolicitudPrivilegio
        fields = ('mensaje', 'unidad', 'privilegio',)

	exclude = ('estado','fecha','solicitante')

class RegistroUnidadForm(ModelForm):
    
    class Meta:
        model = Unidad
        fields = ('nombre','descripcion',)
        
class ConfigurarUnidadForm(ModelForm):
  
    class Meta:
        model = Unidad
        fields = ('nombre','descripcion','auto_aceptar')
        widgets = {
            'nombre': TextInput(attrs={'readonly':'readonly'}),
        }
        #fields['nombre'].widget.attrs['readonly'] = True
       
    
