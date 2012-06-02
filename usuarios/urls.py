from django.conf.urls import patterns, include, url

urlpatterns = patterns('usuarios.views',
    url(r'^cambiar_clave', 'cambiar_clave'),
    url(r'^consultarPerfil/$', 'consultar_datos_de_usuario'),
    url(r'^modificarDatosUsuario', 'modificarDatosUsuario'),
    # Examples:
    # url(r'^crear_paso/$', 'crear_paso'),

)