from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
urlpatterns = patterns('flujos.views',
    # Examples:
    # url(r'^crear_paso/$', 'crear_paso'),
    url(r'^crear_flujo/(?P<unidad_id>\d+)/$', 'crear_flujo'),
)
urlpatterns = patterns('flujos.views',
    # Examples:
    # url(r'^crear_paso/$', 'crear_paso'),
    url(r'^crear_flujo/$', 'crear_flujo'),
)

urlpatterns += patterns('flujos.views',
    # ESTA ES LA LISTA DE URLS QUE NECESITAMOS PARA LA TERCERA ITERACION
    # SIRVEN A MANERA DE GUIA, NO SON DEFINITIVOS
    # SI NECESITAN MAS O MENOS PARAMETROS PARA HACERLO FUNCIONAR LOS ANADEN
    url(r'^listar_flujos/(?P<unidad_id>\d+)/$', 'listar_flujos'),
    url(r'^index/$', TemplateView.as_view(template_name = 'flujos/index.html')),
    url(r'^copiar_flujo/(?P<flujo_id>\d+)$', 'copiar_flujo'),
    url(r'^consultar_flujo/(?P<flujo_id>\d+)/$', 'consultar_flujo'),
    url(r'^modificar_flujo/(?P<flujo_id>\d+)/$', 'copiar_flujo'),
    url(r'^publicar_flujo/(?P<flujo_id>\d+)/$', 'copiar_flujo'),
    url(r'^marcar_obsoleto/(?P<flujo_id>\d+)/$', 'copiar_flujo'),
    url(r'^agregar_paso/(?P<flujo_id>\d+)/$', 'copiar_flujo'),
    url(r'^modificar_paso/(?P<paso_id>\d+)/$', 'copiar_flujo'),
    url(r'^eliminar_paso/(?P<paso_id>\d+)/$', 'copiar_flujo'),
    url(r'^agregar_campo/(?P<paso_id>\d+)$', 'copiar_flujo'),
    url(r'^modificar_campo/(?P<campo_id>\d+)/$', 'copiar_flujo'),
    url(r'^eliminar_campo/(?P<campo_id>\d+)/$', 'copiar_flujo'),
    url(r'^agregar_camino/$', 'copiar_flujo'),
    url(r'^modificar_camino/$', 'copiar_flujo'),
    url(r'^eliminar_camino/$', 'copiar_flujo'),
    url(r'^listar_caminos/$', 'copiar_flujo'),
    url(r'^listar_campos/$', 'copiar_flujo'),
    url(r'^consultar_campos/$', 'copiar_flujo'),
    url(r'^listar_pasos/$', 'copiar_flujo'),
    url(r'^consultar_paso/$', 'copiar_flujo'),

)
