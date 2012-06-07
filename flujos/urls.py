from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from flujos.models import Paso

urlpatterns = patterns('flujos.views',
    # Examples:
    # url(r'^crear_paso/$', 'crear_paso'),
    url(r'^crear_flujo/$', 'crear_flujo'),
    url(r'^listar_flujos/$', 'listar_flujos'),
    url(r'^index/$', TemplateView.as_view(template_name = 'flujos/index.html'), name='flujo_index'),
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
    url(r'^eliminar_paso/(?P<paso_id>\d+)/$', 
        CreateView.as_view(
            model = Paso,
            template_name="flujos/agregar_paso.html",
            success_url="flujos/consultar_paso/%(id)s/"
        )
    ),
    url(r'^agregar_campo/(?P<paso_id>\d+)/$', 'agregar_campo'),
    url(r'^modificar_campo/(?P<campo_id>\d+)/$', 'copiar_flujo'),
    url(r'^eliminar_campo/(?P<campo_id>\d+)/$', 'copiar_flujo'),
    url(r'^agregar_camino/(?P<flujo_id>\d+)/$', 'agregar_camino'),
    url(r'^listar_caminos/(?P<flujo_id>\d+)/$', 'listar_caminos'),
    url(r'^modificar_camino/(?P<flujo_id>\d+)/(?P<criterio_id>\d+)/$', 'modificar_camino'),
    url(r'^eliminar_camino/(?P<flujo_id>\d+)/(?P<criterio_id>\d+)/$', 'eliminar_camino'),
    url(r'^listar_campo    s/$', 'copiar_flujo'),
    url(r'^consultar_campo/$', 'copiar_flujo'),
    url(r'^listar_pasos/(?P<flujo_id>\d+)/$', 'listar_pasos'),
    url(r'^consultar_paso/$', 'copiar_flujo'),

)
