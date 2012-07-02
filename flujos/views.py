# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from flujos.forms import AgregarPasoForm, CrearFlujoForm, AgregarCampoForm,CopiarFlujoForm, ModificarPasoForm, ModificarFlujoForm, AgregarCaminoForm,CampoForm,AlertaForm,InformeForm
from flujos.models import Flujo, Paso, Campo, Criterio, Alerta, Informe
from unidades.models import Unidad, SolicitudPrivilegio

@login_required
def agregar_paso(request, flujo_id):
    flujo = get_object_or_404(Flujo, pk=flujo_id)
    if not flujo.unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
        messages.error(request,"Solo los responsables de unidad pueden crear flujos.")
        return HttpResponseRedirect(reverse("flujo_index"))
    if request.method == 'POST':
        form = AgregarPasoForm(request.POST, flujo = flujo)
        if form.is_valid():
            paso = form.save()
            messages.success(request, "Paso agregado exitosamente.")
            return HttpResponseRedirect("/flujos/consultar_paso/%s/" % paso.id)
        else:
            messages.error(request, "Verifique los datos introducidos e intente de nuevo.")
    else:
        form = AgregarPasoForm(flujo = flujo)
    return render_to_response('flujos/agregar_paso.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def crear_flujo(request):
    if not request.user.unidades_responsable.all():
        messages.error(request, "Necesita ser responsable de unidad para crear flujos.")
        return HttpResponseRedirect(reverse("flujo_index"))
    if request.method == 'POST':
        
        # Creo el form con los datos que llegaron del cliente
        form = CrearFlujoForm(request.POST, usuario=request.user)
        if form.is_valid():   
            # Si no existe unidad con id unidad_id envio error 404
            unidad = form.cleaned_data['unidad']
            # Verifico que el usuario que crea el flujo es responsable de la unidad a la que se asociara
            if not unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
                messages.error(request,"Usted no es responsable de la unidad donde quiere crear el flujo.")
                return HttpResponseRedirect(reverse("flujo_index"))
            flujo = form.save() 
            # SI ES EXITOSO REGRESO CON HttpResponseRedirect
            # SINO DEJO QUE AL FINAL SE PONGA CON render_to_response
            messages.success(request, "Flujo creado exitosamente.")
            return HttpResponseRedirect("/flujos/consultar_flujo/%s/" % flujo.id)
        else:
            messages.error(request, "Verifique los campos introducidos e intente de nuevo.")
    else:
        # Si no es POST creo un form vacio
        form = CrearFlujoForm(initial={'unidad': request.GET.get('unidad', '')}, usuario=request.user)
    # independientemente de si es post y el form no es valido o si es otro metodo, tengo que renderizar
    # el template flujos/crear_flujo.html, pasarle los parametros y el context_instance para el csrf_token
    return render_to_response("flujos/crear_flujo.html", {'form': form},
                                        context_instance=RequestContext(request))
                                        


@login_required
def agregar_campo(request, paso_id):

    p = get_object_or_404(Paso, pk=paso_id)
    
    if (p.flujo.unidad).permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
      
        if request.method == 'GET':
            
            f = CampoForm()
            return render_to_response("flujos/agregar_campo.html", {'form':f, 'paso_id':paso_id},
                                        context_instance=RequestContext(request))
        else:
        
            f = CampoForm(request.POST)
            
            if f.is_valid():
                try:
                    c = Campo.objects.get(paso=p, nombre=f.cleaned_data['nombre'])
                    messages.error(request, "El nombre del campo ya existe para este paso.")
                    return HttpResponseRedirect("/flujos/consultar_paso/%s/" % paso_id)
                
                except Campo.DoesNotExist:
                
                    campo = f.save(commit=False)
                    campo.paso = p    
                    campo.save()
                    messages.success(request, "Campo creado exitosamente.")
                    
                    return HttpResponseRedirect("/flujos/consultar_paso/%s/" % paso_id)
                
            else:
                 messages.error(request, "Verifique los campos introducidos e intente de nuevo.")
                 return render_to_response("flujos/agregar_campo.html", {'form':f, 'paso_id':paso_id},
                                        context_instance=RequestContext(request))
    else:
        messages.error(request, "Esta funcionalidad requiere permisos de Responsable de Unidad.")
        return render_to_response("usuarios/index.html", context_instance=RequestContext(request))
                
            
        
    

def listar_flujos(request):
    # OBTENER PARAMETRO POR URL: /?unidad=X
    unidad = request.GET.get('unidad', None)
    if unidad:
        flujos = Flujo.objects.filter(unidad=unidad)
        if not flujos:
            raise Http404()           
    else:
        flujos = Flujo.objects.all()    
    return render_to_response('flujos/listar_flujos.html', {'flujos': flujos}, context_instance=RequestContext(request))


@login_required
def copiar_flujo(request, flujo_id):
    flujo = get_object_or_404(Flujo, pk=flujo_id)
    if request.method == "POST":
        form = CopiarFlujoForm(request.POST, instance=flujo)
        if form.is_valid():
            form.save()     
            messages.success(request , "Copia de Flujo exitosa.")
            return HttpResponseRedirect(reverse("flujo_index"))
        else:
            messages.error(request, "Verifique el campo e intente de nuevo")
    else:
        form = CopiarFlujoForm(instance=flujo)
        return render_to_response("flujos/copiar_flujo.html", {'form':form}, context_instance=RequestContext(request))


@login_required
def consultar_flujo(request, flujo_id):
    flujo = get_object_or_404(Flujo, pk=flujo_id)
    return render_to_response('flujos/consultar_flujo.html',
                                  {'flujo': flujo}, context_instance=RequestContext(request))

@login_required
def consultar_paso(request, paso_id):
    paso = get_object_or_404(Paso, pk=paso_id)
    if not paso.flujo.unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
        messages.error(request, "Solo el responsable de la unidad puede modificar el flujo.")
        return HttpResponseRedirect(reverse("flujo_index"))
    return render_to_response('flujos/consultar_paso.html', {'paso': paso}, context_instance=RequestContext(request))


def listar_pasos(request, flujo_id):
    flujo = get_object_or_404(Flujo , pk=flujo_id)
    pasos = Paso.objects.filter(flujo=flujo)
    return render_to_response('flujos/listar_pasos.html', {'pasos': pasos})
    
@login_required
def modificar_paso(request, paso_id):
    paso = get_object_or_404(Paso, pk=paso_id)
    if not paso.flujo.unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
        messages.error(request, "Solo el responsable de la unidad puede modificar el flujo.")
        return HttpResponseRedirect(reverse("flujo_index"))
    if request.method == "POST":
        form = ModificarPasoForm(request.POST, instance=paso)
        if form.is_valid():
            form.save()     
            messages.success(request , "Modificacion exitosa.")
            return HttpResponseRedirect("/flujos/consultar_paso/%s/" % paso.id)
        else:
            messages.error(request, "Verifique los campos e intente de nuevo")
    else:
        form = ModificarPasoForm(instance=paso)
        return render_to_response("flujos/modificar_paso.html", {'form':form, 'paso': paso}, context_instance=RequestContext(request))


@login_required
def modificar_flujo(request, flujo_id):
    flujo = get_object_or_404(Flujo, pk=flujo_id)
    if not flujo.unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
        messages.error(request, "Solo el responsable de la unidad puede modificar el flujo.")
        return HttpResponseRedirect(reverse("flujo_index"))
    if request.method == "POST":
        form = ModificarFlujoForm(request.POST, instance=flujo)
        if form.is_valid():
            form.save()     
            messages.success(request , "Modificación exitosa.")
            return HttpResponseRedirect("/flujos/consultar_flujo/%s/" % flujo.id)
        else:
            messages.error(request, "Verifique los campos e intente de nuevo")
    else:
        form = ModificarFlujoForm(instance=flujo)
    return render_to_response("flujos/modificar_flujo.html", {'form':form, 'flujo_id':flujo_id}, context_instance=RequestContext(request))
        
@login_required
def listar_flujos_publico(request):
    unidades = Unidad.objects.filter(responsable=request.user)
    listaFlujo = Flujo.objects.none()
    for u in unidades:
         listaFlujo = listaFlujo | Flujo.objects.filter(unidad=u, estado=Flujo.ESTADO_PUBLICO)
    return render_to_response("flujos/marcar_obsoleto.html", {'listaFlujo':listaFlujo}, context_instance=RequestContext(request))

@login_required(redirect_field_name='/')
def marcar_obsoleto(request, flujo_id):
    unidades = Unidad.objects.filter(responsable=request.user)
    flujo = get_object_or_404(Flujo, pk=flujo_id)
    if (flujo.unidad in unidades and flujo.estado != Flujo.ESTADO_OBSOLETO):
        flujo.estado = Flujo.ESTADO_OBSOLETO
        flujo.save()
        messages.success(request, "Flujo (" + flujo.nombre + ") marcado como obsoleto.")
    else :
        messages.error(request, "Error: el flujo seleccionado no se pudo marcar como obsoleto.")
    return listar_flujos_publico(request)

def eliminar_paso(request, paso_id):
    paso = get_object_or_404(Paso, pk=paso_id)
    if not paso.flujo.unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
        messages.error(request, "Solo el responsable de la unidad puede modificar el flujo.")
        return HttpResponseRedirect(reverse("flujo_index"))
    paso.delete()
    messages.success(request, "Paso eliminado exitosamente.")
    return HttpResponseRedirect("/flujos/consultar_flujo/%s/" % paso.flujo.id)


@login_required
def listar_flujos_por_publicar(request):
    unidades = Unidad.objects.filter(responsable=request.user)
    listaFlujo = Flujo.objects.none()
    for u in unidades:
         listaFlujo = listaFlujo | Flujo.objects.filter(unidad=u, estado=Flujo.ESTADO_BORRADOR)
    return render_to_response("flujos/publicar_flujo.html", {'listaFlujo':listaFlujo}, context_instance=RequestContext(request))

# Para todos los elementos de temporal, se evalua si ya se encuentra en alcanzables, sino, se agrega
def mezclar(alcanzables, temporal):
    for t in temporal:
        if t not in alcanzables:
            alcanzables.append(t)
    return alcanzables

# @inicial Representa el paso inicial
# @recorrido son los nodos por el cual se ha pasado
# Devuelve True si es un grafo conexo de lo contrario devuelve False
def es_grafo_conexo(flujo):
    iniciales = Paso.objects.filter(tipo = Paso.TIPO_INICIAL)
    inicial = iniciales[0]
    pasos = list(Paso.objects.filter(flujo=flujo))
    pasosAbiertos = [inicial]
    recorrido = []
    while pasosAbiertos:
        pas = pasosAbiertos.pop()
        recorrido.append(pas)
        p = list(Paso.objects.get(id=pas.id).sucesores.all())
        for k in p:
            if k not in pasosAbiertos and k not in recorrido:
                pasosAbiertos.append(k)
    #messages.warning(request, str(recorrido) + " " + str(pasos))
    if len(pasos) == len(recorrido):
        return True
    else:
        return False 
    
@login_required(redirect_field_name='/')
def publicar_flujo(request, flujo_id):
    unidades = Unidad.objects.filter(responsable=request.user)
    flujo = get_object_or_404(Flujo, pk=flujo_id)
    if (flujo.estado == Flujo.ESTADO_BORRADOR):
        if (flujo.unidad in unidades):
            inicial_final = flujo.inicial_final()
            es_conexo = es_grafo_conexo(flujo)
            flujo_igual = flujo.nombre_parecido()
            if (inicial_final == True and es_conexo == True):
                if set(flujo_igual) == set(Flujo.objects.none()):
                    flujo.estado = Flujo.ESTADO_PUBLICO
                    flujo.save()
                    messages.success(request, "Flujo (" + flujo.nombre + ") publicado.")
                elif set(flujo_igual) != set(Flujo.objects.none()):
                    messages.error(request, "Ya existe un Flujo publicado con este mismo nombre, si quiere puede marcarlo como obsoleto al que esta publicado o de lo contrario no se podra publicar.")
                    return render_to_response("flujos/marcar_obsoleto.html", {'listaFlujo':flujo_igual}, context_instance=RequestContext(request))
                    
            else :
                if (inicial_final == False):
                    messages.error(request, "Flujo (" + flujo.nombre + ") no posee paso inicial o final, o posee mas de un paso inicial, revise el flujo.")
                if (es_conexo == False):
                    messages.error(request, "Flujo (" + flujo.nombre + ") posee pasos que estan aislados, revise el flujo.")     
        else :
            messages.error(request, "Error: el flujo seleccionado no se puedo publicar debido a que usted no es el" 
            + "responsable de la unidad a la cual esta asociado el flujo")
    else:
        messages.error(request, "Los flujos que estan en estado obsoleto no se puede publicar.")
    return consultar_flujo(request, flujo_id)

#@permission_required('flujos.criterio.add_criterio')
@login_required()
def agregar_camino(request, flujo_id):
    flujo = get_object_or_404(Flujo, pk=flujo_id)
    if not flujo.unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
        messages.error(request, "Solo el responsable de la unidad puede modificar el flujo.")
        return HttpResponseRedirect(reverse("flujo_index"))
    if request.POST:
        form = AgregarCaminoForm(request.POST)
        if form.is_valid():
            paso_origen = form.cleaned_data['paso_origen']
            paso_destino= form.cleaned_data['paso_destino']
            try:
                camino_igual= Criterio.objects.get(paso_origen=paso_origen, paso_destino=paso_destino)
                form = AgregarCaminoForm()
                messages.error(request, "Error:Este camino ya esta agregado")
                return HttpResponseRedirect("/flujos/modificar_camino/{0}/{1}/".format( flujo.id, camino_igual.id) ) 
            except ObjectDoesNotExist:
                form.save()
                form = AgregarCaminoForm()
                messages.success(request, "Camino almacenado exitosamente")       
            return HttpResponseRedirect("/flujos/consultar_flujo/{0}".format(flujo.id) )
        else:
            messages.error(request, "Error: Alguno de los datos del formulario es invalido")
            return render_to_response('flujos/agregar_camino.html',
                {'form':form, 'flujo_id':flujo_id}, context_instance=RequestContext(request))
    else:
        form = AgregarCaminoForm()
        form.fields["paso_origen"].queryset = Paso.objects.filter(flujo=flujo_id)
        form.fields["paso_destino"].queryset = Paso.objects.filter(flujo=flujo_id)
    return render_to_response('flujos/agregar_camino.html',
                {'form':form, 'flujo_id':flujo_id}, context_instance=RequestContext(request))

#@permission_required('flujos.criterio.change_criterio')
@login_required()
def modificar_camino(request, flujo_id, criterio_id):
    flujo = get_object_or_404(Flujo, pk=flujo_id)
    if not flujo.unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
        messages.error(request, "Solo el responsable de la unidad puede modificar el flujo.")
        return HttpResponseRedirect(reverse("flujo_index"))
    if request.POST:
        criterio = Criterio.objects.get(id=criterio_id)
        form = AgregarCaminoForm(request.POST, instance=criterio)
        if form.is_valid():
            camino = form.save()
            messages.success(request, "Camino actualizado exitosamente")
            return HttpResponseRedirect("/flujos/consultar_flujo/%s/" % camino.paso_origen.flujo)
        else:
            messages.error(request, "Error: Alguno de los datos del formulario es invalido")
            return render_to_response('flujos/modificar_camino.html',
                    {'form':form, 'flujo_id':flujo_id, 'criterio_id':criterio_id}, context_instance=RequestContext(request))
    else:
        criterio = Criterio.objects.get(id=criterio_id)
        form = AgregarCaminoForm(instance=criterio)
        form.fields["paso_origen"].queryset = Paso.objects.filter(flujo=flujo_id)
        form.fields["paso_destino"].queryset = Paso.objects.filter(flujo=flujo_id)
        return render_to_response('flujos/modificar_camino.html',
                {'form':form, 'flujo_id':flujo_id, 'criterio_id':criterio_id}, context_instance=RequestContext(request))

def listar_caminos(request, flujo_id):
    caminos = Criterio.objects.all()
    return render_to_response('flujos/listar_caminos.html', {'caminos': caminos, 'flujo_id':flujo_id})

def eliminar_camino(request, flujo_id, criterio_id):
    flujo = get_object_or_404(Flujo, pk=flujo_id)
    if not flujo.unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
        messages.error(request, "Solo el responsable de la unidad puede modificar el flujo.")
        return HttpResponseRedirect(reverse("flujo_index"))
    criterio = get_object_or_404(Criterio, pk=criterio_id)
    criterio.delete()
    return HttpResponseRedirect("/flujos/listar_caminos/")

def modificar_campo(request, campo_id):
    # Si no existe campo con id campo_id envio error 404
    campo = get_object_or_404(Campo, pk=campo_id)
    if request.method == 'POST':
        form = CampoForm(request.POST,instance = campo)
        if form.is_valid():   
            campo = form.save(commit=False)
            campo.save()
            messages.success(request, "Campo actualizado exitosamente.")
            return HttpResponseRedirect("/flujos/consultar_paso/%s/" % campo.paso.id)
        else:
            messages.error(request, "Verifique los campos introducidos e intente de nuevo.")
    else:
         form = CampoForm(instance=campo)
         return render_to_response("flujos/modificar_campo.html", {'form': form,
                                                          'campo_id': campo_id },
                                        context_instance=RequestContext(request))


def eliminar_campo(request, campo_id):
    campo = get_object_or_404(Campo, pk=campo_id)
    campo.delete()
    messages.success(request, "Campo eliminado exitosamente.")
    return HttpResponseRedirect("/flujos/consultar_paso/%s/" % campo.paso.id)

def agregar_alerta(request, paso_id):
    paso = get_object_or_404(Paso, pk=paso_id)
    if request.POST:
        form = AlertaForm(request.POST, paso=paso)
        if form.is_valid():
            alerta = form.save()
            messages.success(request, "Alerta agregada exitosamente")
            return HttpResponseRedirect("/flujos/consultar_alerta/%s/" % alerta.id)
        else:
            messages.error(request, "Error: Alguno de los datos del formulario es invalido")
            return render_to_response('flujos/agregar_alerta.html',
                    {'form':form, 'paso':paso}, context_instance=RequestContext(request))
    else:
        form = AlertaForm(paso=paso)
        return render_to_response('flujos/agregar_alerta.html',
                                {'form':form,'paso':paso}, context_instance=RequestContext(request))

def eliminar_alerta(request,alerta_id):
    alerta = get_object_or_404(Alerta,pk=alerta_id)
    if not alerta.paso.flujo.unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
        messages.error(request, "Solo el responsable de la unidad puede eliminar la alerta.")
        return HttpResponseRedirect(reverse("flujo_index"))
    alerta.delete()
    messages.success(request,"Alerta eliminada exitosamente")
    return HttpResponseRedirect("/flujos/consultar_paso/%s/" % alerta.paso.id)

def agregar_informe(request, paso_id):
    paso = get_object_or_404(Paso, pk=paso_id)
    if request.POST:
        form = InformeForm(request.POST, paso=paso)
        if form.is_valid():
            informe = form.save()
            messages.success(request, "Informe agregado exitosamente")
            return HttpResponseRedirect("/flujos/consultar_informe/%s/" % informe.id)
        else:
            messages.error(request, "Error: Alguno de los datos del formulario es invalido")
            return render_to_response('flujos/agregar_informe.html',
                    {'form':form, 'paso':paso}, context_instance=RequestContext(request))
    else:
        form = AlertaForm(paso=paso)
        return render_to_response('flujos/agregar_informe.html',
                    {'form':form,'paso':paso}, context_instance=RequestContext(request))



@login_required
def consultar_alerta(request, alerta_id):
    alerta = get_object_or_404(Alerta, pk = alerta_id)
    return render_to_response('flujos/consultar_alerta.html', {'alerta': alerta}, 
    											context_instance=RequestContext(request))
    											
@login_required
def consultar_informe(request, informe_id):
    informe = get_object_or_404(Informe, pk = informe_id)
    return render_to_response('flujos/consultar_informe.html', {'informe': informe}, 
    											context_instance = RequestContext(request))

def eliminar_informe(request,informe_id):
    informe = get_object_or_404(Informe,pk=informe_id)
    if not informe.paso.flujo.unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
        messages.error(request, "Solo el responsable de la unidad puede eliminar el informe.")
        return HttpResponseRedirect(reverse("flujo_index"))
    informe.delete()
    messages.success(request,"Informe eliminado exitosamente")
    return HttpResponseRedirect("/flujos/consultar_paso/%s/" % informe.paso.id)


def modificar_alerta(request, alerta_id):
    alerta = get_object_or_404(Alerta, pk=alerta_id)
    if request.POST:
        if 'cancelar' in request.POST:
            return HttpResponseRedirect("/flujos/consultar_alerta/%s/" % alerta.id)
        form = AlertaForm(request.POST, instance=alerta, paso=alerta.paso)
        if form.is_valid():
            alerta = form.save()
            messages.success(request, "Alerta modificada exitosamente")
            return HttpResponseRedirect("/flujos/consultar_alerta/%s/" % alerta.id)
        else:
            messages.error(request, "Error: Alguno de los datos del formulario es invalido")
    else:
        form = AlertaForm(instance=alerta, paso=alerta.paso)
    return render_to_response('flujos/modificar_alerta.html',{'form':form , 'paso_id': alerta.paso.id}, context_instance=RequestContext(request))

def modificar_informe(request, informe_id):
    informe = get_object_or_404(Informe, pk=informe_id)
    if request.POST:
        if 'cancelar' in request.POST:
            return HttpResponseRedirect("/flujos/consultar_informe/%s/" % informe.id)
        form = InformeForm(request.POST, instance=informe, paso=informe.paso)
        if form.is_valid():
            informe = form.save()
            messages.success(request, "Informe modificada exitosamente")
            return HttpResponseRedirect("/flujos/consultar_informe/%s/" % informe.id)
        else:
            messages.error(request, "Error: Alguno de los datos del formulario es invalido")
    else:
        form = InformeForm(instance=informe, paso=informe.paso)
    return render_to_response('flujos/modificar_informe.html',{'form':form , 'paso_id': informe.paso.id}, context_instance=RequestContext(request))

