from django.conf.urls import patterns, include, url
from django.views.generic.edit import CreateView
from unidades.forms import RegistroUnidadForm

urlpatterns = patterns('unidades.views',
    # Examples:
    # url(r'^crear_paso/$', 'crear_paso'),
    url(r'^registroUnidad$', 'registroUnidad'),
    url(r'^configurar_unidad/$', 'configurar_unidad'),
    url(r'^solicitud_privilegio','solicitud_privilegio'),
    url(r'^otorgar_privilegio','otorgar_privilegio'),
)