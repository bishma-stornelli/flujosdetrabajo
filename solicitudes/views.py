# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

@login_required
def listar_solicitudes(request):
     return render_to_response('solicitudes/listar_solicitudes.html')

@login_required
def consultar_solicitud(request, solicitud_id):
     return render_to_response('solicitudes/consultar_solicitud.html')
