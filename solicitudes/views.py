# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from solicitudes.models import Solicitud, Registro

@login_required
def listar_solicitudes(request):
    #Obtiene las solicitudes en las que el usuario es el solicitante.
    solicitudes = Solicitud.objects.filter(solicitantes=request.user)
    #Envia todas las solicitudes que coincidan a la vista. 
    return render_to_response('solicitudes/listar_solicitudes.html', {'solicitudes':solicitudes},context_instance=RequestContext(request))

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
def retirar_solicitud(request,solicitud_id):
    solicitudes = get_object_or_404('Solicitud',pk=solicitud_id)
    if (solicitudes.solicitantes==request.user):
        registro = Registro.objects.filter(solicitud = solicitudes)
        registro.estado = Registro.ESTADO_RETIRADO
        registro.fecha_salida = datetime.datetime.now()
        registro.save()
        messages.success(request, "La Solicitud ha sido retirada")
    else:
        messages.error(request,"Error: Solo la persona que realizo la solicitud puede retirarla")
    return listar_solicitudes(request)

@login_required
def generar_informe(request):
     return render_to_response('solicitudes/generar_informe.html')
