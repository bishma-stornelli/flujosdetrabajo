# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from flujos.forms import CrearFlujoForm
from unidades.models import Unidad

@login_required
def crear_flujo(request, unidad_id):
    if request.method == 'POST':
        # FALTA VERIFICAR QUE EL QUE CREA EL FLUJO ES EL RESPONSABLE DE LA UNIDAD CON ID unidad_id  
        form = CrearFlujoForm(request.POST)
        if form.is_valid():   
            # Aqui puedo ejecutar directamente en el form:
            # form.save()
            # y eso lo guarda en la base de datos, pero como unidad_id no puede ser null entonces
            # tengo que modificarlo antes de guardarlo
            flujo = form.save(commit=False) # Regresa un objeto de tipo Flujo con los datos del formulario
            # Si no existe unidad con id unidad_id envio error 404
            unidad = get_object_or_404(Unidad, pk=unidad_id)
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

def listar_flujos(request):
    pass

def copiar_flujo(request, flujo_id):
    pass