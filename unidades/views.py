# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader, RequestContext
from django.views.generic import ListView
from unidades.forms import SolicitudPrivilegioForm
from unidades.models import SolicitudPrivilegio
from unidades.models import Unidad

@login_required(redirect_field_name='/')
def solicitud_privilegio(request):
  if request.method == "GET":
    return render_to_response("/unidades/solicitud_privilegio.html", {'SolicitudPrivilegioForm': SolicitudPrivilegioForm()},
		      context_instance=RequestContext(request))
  elif request.method == "POST":
            form = SolicitudPrivilegioForm(request.POST)
            if form.is_valid():
                u = request.user
                e = SolicitudPrivilegio(solicitante=u,
                        privilegio = form.cleaned_data['privilegio'],
                        unidad = form.cleaned_data['unidad'],
                        mensaje= form.cleaned_data['mensaje'])
                e.save()
                return render_to_response("/unidades/solicitud_privilegio.html", {'msg': "Solicitud realizada con exito",'SolicitudPrivilegioForm':SolicitudPrivilegioForm()}, 
                                              context_instance=RequestContext(request))
            else:
                return render_to_response("/unidades/solicitud_privilegio.html", {'SolicitudPrivilegioForm': form},
		      context_instance=RequestContext(request))
                
                
@login_required(redirect_field_name='/')
def otorgar_privilegio(request):
    unidadesMiembro= Unidad.objects.filter(miembros=request.user)
    unidadesResponsable = Unidad.objects.filter(responsable=request.user)
        #lista de los privilegios que qieren ser miembros
    listaMiembro=SolicitudPrivilegio.objects.none()
        #lista de los privilegios que quieren ser solicitantes
    listaPrivilegios=SolicitudPrivilegio.objects.none()
    for b in unidadesResponsable:
            listaMiembro = listaMiembro|SolicitudPrivilegio.objects.filter(unidad=b, privilegio='Miembro de Unidad', estado='En espera')
    for a in unidadesMiembro:
            listaPrivilegios=listaPrivilegios|SolicitudPrivilegio.objects.filter(unidad=a, privilegio='Solicitante', estado='En espera')
    if request.method == "GET":
        return render_to_response("/unidades/otorgar_privilegio.html",{'listaPrivilegios':listaPrivilegios, 'listaMiembro':listaMiembro}, context_instance=RequestContext(request))
    elif request.method =="POST":
        form = SolicitudPrivilegioForm()
        if 'aceptar_privilegio' in request.POST:
                priv= SolicitudPrivilegio.objects.get(id= request.POST['id'])# Este id lo puse porque no se como obtener el de la solicitud por probar
                priv.estado= 'Aceptado'
                priv.save()
                unidad= Unidad.objects.get(id=priv.unidad.id)
                if priv.privilegio == "Miembro de Unidad":
                    unidad.miembros.add(priv.solicitante)
                elif priv.privilegio == "Solicitante":
                    pass
                    #Falta agregar los solicitantes de una unidad en el modelo
                    #unidad.solicitantes.add(priv.solicitante)
                
                listaMiembro=SolicitudPrivilegio.objects.none()
        #lista de los privilegios que quieren ser solicitantes
                listaPrivilegios=SolicitudPrivilegio.objects.none()
                for b in unidadesResponsable:
                    listaMiembro = listaMiembro|SolicitudPrivilegio.objects.filter(unidad=b, privilegio='Miembro de Unidad', estado='En espera')
                for a in unidadesMiembro:
                    listaPrivilegios=listaPrivilegios|SolicitudPrivilegio.objects.filter(unidad=a, privilegio='Solicitante', estado='En espera')
                
                return render_to_response("/unidades/otorgar_privilegio.html", {'msg': "Solicitud aceptada",'listaPrivilegios':listaPrivilegios, 'listaMiembro':listaMiembro}, 
                                              context_instance=RequestContext(request))
                
        elif 'negar_privilegio' in request.POST:
                priv= SolicitudPrivilegio.objects.get(id=1)# Este id lo puse porque no se como obtener el de la solicitud
                priv.estado= 'Aceptado'
                priv.save()
                listaMiembro=SolicitudPrivilegio.objects.none()
        #lista de los privilegios que quieren ser solicitantes
                listaPrivilegios=SolicitudPrivilegio.objects.none()
                for b in unidadesResponsable:
                    listaMiembro = listaMiembro|SolicitudPrivilegio.objects.filter(unidad=b, privilegio='Miembro de Unidad', estado='En espera')
                for a in unidadesMiembro:
                    listaPrivilegios=listaPrivilegios|SolicitudPrivilegio.objects.filter(unidad=a, privilegio='Solicitante', estado='En espera')
                return render_to_response("/unidades/otorgar_privilegio.html", {'msg': "Solicitud cancelada",'listaPrivilegios':listaPrivilegios, 'listaMiembro':listaMiembro}, 
                                              context_instance=RequestContext(request))
