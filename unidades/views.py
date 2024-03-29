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
def registrar_unidad(request):
    if not request.user.is_staff:
        messages.error( request , "Solo el administrador puede crear unidades")
        return HttpResponseRedirect(reverse("unidades_index"))

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

@login_required
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
            return HttpResponseRedirect(reverse("listar_privilegios"))
    else:
        form = SolicitudPrivilegioForm(initial={'unidad': request.GET.get('unidad', '')})
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
@login_required                              
def listar_privilegios(request):
    u = request.user
    lista_espera = SolicitudPrivilegio.objects.filter(solicitante = u,estado = 1)
    lista_aceptado = SolicitudPrivilegio.objects.filter(solicitante = u, estado = 2)
    lista_negado = SolicitudPrivilegio.objects.filter(solicitante = u, estado = 3)
          
    return render_to_response("unidades/listar_privilegios.html",
                              {'en_espera': lista_espera,
                               'aceptadas': lista_aceptado,
                               'negadas': lista_negado},
                              context_instance=RequestContext(request))
