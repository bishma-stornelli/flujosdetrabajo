# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from solicitudes.models import Solicitud
from unidades.models import Unidad
from flujos.models import Flujo

@login_required
def listar_solicitudes(request):
    #Obtiene las solicitudes en las que el usuario es el solicitante.
    solicitudes_solicitante = Solicitud.objects.filter(solicitantes=request.user).order_by('fecha_de_solicitud')
    unidades = Unidad.objects.filter(miembros=request.user)
    solicitudes_miembro=Solicitud.objects.none()
    for u in unidades:
        flujos= Flujo.objects.filter(unidad = u)
        for f in flujos:
            solicitudes_miembro= solicitudes_miembro | Solicitud.objects.filter(flujo=f)
            solicitudes_miembro=solicitudes_miembro.order_by('fecha_de_solicitud')
    #Envia todas las solicitudes que coincidan a la vista. 
    return render_to_response('solicitudes/listar_solicitudes.html', {'solicitudes_solicitante':solicitudes_solicitante, 'solicitudes_miembro':solicitudes_miembro},context_instance=RequestContext(request))

@login_required
def consultar_solicitud(request, solicitud_id):
     return render_to_response('solicitudes/consultar_solicitud.html')

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
