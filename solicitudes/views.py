# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from solicitudes.models import Solicitud
from unidades.models import SolicitudPrivilegio

@login_required
def listar_solicitudes(request):
    #Obtiene las solicitudes en las que el usuario es el solicitante.
    solicitudes = Solicitud.objects.filter(solicitantes=request.user)
    #Envia todas las solicitudes que coincidan a la vista. 
    return render_to_response('solicitudes/listar_solicitudes.html', {'solicitudes':solicitudes},context_instance=RequestContext(request))

@login_required
def consultar_solicitud(request, solicitud_id):
     solicitud = get_object_or_404(Solicitud, id = solicitud_id, solicitantes=request.user)
     actuales = solicitud.registros.filter(estado=2)
     completados = solicitud.registros.filter(estado=1).order_by('fecha_de_salida')
     por_hacer = set([])
     pila = list(actuales)
     
     
     while pila !=[]:
        aux = pila.pop()
        pila.extend(aux.paso.sucesores.all())
        por_hacer.add(aux)
        
        
     if solicitud.flujo.unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
        responsable = True
     else:
        responsable = False
     


     
     return render_to_response('solicitudes/consultar_solicitud.html', {'solicitud':solicitud, 'actuales':actuales, 'completados':completados, 'por_hacer':por_hacer, 'responsable':responsable}, context_instance=RequestContext(request))

@login_required
def crear_solicitud(request):
     return render_to_response('solicitudes/crear_solicitud.html')

@login_required
def agregar_dato(request):
     return render_to_response('solicitudes/agregar_dato.html')

@login_required
def completar_dato(request):
     return render_to_response('solicitudes/completar_dato.html')

@login_required
def avanzar_solicitud(request):
     return render_to_response('solicitudes/avanzar_solicitud.html')

@login_required
def retirar_solicitud(request):
     return render_to_response('solicitudes/retirar_solicitud.html')

@login_required
def generar_informe(request):
     return render_to_response('solicitudes/generar_informe.html')
