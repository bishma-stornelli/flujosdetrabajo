from unidades.models import SolicitudPrivilegio
from unidades.models import Unidad
from django.forms import ModelForm
from django.db import models

class SolicitudPrivilegioForm(ModelForm):
    
    class Meta:
        model = SolicitudPrivilegio

	exclude = ('estado','fecha','solicitante',)

class RegistroUnidadForm(ModelForm):
    
    class Meta:
        model = Unidad
        exclude = ('fecha','miembros','responsable','auto_aceptar',)
        
class ConfigurarUnidadForm(ModelForm):
  
    class Meta:
        model = Unidad
        fields = ('nombre','descripcion','auto_aceptar')
       
    