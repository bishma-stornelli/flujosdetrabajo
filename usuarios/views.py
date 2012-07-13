# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from usuarios.forms import RegistroForm, LoginForm, UserForm
from usuarios.models import PerfilDeUsuario

def registro(request):
#Esta vista permite generar(metodo GET) un formulario de registro y procesar el registro del usuario
#(metodo POST). Debe retornar 'reg' un mensaje que indica un registro exitoso o 'msj' que indica
#un problema con el registro.
    if request.user.is_authenticated():
        messages.error(request, "Usted ha iniciado sesión. Cierre sesión antes de registrarse.")
        return HttpResponseRedirect("/")
    if request.method == "GET":
        
        f = RegistroForm()
        return render_to_response("usuarios/registro.html",
                      {"registroform": f, "msj":""}, 
                      context_instance = RequestContext(request))
    elif request.method == "POST":
        f = RegistroForm(request.POST)
        if f.is_valid():
            try:
                u = User.objects.get(username__exact=f.cleaned_data['username'])
                messages.error(request,"El nombre de usuario que inserto ya existe.")
                return render_to_response("usuarios/registro.html",
                              {"registroform": f}, 
                              context_instance = RequestContext(request))
            except User.DoesNotExist:
                if f.cleaned_data['clave'] != f.cleaned_data['confirm']:
                    messages.error(request,"La clave y la confirmacion no concuerdan.")
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
                    l=LoginForm()
                    messages.success(request,"Su registro ha sido satisfactorio.")
                    return HttpResponseRedirect("/usuarios/login/")
                        
        else:    
            messages.error(request,"Revise los datos ingresado e intente de nuevo.")
            return render_to_response("usuarios/registro.html",
                           {"registroform":f }, 
                                context_instance = RequestContext(request))
            
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
    messages.success(request, "Sesión cerrada exitosamente.")
    return HttpResponseRedirect(reverse("index"))

@login_required()
def consultar_datos_usuario(request):
    if request.user.is_authenticated():
        u= User.objects.get(username=request.user)
        perfil= PerfilDeUsuario.objects.all()
        return render_to_response("usuarios/consultar_datos_usuario.html",{"usr":u, "perfil":perfil}, context_instance = RequestContext(request))

    else:
        f = LoginForm()
        return render_to_response("usuarios/log_in.html",{"loginform":f}, context_instance = RequestContext(request))

@login_required()
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
            return render_to_response("/")

    else:
        f = LoginForm()
        return render_to_response("usuarios/log_in.html",{"loginform":f}, context_instance = RequestContext(request))

@login_required
def modificar_datos_usuario(request):
    if request.method == "GET":
        user_form = UserForm(instance=request.user)
        return render_to_response('usuarios/modificar_datos_usuario.html', { 'user_form': user_form }, context_instance=RequestContext(request))    

    else:
        u= request.user
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            u.first_name=user_form.cleaned_data['first_name']
            u.last_name=user_form.cleaned_data['last_name']
            u.email=user_form.cleaned_data['email']
            u.dni = user_form.cleaned_data['dni']
            u.save()
            messages.success(request,"Perfil Actualizado Exitosamente")
            return render_to_response('usuarios/modificar_datos_usuario.html', { 'user_form': user_form }, context_instance=RequestContext(request))
        else:
            user_form = UserForm(instance=request.user)
            return render_to_response('usuarios/modificar_datos_usuario.html', { 'user_form': user_form}, context_instance=RequestContext(request))


