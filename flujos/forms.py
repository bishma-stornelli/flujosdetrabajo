from django import forms
from django.forms.models import ModelForm
from django.forms.util import ErrorList
from flujos.models import Criterio, Flujo, Campo, Paso, Alerta, Informe
import re
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from array import *

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
        
class AlertaForm(ModelForm):
    class Meta:
        model= Alerta
        fields=('paso','nombre','mostar_al_llegar','miembro_es_receptor','solicitante_es_receptor','tipos','formato')
        widgets = {
                   'paso': forms.HiddenInput()
        }
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, 
        initial=None, error_class=ErrorList, label_suffix=':', 
        empty_permitted=False, instance=None, paso = None):
        ModelForm.__init__(self, data=data, files=files, auto_id=auto_id, prefix=prefix, initial=initial, error_class=error_class, label_suffix=label_suffix, empty_permitted=empty_permitted, instance=instance)
        self.fields['paso'].choices = (paso.id, paso.nombre)
        self.fields['paso'].initial = paso.id
      
    def clean_formato(self):
        data = self.cleaned_data['formato']
        if (validar_format(data,self)):
            return data  
        else:
            raise forms.ValidationError("Formato ingresado no valido")
    
    def is_valid(self):
        return ModelForm.is_valid(self)
        
class InformeForm(ModelForm):
    class Meta:
        model= Informe
        fields = ('paso','nombre','miembro_es_receptor','solicitante_es_receptor','formato')
        widgets = {
                   'paso': forms.HiddenInput()
        }
        
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, 
        initial=None, error_class=ErrorList, label_suffix=':', 
        empty_permitted=False, instance=None, paso = None):
        ModelForm.__init__(self, data=data, files=files, auto_id=auto_id, prefix=prefix, initial=initial, error_class=error_class, label_suffix=label_suffix, empty_permitted=empty_permitted, instance=instance)
        self.fields['paso'].choices = (paso.id, paso.nombre)
        self.fields['paso'].initial = paso.id
    
    def clean_formato(self):
        data = self.cleaned_data['formato']
        if (validar_format(data,self)):
            return data  
        else:
            raise forms.ValidationError("Formato ingresado no valido")
        
    def is_valid(self):
        return ModelForm.is_valid(self)

# Dada la lista de campos un paso se busca si esta tiene el campo a buscar
def existe_campo(campos,campo_buscado):
    for campo in campos:
        if(campo.nombre == campo_buscado):
            return True
    return False

# Se verifica si todos los campos que se declaran en el formato
# referencian o no a campos de pasos anteriores
def validar_format(formato,a):
    valido=False
    predecesores=[]
    campos_formato = re.findall(r'(\${(\w+)(([.](\w+))?)})', formato)
    print("formato: "+formato)
    
    for campo_f in campos_formato:   
        # en campo[1] esta el atrubuto y en campo[4] lo q va despues del . (solicitante.nombre) 
        paso = a.cleaned_data['paso']
        paso = get_object_or_404(Paso, pk=paso.id)
                               
        if((campo_f[1]=="solicitante" and (campo_f[4]=="" or campo_f[4]=="email")) or campo_f[1]=="unidad" ):
            valido=True
        else:                       
            valido=existe_campo(paso.campos.all(),campo_f[1])
            if (valido):
                break 
            else:
                predecesores.append(paso.predecesores.all())               
            if(not valido):
                i=0
                tam=len(predecesores)
                while(i<tam and not valido):
                    for pred in predecesores[i]: 
                        valido=existe_campo(pred.campos.all(),campo_f[1])
                        if (valido):
                            break
                        predecesores.append(pred.predecesores.all())
                    tam=len(predecesores)
                    i=i+1
        if(valido):
            break  
    return valido
    
    #return re.match("^([^$]*(\${\w+(([.]\w+)?)})*)*$",formato)
    #return re.match("^([^$]*(\${.*})*)*$",formato)
    #return re.match("^([\s\w\d]*(\${.*})*)*$",formato)
    #return re.match("[\s\w\d]*([^(\${.*})])",formato)
    #return re.match("(\${.*})",formato)


