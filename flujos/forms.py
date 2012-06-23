from django import forms
from django.forms.models import ModelForm
from django.forms.util import ErrorList
from flujos.models import Criterio, Flujo, Campo, Paso, Alerta, Informe

class AgregarCaminoForm(ModelForm): #esto quiere decir que se extiende a ModelForm
    class Meta:
        model = Criterio
        exclude = ('campos')

class CrearFlujoForm(ModelForm): #esto quiere decir que se extiende a ModelForm
    class Meta:
        model = Flujo
        exclude = ('estado',)
    
    # Sobreescrito el constructor para anadir el parametro usuario para poder limitar las unidades
    # a las unidades que el usuario es responsable
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, 
        initial=None, error_class=ErrorList, label_suffix=':', 
        empty_permitted=False, instance=None, usuario=None):
        ModelForm.__init__(self, data=data, files=files, auto_id=auto_id, prefix=prefix, initial=initial, error_class=error_class, label_suffix=label_suffix, empty_permitted=empty_permitted, instance=instance)
        unidades = [(0, "------------")]
        for unidad in usuario.unidades_responsable.all():
            unidades.append( (unidad.id,unidad.nombre) )
        self.fields['unidad'].choices = unidades

class AgregarCampoForm(forms.Form):
    nombre= forms.CharField(max_length=20, label="Nombre")
    tipo = forms.ChoiceField(choices=Campo.TIPO_CHOICES, label="Tipo")
    #responsable = forms.ChoiceField(choices=Campo.TIPO_CHOICES2, label="Responsable")
    esObligatorio = forms.BooleanField(label="Obligatorio", initial=False, required=False)
    

class ModificarPasoForm(ModelForm):
    class Meta:
        model = Paso
        fields= ('nombre', 'tipo', 'descripcion') 
        
    
class ModificarFlujoForm(ModelForm):
    class Meta:
        model = Flujo
        fields= ('nombre',  'descripcion')
         
        
class CopiarFlujoForm(ModelForm):
    class meta:
        model = Paso
        fields = ('nombre')

class AgregarPasoForm(ModelForm):
    class Meta:
        model = Paso
        fields=('nombre', 'tipo', 'descripcion', 'flujo')
        widgets = {
                   'flujo': forms.HiddenInput()
        }
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, 
        initial=None, error_class=ErrorList, label_suffix=':', 
        empty_permitted=False, instance=None, flujo = None):
        ModelForm.__init__(self, data=data, files=files, auto_id=auto_id, prefix=prefix, initial=initial, error_class=error_class, label_suffix=label_suffix, empty_permitted=empty_permitted, instance=instance)
        self.fields['flujo'].choices = (flujo.id, flujo.nombre,)
        self.fields['flujo'].initial = flujo.id


class CampoForm(ModelForm):
    class Meta:
        model = Campo
        exclude = ('paso')
        
class AgregarAlertaForm(ModelForm):
    class Meta:
        model= Alerta
        fields=('paso','descripcion','mostar_al_llegar','plantilla','miembro_es_receptor','solicitante_es_receptor','tipos')
        widgets = {
                   'paso': forms.HiddenInput()
        }
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, 
        initial=None, error_class=ErrorList, label_suffix=':', 
        empty_permitted=False, instance=None, paso = None):
        ModelForm.__init__(self, data=data, files=files, auto_id=auto_id, prefix=prefix, initial=initial, error_class=error_class, label_suffix=label_suffix, empty_permitted=empty_permitted, instance=instance)
        self.fields['paso'].choices = (paso.id, paso.nombre)
        self.fields['paso'].initial = paso.id
        
class AgregarInformeForm(ModelForm):
    class Meta:
        model= Informe
        fields = ('paso','descripcion','plantilla','miembro_es_receptor','solicitante_es_receptor')
        widgets = {
                   'paso': forms.HiddenInput()
        }
        
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, 
        initial=None, error_class=ErrorList, label_suffix=':', 
        empty_permitted=False, instance=None, paso = None):
        ModelForm.__init__(self, data=data, files=files, auto_id=auto_id, prefix=prefix, initial=initial, error_class=error_class, label_suffix=label_suffix, empty_permitted=empty_permitted, instance=instance)
        self.fields['paso'].choices = (paso.id, paso.nombre)
        self.fields['paso'].initial = paso.id
