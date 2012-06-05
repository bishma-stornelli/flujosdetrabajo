# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils import timezone
from flujos.forms import CrearFlujoForm, ModificarPasoForm, ModificarFlujoForm
from flujos.models import Flujo, Paso
from unidades.models import Unidad, SolicitudPrivilegio


@login_required
def crear_flujo(request, unidad_id):
    if request.method == 'POST':
        # Si no existe unidad con id unidad_id envio error 404
        unidad = get_object_or_404(Unidad, pk=unidad_id)
        # Verifico que el usuario que crea el flujo es responsable de la unidad a la que se asociara
        unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE)
        # Creo el form con los datos que llegaron del cliente
        form = CrearFlujoForm(request.POST)
        if form.is_valid():   
            # Aqui puedo ejecutar directamente en el form:
            # form.save()
            # y eso lo guarda en la base de datos, pero como unidad_id no puede ser null entonces
            # tengo que modificarlo antes de guardarlo
            flujo = form.save(commit=False) # Regresa un objeto de tipo Flujo con los datos del formulario
            
            flujo.unidad = unidad 
            flujo.save()
            # SI ES EXITOSO REGRESO CON HttpResponseRedirect
            # SINO DEJO QUE AL FINAL SE PONGA CON render_to_response
            messages.success(request, "Flujo creado exitosamente.")
            return HttpResponseRedirect("/flujos/crear_flujo/%s/" % unidad_id)
        else:
            messages.error(request, "Verifique los campos introducidos e intente de nuevo.")
    else:
        # Si no es POST creo un form vacio
        form = CrearFlujoForm()
    # independientemente de si es post y el form no es valido o si es otro metodo, tengo que renderizar
    # el template flujos/crear_flujo.html, pasarle los parametros y el context_instance para el csrf_token
    return render_to_response("flujos/crear_flujo.html", {'form': form,
                                                          'unidad_id': unidad_id },
                                        context_instance=RequestContext(request))
                                        


def listar_flujos(request, unidad_id):
  unidad = get_object_or_404(Unidad , pk=unidad_id)
  flujos = Flujo.objects.filter(unidad=unidad)
  return render_to_response('flujos/listar_flujos.html', {'flujos': flujos})


def copiar_flujo(request, flujo_id):
    # flujo = get_object_or_404(Flujo, pk=flujo_id)
    #flujo_nuevo = flujo.clone();
#form = CopiarFlujoForm()
 pass   

@login_required
def consultar_flujo(request, flujo_id):
    flujo = get_object_or_404(Flujo, pk=flujo_id)
    if flujo.unidad.permite(usuario=request.user, permiso=SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE):
        return render_to_response('flujos/consultar_flujo.html',
                                  {'flujo': flujo}, context_instance=RequestContext(request))
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
		return render_to_response("flujos/modificar_flujo.html", {'form':form}, context_instance=RequestContext(request))
