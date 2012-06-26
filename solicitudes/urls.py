from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

urlpatterns = patterns('solicitudes.views',
    # Examples:
    # url(r'^crear_paso/$', 'crear_paso'),
	url(r'^listar_solicitudes/$', 'listar_solicitudes'),
    url(r'^crear_solicitud/$', 'crear_solicitud'),
    url(r'^index/$', TemplateView.as_view(template_name = 'solicitudes/base.html'), name='solicitudes_index'),
    url(r'^consultar_solicitud/(?P<solicitud_id>\d+)/$', 'consultar_solicitud'),
    url(r'^agregar_dato/$', 'agregar_dato'),
    url(r'^completar_dato/$', 'completar_dato'),
    url(r'^avanzar_solicitud/$', 'avanzar_solicitud'),
    url(r'^retirar_solicitud/$', 'retirar_solicitud'),
    url(r'^generar_informe/$', 'generar_informe')
)

