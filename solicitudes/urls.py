from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

urlpatterns = patterns('solicitudes.views',
    # Examples:
    # url(r'^crear_paso/$', 'crear_paso'),
	url(r'^listar_solicitudes/$', 'listar_solicitudes'),
    url(r'^index/$', TemplateView.as_view(template_name = 'solicitudes/base.html'), name='solicitudes_index'),
    
)

