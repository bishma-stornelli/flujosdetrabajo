from django.conf.urls import patterns, include, url
from django.contrib import admin
import flujos.urls


# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'flujosdetrabajo.views.home', name='home'),
    # url(r'^flujosdetrabajo/', include('flujosdetrabajo.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'usuarios.views.index'),
    url(r'^index/$', 'usuarios.views.index'),
   
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
    
    # Asi se importan urls de otros modulos
    url(r'^flujos/', include('flujos.urls')),
    url(r'^usuarios/', include('usuarios.urls')),
    url(r'^unidades/', include('unidades.urls')),
    url(r'^solicitudes/', include('solicitudes.urls')),
    
)

