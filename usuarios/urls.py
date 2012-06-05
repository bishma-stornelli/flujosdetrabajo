from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout


urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':'usuarios/log_in.html'}),)

    # Examples:
    # url(r'^crear_paso/$', 'crear_paso'),


urlpatterns += patterns('usuarios.views', 
    url(r'^registro/$', 'registro'),
    url(r'^login/', 'django.contrib.auth.views.login', {'template_name':'usuarios/log_in.html'}),
    url(r'^logout/$', logout, {'next_page': '/'}),
    url(r'^cambiar_clave/$', 'cambiar_clave'),
    url(r'^consultar_datos_usuario/$', 'consultar_datos_usuario'),
    url(r'^modificar_datos_usuario/$', 'modificar_datos_usuario'),     
)

