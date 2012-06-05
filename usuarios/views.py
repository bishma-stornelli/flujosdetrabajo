# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from usuarios.forms import RegistroForm, LoginForm, UserForm
from usuarios.models import PerfilDeUsuario


def index(request):
#Esta vista permite generar una pantalla sencilla de index, es necesario que se retorne el usuario para identificar
#si el usuario esta autenticado o no. 
#NOTA: no funciona utilizando la variable de contexto user provista por django
	if request.user.is_authenticated():
		usr = request.user
		return render_to_response("usuarios/index.html",{"usr":usr})
	else:
		return render_to_response("usuarios/index.html")

def registro(request):
#Esta vista permite generar(metodo GET) un formulario de registro y procesar el registro del usuario
#(metodo POST). Debe retornar 'reg' un mensaje que indica un registro exitoso o 'msj' que indica
#un problema con el registro.

	if request.method == "GET":
		if request.user.is_authenticated():
			return index(request)
		f = RegistroForm()
		return render_to_response("usuarios/registro.html",
					  {"registroform": f, "msj":""}, 
					  context_instance = RequestContext(request))
	elif request.method == "POST":
		f = RegistroForm(request.POST)
		if f.is_valid():
			try:
				u = User.objects.get(username__exact=f.cleaned_data['username'])
				messages.error(request,"El Username que inserto ya existe")
				return render_to_response("usuarios/registro.html",
							  {"registroform": f}, 
							  context_instance = RequestContext(request))
			except User.DoesNotExist:
				if f.cleaned_data['clave'] != f.cleaned_data['confirm']:
					messages.error(request,"La clave y la confirmacion no concuerdan")
					return render_to_response("usuarios/registro.html",
								  {"registroform": f}, context_instance = RequestContext(request))
				else:
					u = User.objects.create_user(username=f.cleaned_data['username'], 
                                                                        password=f.cleaned_data['clave'], 
                                                                        email=f.cleaned_data['email'])
					u.first_name = f.cleaned_data['nombre'] 
					u.last_name = f.cleaned_data['apellido']
					u.dni = f.cleaned_data['dni']
					u.save()
				   # p = PerfilDeUsuario.objects.create(user_id=1)
                   # p.user=f.cleaned_data['username']
                   # p.dni=f.cleaned_data['dni']
                   # p.save()
					l=LoginForm()
					messages.success(request,"La clave y la confirmacion no concuerdan")
					return render_to_response("usuarios/index.html", context_instance = RequestContext(request))
						
		else:	
			messages.error(request,"Alguno de los datos provistos tienen un formato equivocado")
			return render_to_response("usuarios/registro.html",
						   {"registroform":f }, context_instance = RequestContext(request))
			
#IMPORTANTE: Deberiamos mantener esta vista a pesar de que estemos usando la vista de login generica, 
# es posible que mas adelante nos demos cuenta que necesitamos hacer algo en el login que no se pueda
# hacer con la version generica.
def log_in(request):
#Esta vista permite generar un formulario de login(metodo GET) y procesar el login(metodo POST).
	if request.method == "GET":
		if request.user.is_authenticated():
			return render_to_response("usuarios/index.html",{"usr":request.user}, context_instance = RequestContext(request))
		else:
			f = LoginForm()
			return render_to_response("usuarios/log_in.html",{"loginform":f}, context_instance = RequestContext(request))
	elif request.method == "POST":
		f = LoginForm(request.POST)
		if f.is_valid():
			usr = authenticate(username = f.cleaned_data['username'], password = f.cleaned_data['clave'])
			if usr is not None:
				login(request, usr)
				msj = "Bienvenido "+usr.username
				return render_to_response("usuarios/index.html",{"usr":usr, "msj":msj}, context_instance = RequestContext(request))
			else:
				return render_to_response("usuarios/log_in.html", {"loginform":f, "msj": "Username o Password invalidos"},context_instance = RequestContext(request))
		else:
				
			return render_to_response("usuarios/log_in.html", {"loginform":f, "msj": "Formato de Datos Invalidos"},context_instance = RequestContext(request))

def log_out(request):
#Esta vista permite desloguearse de la pagina. Retorna la variable de retorno 'reg' para indicar la salida exitosa del sistema
	logout(request)			
	return render_to_response("usuarios/index.html",{"reg":"Sesion cerrada con exito"}, context_instance = RequestContext(request))


def consultar_datos_usuario(request):
    if request.user.is_authenticated():
        u= User.objects.get(username=request.user)
        perfil= PerfilDeUsuario.objects.all()
        return render_to_response("usuarios/consultar_datos_usuario.html",{"usr":u, "perfil":perfil}, context_instance = RequestContext(request))

    else:
        f = LoginForm()
        return render_to_response("usuarios/log_in.html",{"loginform":f}, context_instance = RequestContext(request))

def cambiar_clave(request):

    if request.user.is_authenticated():
        if request.method == 'POST': # If the form has been submitted...
            #form =
            user = request.user
            #Verificamos que sea el usuario con la clave antigua
            if user.check_password(request.POST['claveAntigua']):
                password = request.POST ['claveNueva']
                passwordConfirm = request.POST['claveConfirmacion']
                #Verificamos confirmacion de clave
                if password == passwordConfirm:
                    user.set_password(password)
                    user.save()
                    messages.success(request, "Cambio de clave exitosa")
                    return render_to_response("usuarios/index.html",{"usr":user}, context_instance = RequestContext(request))
                else:
                    messages.error(request,"Las claves no coinciden")
                    return render_to_response("usuarios/cambiar_clave.html", context_instance = RequestContext(request))

            else:
                messages.error(request,"Cambio de clave fallida")
                return render_to_response("usuarios/cambiar_clave.html", context_instance = RequestContext(request))
        else:
            return render_to_response('usuarios/cambiar_clave.html',
                context_instance = RequestContext(request))

    else:
        f = LoginForm()
        return render_to_response("usuarios/log_in.html",{"loginform":f}, context_instance = RequestContext(request))


def modificar_datos_usuario(request):
	
	if request.method == "GET":
		user_form = UserForm(instance=request.user)
		return render_to_response('usuarios/modificar_datos_usuario.html', { 'user_form': user_form }, context_instance=RequestContext(request))	

	else:
		u= User.objects.get(username=request.user)
		user_form = UserForm(request.POST, instance=request.user)
		if user_form.is_valid():
			u.first_name=user_form.cleaned_data['first_name']
			u.last_name=user_form.cleaned_data['last_name']
			u.email=user_form.cleaned_data['email']
			u.save()

			messages.success(request,"Perfil Actualizado Exitosamente")
			return render_to_response('usuarios/modificar_datos_usuario.html', { 'user_form': user_form}, context_instance=RequestContext(request))

		else:
			user_form = UserForm(instance=request.user)
			return render_to_response('usuarios/modificar_datos_usuario.html', { 'user_form': user_form}, context_instance=RequestContext(request))



