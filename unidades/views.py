# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from django.core.urlresolvers import reverse
from django.db.models.query_utils import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, get_object_or_404, \
    render_to_response
from django.template import Context, loader, RequestContext
from unidades.forms import RegistroUnidadForm, SolicitudPrivilegioForm, \
    ConfigurarUnidadForm
from unidades.models import SolicitudPrivilegio, Unidad

@login_required
def solicitud_privilegio(request):
  if request.method == "GET":

    return render_to_response("unidades/solicitud_privilegio.html", {'SolicitudPrivilegioForm': SolicitudPrivilegioForm()},
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
                
                messages.success(request, "Solicitud aceptada.")
                return render_to_response("unidades/solicitud_privilegio.html", {'SolicitudPrivilegioForm':SolicitudPrivilegioForm()},context_instance=RequestContext(request)) 
            else:
                messages.error(request, 'Error: Campos invalidos.')
                return render_to_response("unidades/solicitud_privilegio.html", {'SolicitudPrivilegioForm': form},
		      context_instance=RequestContext(request))
     #dasdas          
                
@login_required
def otorgar_privilegio(request):
    #miembro = get_object_or_404(Group, name='Miembro de Unidad')
    #solicitante = get_object_or_404(Group, name='Solicitante')
    #responsable = get_object_or_404(Group, name='Responsable de Unidad')
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

        return render_to_response("unidades/otorgar_privilegio.html",{'listaPrivilegios':listaPrivilegios, 'listaMiembro':listaMiembro,'listaResponsable':listaResponsable}, context_instance=RequestContext(request))
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
                messages.success(request, "Solicitud aceptada.")
                return render_to_response("unidades/otorgar_privilegio.html", {'listaPrivilegios':listaPrivilegios, 'listaMiembro':listaMiembro,'listaResponsable':listaResponsable}, 
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
                messages.success(request, "Solicitud cancelada.")
                return render_to_response("unidades/otorgar_privilegio.html", {'listaPrivilegios':listaPrivilegios, 'listaMiembro':listaMiembro,'listaResponsable':listaResponsable}, 
                                              context_instance=RequestContext(request))


@login_required
def registrar_unidad(request):
	if request.method == "POST":
		form = RegistroUnidadForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success( request , "Registro de unidad exitoso.")
			return HttpResponseRedirect(reverse("unidades_index"))
		else:
			messages.error(request, "Verifique los datos e intente de nuevo.")
	else:
		form = RegistroUnidadForm()
	return render_to_response("unidades/registrar_unidad.html", {'form':form}, context_instance=RequestContext(request))

def configurar_unidad(request, unidad_id):
  unidad = get_object_or_404( Unidad, pk = unidad_id)
  if request.method == "POST":
    form = ConfigurarUnidadForm(request.POST, instance=unidad)
    if form.is_valid():
      form.save()     
      messages.success( request , "Configuracion exitosa.")
      return HttpResponseRedirect(reverse("unidades_index"))
    else:
      messages.error(request, "Verifique los campos e intente de nuevo")
  else:
    form = ConfigurarUnidadForm(instance = unidad)
    return render_to_response("unidades/configurar_unidad.html", {'form':form}, context_instance=RequestContext(request))

@login_required
def solicitar_privilegio(request):
    if request.method == 'POST':
        form = SolicitudPrivilegioForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.solicitante = request.user
            s.save()
            messages.success(request, "Su solicitud de privilegios ha sido enviada con exito. \
            Por favor espere a que sea aprobada.")
            return HttpResponseRedirect("/unidades/solicitar_privilegio/")
    else:
        form = SolicitudPrivilegioForm()
    return render_to_response("unidades/solicitar_privilegio.html",
                              {"form": form},
                              context_instance=RequestContext(request))

@login_required
def otorgar_privilegios(request):
    u = request.user
    if request.method == 'POST':        
        sp = get_object_or_404(SolicitudPrivilegio, pk=request.POST.get('id', -1))
        unidad = sp.unidad
        if sp.privilegio == SolicitudPrivilegio.PRIVILEGIO_SOLICITANTE:
            if unidad.permite(usuario=u, permiso=SolicitudPrivilegio.PRIVILEGIO_MIEMBRO):
                if 'aceptar_privilegio' in request.POST: 
                    sp.solicitante.unidades_solicitantes.add(unidad) 
                sp.estado = SolicitudPrivilegio.ESTADO_ACEPTADO if 'aceptar_privilegio' in request.POST else SolicitudPrivilegio.ESTADO_NEGADO
                sp.save()
            else:
                raise Http404()
        elif sp.privilegio == SolicitudPrivilegio.PRIVILEGIO_MIEMBRO: 
            if unidad.permite(usuario=u, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
                if 'aceptar_privilegio' in request.POST:
                    sp.solicitante.unidades_miembros.add(unidad)
                sp.estado = SolicitudPrivilegio.ESTADO_ACEPTADO if 'aceptar_privilegio' in request.POST else SolicitudPrivilegio.ESTADO_NEGADO
                sp.save()
            else:
                raise Http404()
        elif sp.privilegio == SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE:
            if u.is_staff:
                if 'aceptar_privilegio' in request.POST:
                    sp.solicitante.unidades_responsable.add(unidad)
                sp.estado = SolicitudPrivilegio.ESTADO_ACEPTADO if 'aceptar_privilegio' in request.POST else SolicitudPrivilegio.ESTADO_NEGADO
                sp.save()
            else:
                raise Http404()
        else:
            print "Hay una solicitud de privilegio en la base de datos cuyo privilegio no corresponde con los \
            valores posibles para las solicitudes de privilegio."
            raise Http404()
        messages.success(request, "Solicitud aprobada.")
        return HttpResponseRedirect("/unidades/otorgar_privilegio/")
    q1 = [Q(estado=SolicitudPrivilegio.ESTADO_ESPERA,unidad=value,privilegio=SolicitudPrivilegio.PRIVILEGIO_SOLICITANTE) for value in u.unidades_miembros.all()]
    q2 = [Q(estado=SolicitudPrivilegio.ESTADO_ESPERA,unidad=value,privilegio=SolicitudPrivilegio.PRIVILEGIO_MIEMBRO) for value in u.unidades_responsable.all()]
    q3 = []
    if u.is_staff:
        q3 = [Q(estado=SolicitudPrivilegio.ESTADO_ESPERA,unidad=value,privilegio=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE) for value in Unidad.objects.all()]
    qu1 = Q(pk=-1)
    qu2 = Q(pk=-1)
    qu3 = Q(pk=-1)
    for item in q1: 
        qu1 |= item
    for item in q2: 
        qu2 |= item
    for item in q3: 
        qu3 |= item
    r1 = SolicitudPrivilegio.objects.filter(qu1)
    r2 = SolicitudPrivilegio.objects.filter(qu2)
    r3 = SolicitudPrivilegio.objects.filter(qu3)
    return render_to_response("unidades/otorgar_privilegio.html",
                              {'solicitudes_responsable': r3,
                               'solicitudes_miembro': r2,
                               'solicitudes_solicitante': r1},
                              context_instance=RequestContext(request))
    
    