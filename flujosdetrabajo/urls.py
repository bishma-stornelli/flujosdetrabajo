from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'flujosdetrabajo.views.home', name='home'),
    # url(r'^flujosdetrabajo/', include('flujosdetrabajo.foo.urls')),
	url(r'^$', 'usuarios.views.index'),
    url(r'^index$', 'usuarios.views.index'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'log_in.html'}),
    url(r'^logout$', 'usuarios.views.log_out'),
    url(r'^registro$', 'usuarios.views.registro'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
