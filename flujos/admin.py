from django.contrib import admin
from flujos.models import *

admin.site.register(Alerta)
admin.site.register(TipoAlerta)
admin.site.register(Informe)
admin.site.register(Plantilla)
admin.site.register(Campo)
admin.site.register(Criterio)
admin.site.register(Paso)
admin.site.register(Flujo)

