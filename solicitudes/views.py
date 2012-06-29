# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from solicitudes.models import Solicitud
from flujos.models import Flujo
from unidades.models import SolicitudPrivilegio

@login_required
def listar_solicitudes(request):
    #Obtiene las solicitudes en las que el usuario es el solicitante.
    solicitudes = Solicitud.objects.filter(solicitante=request.user)
    #Envia todas las solicitudes que coincidan a la vista. 
    return render_to_response('solicitudes/listar_solicitudes.html', {'solicitudes':solicitudes},context_instance=RequestContext(request))

@login_required
def consultar_solicitud(request, solicitud_id):
     return render_to_response('solicitudes/consultar_solicitud.html')

@login_required
def crear_solicitud(request, flujo_id):
	flujo = get_object_or_404(Flujo, pk=flujo_id)
	if not flujo.unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_SOLICITANTE):
		messages.error(request,"Solo los solicitantes de unidad pueden crear una solicitud.")
		return HttpResponseRedirect(reverse("flujo_index"))

	solicitud = Solicitud(flujo=flujo, solicitante=request.user)
	solicitud.save()
	messages.success( request , "Registro de solicitud exitoso.")
	return HttpResponseRedirect(reverse("flujo_index"))

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
