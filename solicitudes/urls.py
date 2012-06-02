from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('solicitudes.views',
    # Examples:
    # url(r'^crear_paso/$', 'crear_paso'),
    url(r'^index/$', TemplateView.as_view(template_name = 'solicitudes/index.html')),
    
)

