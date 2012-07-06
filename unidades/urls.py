from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from unidades.forms import RegistroUnidadForm
from unidades.models import Unidad

urlpatterns = patterns('unidades.views',
    # Examples:
    # url(r'^crear_paso/$', 'crear_paso'),
    url(r'^registrar_unidad/$', 'registrar_unidad'),
    url(r'^configurar_unidad/(?P<unidad_id>\d+)/$', 'configurar_unidad'),
    url(r'^otorgar_privilegio/$','otorgar_privilegios'),
    url(r'^solicitar_privilegio/$','solicitar_privilegio'),
    url(r'^listar_privilegios/$','listar_privilegios', name="listar_privilegios"),
    url(r'^listar_unidades/$', ListView.as_view(model=Unidad, template_name='unidades/listar_unidades.html'),name= "unidades_index"),
    url(r'^index/$', TemplateView.as_view(template_name = 'unidades/base.html')),
)
