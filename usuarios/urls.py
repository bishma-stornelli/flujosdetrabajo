from django.conf.urls import patterns, include, url

urlpatterns = patterns('usuarios.views',
    # Examples:
    # url(r'^crear_paso/$', 'crear_paso'),
    
)

urlpatterns += patterns('usuarios.views',
    url(r'^cambiar_clave', 'cambiar_clave'),
    url(r'^ConsultarDatosUsuario', 'ConsultarDatosUsuario'),
    url(r'^modificarDatosUsuario', 'modificarDatosUsuario'),     
)
