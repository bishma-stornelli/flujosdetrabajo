from django.db import models
from django.contrib.auth.models import User 

class Unidad(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    miembros = models.ManyToManyField(User, related_name="unidades_miembro")
    responsable = models.ForeignKey(User, related_name="unidades_responsable")
    
class SolicitudPrivilegio(models.Model):
    PRIVILEGIO_SOLICITANTE = 1
    PRIVILEGIO_MIEMBRO = 2
    PRIVILEGIO_RESPONSABLE = 3
    PRIVILEGIO_CHOICES = (
            (PRIVILEGIO_SOLICITANTE, 'Solicitante'),
            (PRIVILEGIO_MIEMBRO, 'Miembro de Unidad'),
            (PRIVILEGIO_RESPONSABLE, 'Responsable de Unidad'))
    privilegio = models.IntegerField(choices=PRIVILEGIO_CHOICES)
    solicitante = models.ForeignKey(User,related_name="solicitudes_de_privilegio")
    unidad = models.ForeignKey("Unidad", "solicitudes_de_privilegio")

