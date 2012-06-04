from django.conf.urls import patterns, include, url
from django.views.generic.edit import CreateView
from unidades.forms import RegistroUnidadForm
from django.views.generic.base import TemplateView

urlpatterns = patterns('unidades.views',
    # Examples:
    # url(r'^crear_paso/$', 'crear_paso'),
    url(r'^registrar_unidad/$', 'registrar_unidad'),
    url(r'^configurar_unidad/(?P<unidad_id>\d+)/$', 'configurar_unidad'),
    url(r'^otorgar_privilegio/$','otorgar_privilegio'),
    url(r'^solicitud_privilegio/$','solicitud_privilegio'),
    url(r'^index/$', TemplateView.as_view(template_name = 'unidades/index.html') , name= "unidades_index"),
    )
