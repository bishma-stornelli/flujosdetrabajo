from usuarios.models import *
from unidades.models import SolicitudPrivilegio, Unidad
from django.contrib import admin

admin.site.register(PerfilDeUsuario)
admin.site.register(Unidad)
admin.site.register(SolicitudPrivilegio)

