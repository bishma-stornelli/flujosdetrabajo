# Create your views here.
from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from unidades.forms import SolicitudPrivilegioForm
from unidades.models import SolicitudPrivilegio

@login_required(redirect_field_name='/')
def solicitudPrivilegio(request):
  if request.method == "GET":
    return render_to_response("solicitudPrivilegio.html", {'SolicitudPrivilegioForm': SolicitudPrivilegioForm()},
		      context_instance=RequestContext(request))
  elif request.method == "POST":
            form = SolicitudPrivilegioForm(request.POST)
            if form.is_valid():
                u = request.user
                e = SolicitudPrivilegio(solicitante=u,
                        privilegio = form.cleaned_data['privilegio'],
                        unidad = form.cleaned_data['unidad'])
                e.save()
                return render_to_response("solicitudPrivilegio.html", {'msg': "Solicitud realizada con exito",'SolicitudPrivilegioForm':SolicitudPrivilegioForm()}, 
                                              context_instance=RequestContext(request))
            else:
                return render_to_response("solicitudPrivilegio.html", {'SolicitudPrivilegioForm': form},
		      context_instance=RequestContext(request))
	
