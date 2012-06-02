from django.conf.urls import patterns, include, url

<<<<<<< HEAD
urlpatterns = patterns('usuarios.views',
    url(r'^cambiar_clave', 'cambiar_clave'),
    url(r'^consultarPerfil/$', 'consultar_datos_de_usuario'),
    url(r'^modificarDatosUsuario', 'modificarDatosUsuario'),
=======
urlpatterns = patterns('',
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name':'usuarios/log_in.html'}),
>>>>>>> cesar_arreglarurl
    # Examples:
    # url(r'^crear_paso/$', 'crear_paso'),

<<<<<<< HEAD
)
=======
urlpatterns += patterns('usuarios.views', 
    url(r'registro/$', 'registro'),
    url(r'logout/$', 'log_out'),
    url(r'cambiar_clave/$', 'cambiar_clave'),
    url(r'ConsultarDatosUsuario/$', 'consultar_datos_usuario'),
    url(r'modificarDatosUsuario/$', 'modificar_datos_usuario'),     
)
>>>>>>> cesar_arreglarurl
