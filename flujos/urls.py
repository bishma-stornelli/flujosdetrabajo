from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

urlpatterns = patterns('flujos.views',
    # Examples:
    # url(r'^crear_paso/$', 'crear_paso'),
    url(r'^crear_flujo/$', 'crear_flujo'),
    url(r'^listar_flujos/$', 'listar_flujos'),
    url(r'^index/$', TemplateView.as_view(template_name = 'flujos/base.html'), name='flujo_index'),
    url(r'^copiar_flujo/(?P<flujo_id>\d+)$', 'copiar_flujo'),
    url(r'^consultar_flujo/(?P<flujo_id>\d+)/$', 'consultar_flujo'),
    url(r'^consultar_paso/(?P<paso_id>\d+)/$', 'consultar_paso'),
    url(r'^modificar_flujo/(?P<flujo_id>\d+)/$', 'modificar_flujo'),
    #url(r'^publicar_flujo/(?P<flujo_id>\d+)/$', 'copiar_flujo'),
    url(r'^marcar_obsoleto/(?P<flujo_id>\d+)/$', 'marcar_obsoleto'),
    url(r'^marcar_obsoleto/$', 'listar_flujos_publico'),
    url(r'^publicar_flujo/(?P<flujo_id>\d+)/$', 'publicar_flujo'),
    url(r'^publicar_flujo/$', 'listar_flujos_por_publicar'),
    url(r'^agregar_paso/(?P<flujo_id>\d+)/$', 'agregar_paso'),
    url(r'^modificar_paso/(?P<paso_id>\d+)/$', 'modificar_paso'),
    url(r'^eliminar_paso/(?P<paso_id>\d+)/$', 'eliminar_paso'), 
    url(r'^agregar_campo/(?P<paso_id>\d+)/$', 'agregar_campo'),
    url(r'^modificar_campo/(?P<campo_id>\d+)/$', 'modificar_campo'),
    url(r'^eliminar_campo/(?P<campo_id>\d+)/$', 'eliminar_campo'),
    url(r'^agregar_camino/(?P<flujo_id>\d+)/$', 'agregar_camino'),
    url(r'^listar_caminos/(?P<flujo_id>\d+)/$', 'listar_caminos'),
    url(r'^modificar_camino/(?P<flujo_id>\d+)/(?P<criterio_id>\d+)/$', 'modificar_camino'),
    url(r'^eliminar_camino/(?P<flujo_id>\d+)/(?P<criterio_id>\d+)/$', 'eliminar_camino'),
                       
    url(r'^eliminar_criterio/(?P<criterio_id>\d+)/$', 'eliminar_criterio'),
    url(r'^listar_pasos/(?P<flujo_id>\d+)/$', 'listar_pasos'),
    url(r'^consultar_paso/$', 'copiar_flujo'),
    url(r'^agregar_alerta/(?P<paso_id>\d+)/$', 'agregar_alerta'),
    url(r'^eliminar_alerta/(?P<alerta_id>\d+)/$', 'eliminar_alerta'), 
    url(r'^agregar_informe/(?P<paso_id>\d+)/$', 'agregar_informe'),
    url(r'^consultar_alerta/(?P<alerta_id>\d+)/$', 'consultar_alerta'),
    url(r'^consultar_informe/(?P<informe_id>\d+)/$', 'consultar_informe'),
    url(r'^eliminar_informe/(?P<informe_id>\d+)/$', 'eliminar_informe'),
    url(r'^modificar_alerta/(?P<alerta_id>\d+)/$', 'modificar_alerta'),
    url(r'^modificar_informe/(?P<informe_id>\d+)/$', 'modificar_informe'),
    url(r'^generar_informe/(?P<informe_id>\d+)/$', 'generar_informe'),
)
