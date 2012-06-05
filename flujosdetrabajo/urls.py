from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView


# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'flujosdetrabajo.views.home', name='home'),
    # url(r'^flujosdetrabajo/', include('flujosdetrabajo.foo.urls')),
    url(r'^$', TemplateView.as_view(template_name='base.html')),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^flujos/', include('flujos.urls')),
    url(r'^usuarios/', include('usuarios.urls')),
    url(r'^unidades/', include('unidades.urls')),
    url(r'^solicitudes/', include('solicitudes.urls')),
    
)

