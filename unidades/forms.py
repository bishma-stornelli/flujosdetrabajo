from unidades.models import SolicitudPrivilegio
from django.forms import ModelForm
from django.db import models

class SolicitudPrivilegioForm(ModelForm):
    
    class Meta:
        model = SolicitudPrivilegio

	exclude = ('estado','fecha','solicitante',)
