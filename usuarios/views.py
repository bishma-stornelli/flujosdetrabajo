# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import redirect_to_login
from django.template import  RequestContext
from django.shortcuts import render_to_response
from usuarios.forms import RegistroForm, LoginForm
from usuarios.models import PerfilDeUsuario

def index(request):
#Esta vista permite generar una pantalla sencilla de index, es necesario que se retorne el usuario para identificar
#si el usuario esta autenticado o no. 
#NOTA: no funciona utilizando la variable de contexto user provista por django
	if request.user.is_authenticated():
		usr = request.user
		return render_to_response("index.html",{"usr":usr})
	else:
		return render_to_response("index.html")

def registro(request):
#Esta vista permite generar(metodo GET) un formulario de registro y procesar el registro del usuario
#(metodo POST). Debe retornar 'reg' un mensaje que indica un registro exitoso o 'msj' que indica
#un problema con el registro.

	if request.method == "GET":
		if request.user.is_authenticated():
			return index(request)
		f = RegistroForm()
		return render_to_response("registro.html",
					  {"registroform": f, "msj":""}, 
					  context_instance = RequestContext(request))
	elif request.method == "POST":
		f = RegistroForm(request.POST)
		if f.is_valid():
			try:
				u = User.objects.get(username__exact=f.cleaned_data['username'])
				msj = "El Username que inserto ya existe"
				return render_to_response("registro.html",
							  {"registroform": f, "msj":msj}, 
							  context_instance = RequestContext(request))
			except User.DoesNotExist:
				if f.cleaned_data['clave'] != f.cleaned_data['confirm']:
					msj = "La clave y la confirmacion no concuerdan"
					return render_to_response("registro.html",
								  {"registroform": f, "msj":msj}, context_instance = RequestContext(request))
				else:
					u = User.objects.create_user(username=f.cleaned_data['username'], 
                                                                        password=f.cleaned_data['clave'], 
                                                                        email=f.cleaned_data['email'])
					u.first_name = f.cleaned_data['nombre'] 
					u.last_name = f.cleaned_data['apellido']
					u.dni = f.cleaned_data['dni']
					u.save()
					l=LoginForm()
					return render_to_response("index.html", {"reg":"Usuario registrado exitosamente"})
						
		else:
			return render_to_response("registro.html",
						   {"registroform":f, "msj": "Alguno de los datos provistos tienen un formato equivocado"}, 
					            context_instance = RequestContext(request))
			
#IMPORTANTE: Deberiamos mantener esta vista a pesar de que estemos usando la vista de login generica, 
# es posible que mas adelante nos demos cuenta que necesitamos hacer algo en el login que no se pueda
# hacer con la version generica.
def log_in(request):
#Esta vista permite generar un formulario de login(metodo GET) y procesar el login(metodo POST).
	if request.method == "GET":
		if request.user.is_authenticated():
			return render_to_response("index.html",{"usr":request.user}, context_instance = RequestContext(request))
		else:
			f = LoginForm()
			return render_to_response("log_in.html",{"loginform":f, "msj":""}, context_instance = RequestContext(request))
	elif request.method == "POST":
		f = LoginForm(request.POST)
		if f.is_valid():
			usr = authenticate(username = f.cleaned_data['username'], password = f.cleaned_data['clave'])
			if usr is not None:
				login(request, usr)
				msj = "Bienvenido "+usr.username
				return render_to_response("index.html",{"usr":usr, "msj":msj}, context_instance = RequestContext(request))
			else:
				return render_to_response("log_in.html", {"loginform":f, "msj": "Username o Password invalidos"},context_instance = RequestContext(request))
		else:
				
			return render_to_response("log_in.html", {"loginform":f, "msj": "Formato de Datos Invalidos"},context_instance = RequestContext(request))

def log_out(request):
#Esta vista permite desloguearse de la pagina. Retorna la variable de retorno 'reg' para indicar la salida exitosa del sistema
	logout(request)			
	return render_to_response("index.html",{"reg":"Sesion cerrada con exito"}, context_instance = RequestContext(request))



