from django.conf.urls import patterns, include, url
from django.views.generic.edit import CreateView
from unidades.forms import RegistroUnidadForm
from django.views.generic.base import TemplateView

urlpatterns = patterns('unidades.views',
    # Examples:
    # url(r'^crear_paso/$', 'crear_paso'),
    url(r'^registroUnidad$', 'registroUnidad'),
    url(r'^configurar_unidad/(?P<unidad_id>\d+)/$', 'configurar_unidad'),
    url(r'^solicitudPrivilegio','solicitudPrivilegio'),
    url(r'^otorgarPrivilegio','otorgarPrivilegio'),
    url(r'^index/$', TemplateView.as_view(template_name = 'unidades/index.html') , name= "unidades_index"),
    )