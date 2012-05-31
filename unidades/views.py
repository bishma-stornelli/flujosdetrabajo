# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader, RequestContext
from unidades.forms import RegistroUnidadForm, SolicitudPrivilegioForm
from unidades.models import SolicitudPrivilegio, Unidad
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group, Permission

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
                        unidad = form.cleaned_data['unidad'],
                        mensaje= form.cleaned_data['mensaje'])
                e.save()
                return render_to_response("solicitudPrivilegio.html", {'msg': "Solicitud realizada con exito",'SolicitudPrivilegioForm':SolicitudPrivilegioForm()}, 
                                              context_instance=RequestContext(request))
            else:
                return render_to_response("solicitudPrivilegio.html", {'SolicitudPrivilegioForm': form},
		      context_instance=RequestContext(request))
     #dasdas          
                
@login_required(redirect_field_name='/')
def otorgarPrivilegio(request):
    miembro = get_object_or_404(Group, name='Miembro de Unidad')
    solicitante = get_object_or_404(Group, name='Solicitante')
    responsable = get_object_or_404(Group, name='Responsable de Unidad')
    unidadesMiembro= Unidad.objects.filter(miembros=request.user)
    unidadesResponsable = Unidad.objects.filter(responsable=request.user)
        #lista de los privilegios que qieren ser miembros
    listaMiembro=SolicitudPrivilegio.objects.none()
        #lista de los privilegios que quieren ser solicitantes
    listaPrivilegios=SolicitudPrivilegio.objects.none()
    #lista de los privilegios que quieren ser responsable
    listaResponsable=SolicitudPrivilegio.objects.none()
    for b in unidadesResponsable:
            listaMiembro = listaMiembro|SolicitudPrivilegio.objects.filter(unidad=b, privilegio=2, estado=1)
    for a in unidadesMiembro:
            listaPrivilegios=listaPrivilegios|SolicitudPrivilegio.objects.filter(unidad=a, privilegio=1, estado=1)
    if request.user.is_superuser:
            listaResponsable=listaResponsable|SolicitudPrivilegio.objects.filter(privilegio=3, estado=1)
    if request.method == "GET":
        return render_to_response("otorgarPrivilegio.html",{'listaPrivilegios':listaPrivilegios, 'listaMiembro':listaMiembro,'listaResponsable':listaResponsable}, context_instance=RequestContext(request))
    elif request.method =="POST":
        form = SolicitudPrivilegioForm()
        if 'aceptar_privilegio' in request.POST:
                priv= SolicitudPrivilegio.objects.get(id= request.POST['id'])# Este id lo puse porque no se como obtener el de la solicitud por probar
                priv.estado= 2
                priv.save()
                unidad= Unidad.objects.get(id=priv.unidad.id)
                if priv.privilegio == SolicitudPrivilegio.PRIVILEGIO_MIEMBRO:
                    unidad.miembros.add(priv.solicitante)
                    priv.solicitante.groups.add(miembro)
                elif priv.privilegio == SolicitudPrivilegio.PRIVILEGIO_SOLICITANTE:
                    unidad.solicitantes.add(priv.solicitante)
                    priv.solicitante.groups.add(solicitante)
                elif priv.privilegio == SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE:
                    priv.solicitante.groups.add(responsable)
                    unidad.responsable = priv.solicitante
                    unidad.save()
                listaMiembro=SolicitudPrivilegio.objects.none()
        #lista de los privilegios que quieren ser solicitantes
                listaPrivilegios=SolicitudPrivilegio.objects.none()
                listaResponsable=SolicitudPrivilegio.objects.none()
                for b in unidadesResponsable:
                    listaMiembro = listaMiembro|SolicitudPrivilegio.objects.filter(unidad=b, privilegio=2, estado=1)
                for a in unidadesMiembro:
                    listaPrivilegios=listaPrivilegios|SolicitudPrivilegio.objects.filter(unidad=a, privilegio=1, estado=1)
                if request.user.is_superuser:
                    listaResponsable=listaResponsable|SolicitudPrivilegio.objects.filter(privilegio=3, estado=1)
            
                return render_to_response("otorgarPrivilegio.html", {'msg': "Solicitud aceptada",'listaPrivilegios':listaPrivilegios, 'listaMiembro':listaMiembro,'listaResponsable':listaResponsable}, 
                                              context_instance=RequestContext(request))
                
        elif 'negar_privilegio' in request.POST:
                priv= SolicitudPrivilegio.objects.get(id=1)# Este id lo puse porque no se como obtener el de la solicitud
                priv.estado= 2
                priv.save()
                listaMiembro=SolicitudPrivilegio.objects.none()
        #lista de los privilegios que quieren ser solicitantes
                listaPrivilegios=SolicitudPrivilegio.objects.none()
                listaResponsable=SolicitudPrivilegio.objects.none()
                for b in unidadesResponsable:
                    listaMiembro = listaMiembro|SolicitudPrivilegio.objects.filter(unidad=b, privilegio=2, estado=1)
                for a in unidadesMiembro:
                    listaPrivilegios=listaPrivilegios|SolicitudPrivilegio.objects.filter(unidad=a, privilegio=1, estado=1)
                if request.user.is_superuser:
                    listaResponsable=listaResponsable|SolicitudPrivilegio.objects.filter(privilegio=3, estado=1)
                return render_to_response("otorgarPrivilegio.html", {'msg': "Solicitud cancelada",'listaPrivilegios':listaPrivilegios, 'listaMiembro':listaMiembro,'listaResponsable':listaResponsable}, 
                                              context_instance=RequestContext(request))

											  
@login_required(redirect_field_name='/')
def registroUnidad(request):
    if request.method == "GET":
        return render_to_response("registroUnidad.html", {'RegistroUnidadForm': RegistroUnidadForm()},
                                        context_instance=RequestContext(request))
    elif request.method == "POST":
        form = RegistroUnidadForm(request.POST)
        if form.is_valid():
            # Crear RegistroUnidadForm pasandole request.POST hace esto por ti
            # AQUI ESTABA EL ERROR NO SE POR QUE
            #e = Unidad(nombre = form.cleaned_data['nombre'],
            #        miembros = form.cleaned_data['miembros'],
            #        responsable = form.cleaned_data['responsable'],
            #        descripcion= form.cleaned_data['descripcion'])
            #e.save()
            form.save()
            ## AQUI TIENES QUE USAR HtmlResponseRedirect en vez de render_to_response
            # HtmlResponseRedirect(URL)
            return render_to_response("registroUnidad.html", {'msg': "Registro realizado con exito",'RegistroUnidadForm':RegistroUnidadForm()}, 
                                      context_instance=RequestContext(request))
        else:
            return render_to_response("registroUnidad.html", {'RegistroUnidadForm': form},
                                  context_instance=RequestContext(request))

def configurar_unidad(request):
    pass
