from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
urlpatterns = patterns('flujos.views',
    # Examples:
    # url(r'^crear_paso/$', 'crear_paso'),
    url(r'^crear_flujo/(?P<unidad_id>\d+)/$', 'crear_flujo'),
    url(r'^listar_flujos/(?P<unidad_id>\d+)/$', 'listar_flujos'),
    url(r'^index/$', TemplateView.as_view(template_name = 'flujos/index.html'), name='flujo_index'),
    url(r'^copiar_flujo/(?P<flujo_id>\d+)$', 'copiar_flujo'),
    url(r'^consultar_flujo/(?P<flujo_id>\d+)/$', 'consultar_flujo'),
    url(r'^modificar_flujo/(?P<flujo_id>\d+)/$', 'modificar_flujo'),
    url(r'^publicar_flujo/(?P<flujo_id>\d+)/$', 'copiar_flujo'),
    url(r'^marcar_obsoleto/(?P<flujo_id>\d+)/$', 'copiar_flujo'),
    url(r'^agregar_paso/(?P<flujo_id>\d+)/$', 'copiar_flujo'),
    url(r'^modificar_paso/(?P<paso_id>\d+)/$', 'modificar_paso'),
    url(r'^eliminar_paso/(?P<paso_id>\d+)/$', 'copiar_flujo'),
    url(r'^agregar_campo/(?P<paso_id>\d+)/$', 'agregar_campo'),
    url(r'^modificar_campo/(?P<campo_id>\d+)/$', 'copiar_flujo'),
    url(r'^eliminar_campo/(?P<campo_id>\d+)/$', 'copiar_flujo'),
    url(r'^agregar_camino/$', 'copiar_flujo'),
    url(r'^modificar_camino/$', 'copiar_flujo'),
    url(r'^eliminar_camino/$', 'copiar_flujo'),
    url(r'^listar_caminos/$', 'copiar_flujo'),
    url(r'^listar_campos/$', 'copiar_flujo'),
    url(r'^consultar_campos/$', 'copiar_flujo'),
    url(r'^listar_pasos/(?P<flujo_id>\d+)/$', 'listar_pasos'),
    url(r'^consultar_paso/$', 'copiar_flujo'),

)
