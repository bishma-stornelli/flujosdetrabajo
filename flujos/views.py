# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from flujos.forms import CrearFlujoForm, AgregarCampoForm, ModificarPasoForm, ModificarFlujoForm,AgregarCaminoForm
from flujos.models import Paso, Campo, Flujo, Criterio
from unidades.models import Unidad, SolicitudPrivilegio
from django.contrib.auth.decorators import permission_required

@login_required
def crear_flujo(request):
    if request.method == 'POST':
        
        # Creo el form con los datos que llegaron del cliente
        form = CrearFlujoForm(request.POST)
        if form.is_valid():   
            # Si no existe unidad con id unidad_id envio error 404
            unidad = form.cleaned_data['unidad']
            # Verifico que el usuario que crea el flujo es responsable de la unidad a la que se asociara
            if not unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
                return Http404()
            flujo = form.save() 
            # SI ES EXITOSO REGRESO CON HttpResponseRedirect
            # SINO DEJO QUE AL FINAL SE PONGA CON render_to_response
            messages.success(request, "Flujo creado exitosamente.")
            return HttpResponseRedirect("/flujos/consultar_flujo/%s/" % flujo.id)
        else:
            messages.error(request, "Verifique los campos introducidos e intente de nuevo.")
    else:
        # Si no es POST creo un form vacio
        form = CrearFlujoForm(initial={'unidad': request.GET.get('unidad', '')})
    # independientemente de si es post y el form no es valido o si es otro metodo, tengo que renderizar
    # el template flujos/crear_flujo.html, pasarle los parametros y el context_instance para el csrf_token
    return render_to_response("flujos/crear_flujo.html", {'form': form},
                                        context_instance=RequestContext(request))
                                        


@login_required
def agregar_campo(request, paso_id):

    p = get_object_or_404(Paso, pk=paso_id)
    
    if (p.flujo.unidad).permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
      
        if request.method == 'GET':
            
            f = AgregarCampoForm()
            return render_to_response("flujos/agregar_campo.html", {'form':f, 'paso_id':paso_id}, 
                                        context_instance=RequestContext(request))
        else:
        
            f=AgregarCampoForm(request.POST)
            
            if f.is_valid():
                try:
                    c=Campo.objects.get(paso=p, nombre=f.cleaned_data['nombre'])
                    messages.error(request, "El nombre del campo ya existe para este paso.")
                    return HttpResponseRedirect("/flujos/consultar_paso/%s/" % paso_id)
                
                except Campo.DoesNotExist:
                
                    campo = Campo(nombre = f.cleaned_data['nombre'],llenado_por_miembro=True, llenado_por_solicitante=False, tipo = f.cleaned_data['tipo'], esObligatorio = f.cleaned_data['esObligatorio'], paso=p)
                    campo.paso = p    
                    campo.save()
                    messages.success(request, "Campo creado exitosamente.")
                    
                    return HttpResponseRedirect("/flujos/consultar_paso/%s/" % paso_id)
                
            else:
                 messages.error(request, "Verifique los campos introducidos e intente de nuevo.")
                 return render_to_response("flujos/agregar_campo.html", {'form':f}, 
                                        context_instance=RequestContext(request))
    else:
        messages.error(request, "Esta funcionalidad requiere permisos de Responsable de Unidad.")
        return render_to_response("usuarios/index.html", context_instance=RequestContext(request))
                
            
        
    

def listar_flujos(request, unidad_id):
  unidad = get_object_or_404(Unidad , pk=unidad_id)
  flujos = Flujo.objects.filter(unidad=unidad)
  return render_to_response('flujos/listar_flujos.html', {'flujos': flujos})


@login_required
def copiar_flujo(request, flujo_id):
    flujo = get_object_or_404( Flujo, pk = flujo_id)
	if request.method == "POST":
		form = CopiarFlujoForm(request.POST, instance=flujo)
		if form.is_valid():
			form.save()     
			messages.success( request , "Copia de Flujo exitosa.")
			return HttpResponseRedirect(reverse("flujo_index"))
		else:
			messages.error(request, "Verifique el campo e intente de nuevo")
	else:
		form = CopiaFlujoForm(instance = flujo)
		return render_to_response("flujos/copiar_flujo.html", {'form':form}, context_instance=RequestContext(request))
    

@login_required
def consultar_flujo(request, flujo_id):
    flujo = get_object_or_404(Flujo, pk=flujo_id)
    if flujo.unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
        return render_to_response('flujos/consultar_flujo.html',
                                  {'flujo': flujo}, context_instance=RequestContext(request))
    else:
        raise Http404()

@login_required
def consultar_paso(request, paso_id):
	paso = get_object_or_404(Paso, pk=paso_id)
	if paso.flujo.unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
		return render_to_response('flujos/consultar_paso.html', {'paso': paso}, context_instance=RequestContext(request))
	else:
		raise Http404()

def agregar_paso_flujo(request, flujo_id):
  #  if request.method == 'POST':
   #     form = ErrorSaveForm(request)
    #    if form.is_valid():
            


     #       return HttResponseRedirect('')
    #else:
     #   form = ErrorSaveForm()

    #return render_to_response('agregar_paso.html', {'form': form})
    pass
    
def listar_pasos(request, flujo_id):
  flujo = get_object_or_404(Flujo , pk = flujo_id)
  pasos = Paso.objects.filter(flujo = flujo)
  return render_to_response('flujos/listar_pasos.html', {'pasos': pasos})
    
def modificar_paso(request, paso_id):
	paso = get_object_or_404( Paso, pk = paso_id)
	if request.method == "POST":
		form = ModificarPasoForm(request.POST, instance=paso)
		if form.is_valid():
			form.save()     
			messages.success( request , "Modificacion exitosa.")
			return HttpResponseRedirect(reverse("flujo_index"))
		else:
			messages.error(request, "Verifique los campos e intente de nuevo")
	else:
		form = ModificarPasoForm(instance = paso)
		return render_to_response("flujos/modificar_paso.html", {'form':form}, context_instance=RequestContext(request))


def modificar_flujo(request, flujo_id):
	flujo = get_object_or_404( Flujo, pk = flujo_id)
	if request.method == "POST":
		form = ModificarFlujoForm(request.POST, instance=flujo)
		if form.is_valid():
			form.save()     
			messages.success( request , "Modificacion exitosa.")
			return HttpResponseRedirect(reverse("flujo_index"))
		else:
			messages.error(request, "Verifique los campos e intente de nuevo")
	else:
		form = ModificarFlujoForm(instance = flujo)
		return render_to_response("flujos/modificar_flujo.html", {'form':form,'flujo_id':flujo_id}, context_instance=RequestContext(request))
        
@login_required(redirect_field_name='/')
def listar_flujos_publico(request):
    unidades = Unidad.objects.filter(responsable=request.user)
    listaFlujo = Flujo.objects.none()
    for u in unidades:
         listaFlujo = listaFlujo|Flujo.objects.filter(unidad=u,estado=Flujo.ESTADO_PUBLICO)
    return render_to_response("flujos/marcar_obsoleto.html", {'listaFlujo':listaFlujo}, context_instance=RequestContext(request))

@login_required(redirect_field_name='/')
def marcar_obsoleto(request, flujo_id):
    unidades = Unidad.objects.filter(responsable=request.user)
    flujo = get_object_or_404( Flujo, pk = flujo_id)
    if (flujo.unidad in unidades and flujo.estado!=Flujo.ESTADO_OBSOLETO):
        flujo.estado = Flujo.ESTADO_OBSOLETO
        flujo.save()
        messages.success(request, "Flujo (" + flujo.nombre + ") marcado como obsoleto.")
    else :
        messages.error(request, "Error: el flujo seleccionado no se pudo marcar como obsoleto.")
    return listar_flujos_publico(request)

def eliminar_paso(request, paso_id):
	paso = get_object_or_404(Paso, pk = paso_id)
	flujo = paso.flujo
	if request.method == "GET":
		if(paso):	
			paso.delete()
	return HttpResponseRedirect(reverse("flujo_index"))


@login_required(redirect_field_name='/')
def listar_flujos_por_publicar(request):
    unidades = Unidad.objects.filter(responsable=request.user)
    listaFlujo = Flujo.objects.none()
    for u in unidades:
         listaFlujo = listaFlujo|Flujo.objects.filter(unidad=u,estado=Flujo.ESTADO_BORRADOR)
    return render_to_response("flujos/publicar_flujo.html", {'listaFlujo':listaFlujo}, context_instance=RequestContext(request))

# Para todos los elementos de temporal, se evalua si ya se encuentra en alcanzables, sino, se agrega
def mezclar(alcanzables,temporal):
    for t in temporal:
        if t not in alcanzables:
            alcanzables.append(t)
    return alcanzables

# @alcanzables son todos los nodos alcanzables a partir de un nodo inicial contenido en alcanzable
# @recorrido son los nodos por el cual se ha pasado
# return alcanzables
def dfs(alcanzables,recorrido):
    while not recorrido == alcanzables:
        temporal = []
        for al in alcanzables:
            if al not in recorrido:
                recorrido.append(al)
                temporal.extend(list(Paso.objects.get(paso=al).sucesores.all()))
                temporal.extend(list(Paso.objects.filter(sucesores=al)))
        alcanzables = mezclar(alcanzables,temporal)
    return alcanzables
# @alcanzables son todos los nodos alcanzables
# @recorrido son los nodos por el cual se ha pasado
# @pasos son todos los nodos presentes en el flujo
# @pas representa el nodo inicial y se le aplicara un dfs para saber si los nodos alcanzables
# Devuelve True si es un grafo conexo de lo contrario devuelve False
def es_grafo_conexo(flujo):
    pasos = Paso.objects.filter(flujo=flujo)
    for pas in pasos:
        alcanzables = [pas]
        recorrido = []
        if not dfs(alcanzables,recorrido) == list(pasos):
            return False
    return True 
    


@login_required(redirect_field_name='/')
def publicar_flujo(request, flujo_id):
    unidades = Unidad.objects.filter(responsable=request.user)
    flujo = get_object_or_404( Flujo, pk = flujo_id)
    if (flujo.unidad in unidades):
        inicial_final= flujo.inicial_final()
        es_conexo= es_grafo_conexo(flujo)
        flujo_igual= flujo.nombre_parecido()
        if (inicial_final == True &  es_conexo == True):
            if set(flujo_igual) == set(Flujo.objects.none()):
                flujo.estado = Flujo.ESTADO_PUBLICO
                flujo.save()
                messages.success(request, "Flujo (" + flujo.nombre + ") publicado.")
            elif set(flujo_igual) != set(Flujo.objects.none()):
                messages.error(request, "Flujo (" + flujo.nombre + ") ya existe con este nombre si quiere puede marcarlo como obsoleto y volver a publicarlo o no se podra publicar ")
                return render_to_response("flujos/marcar_obsoleto.html", {'listaFlujo':flujo_igual}, context_instance=RequestContext(request))
                
        else :
            messages.success(request, "Flujo (" + flujo.nombre + ") no pudo ser publicado.")
    else :
        messages.error(request, "Error: el flujo seleccionado no se pudo publicar o porque no tiene nodo inicial o final o porque no es conexo")
    return listar_flujos_por_publicar(request)

@permission_required('flujos.criterio.add_criterio')
@login_required()
def agregar_camino(request, flujo_id):
    if request.POST:
        form = AgregarCaminoForm(request.POST)
        if form.is_valid():
            form.save()
            form = AgregarCaminoForm()
            messages.success(request, "Camino almacenado exitosamente")
            caminos = Criterio.objects.all()
            return render_to_response('flujos/listar_caminos.html', {'caminos': caminos,'flujo_id':flujo_id})
        else:
            messages.error(request, "Error: Alguno de los datos del formulario es invalido")
            return render_to_response('flujos/agregar_camino.html',
                {'form':form,'flujo_id':flujo_id}, context_instance=RequestContext(request))
    else:
        form = AgregarCaminoForm()
        form.fields["paso_origen"].queryset = Paso.objects.filter(flujo=flujo_id)
        form.fields["paso_destino"].queryset = Paso.objects.filter(flujo=flujo_id)
        return render_to_response('flujos/agregar_camino.html',
                {'form':form,'flujo_id':flujo_id}, context_instance=RequestContext(request))

@permission_required('flujos.criterio.change_criterio')
@login_required()
def modificar_camino(request, flujo_id,criterio_id):
    if request.POST:
        criterio=Criterio.objects.get(id=criterio_id)
        form = AgregarCaminoForm(request.POST,instance=criterio)
        if form.is_valid():
            form.save()
            form = AgregarCaminoForm()
            messages.success(request, "Camino actualizado exitosamente")
            caminos = Criterio.objects.all()
            return render_to_response('flujos/listar_caminos.html', {'caminos': caminos,'flujo_id':flujo_id})
        else:
            messages.error(request, "Error: Alguno de los datos del formulario es invalido")
            return render_to_response('flujos/modificar_camino.html',
                    {'form':form,'flujo_id':flujo_id,'criterio_id':criterio_id}, context_instance=RequestContext(request))
    else:
        criterio = Criterio.objects.get(id=criterio_id)
        form = AgregarCaminoForm(instance=criterio)
        form.fields["paso_origen"].queryset = Paso.objects.filter(flujo=flujo_id)
        form.fields["paso_destino"].queryset = Paso.objects.filter(flujo=flujo_id)
        return render_to_response('flujos/modificar_camino.html',
                {'form':form,'flujo_id':flujo_id,'criterio_id':criterio_id}, context_instance=RequestContext(request))

def listar_caminos(request,flujo_id):
    caminos = Criterio.objects.all()
    return render_to_response('flujos/listar_caminos.html', {'caminos': caminos,'flujo_id':flujo_id})

def eliminar_camino(request,flujo_id, criterio_id):
    criterio = get_object_or_404(Criterio, pk = criterio_id)
    if request.method == "GET":
        if(criterio):
            criterio.delete()
    caminos = Criterio.objects.all()
    return render_to_response('flujos/listar_caminos.html', {'caminos': caminos,'flujo_id':flujo_id})
