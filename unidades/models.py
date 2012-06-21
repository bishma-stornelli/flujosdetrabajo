from django.contrib.auth.models import User
from django.db import models
from django.utils import encoding
#from unidades.groups import responsable
#
#

class Unidad(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    miembros = models.ManyToManyField(User, related_name="unidades_miembros", null=True, blank=True)
    solicitantes = models.ManyToManyField(User, related_name="unidades_solicitantes", null=True, blank=True)
    responsable = models.ForeignKey(User, related_name="unidades_responsable", null=True, blank=True)
    auto_aceptar = models.BooleanField(default=False)

    def __unicode__ (self):
        return self.nombre
    
    # usuario es de tipo django.contrib.auth.models.User
    # permiso es uno de los siguientes:
    #     SolicitudPrivilegio.PRIVILEGIO_SOLICITANTE
    #     SolicitudPrivilegio.PRIVILEGIO_MIEMBRO
    #     SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE
    def permite(self, usuario, permiso):
        if not usuario or not permiso:
            return False
        if permiso == SolicitudPrivilegio.PRIVILEGIO_SOLICITANTE:
            if self in usuario.unidades_solicitantes.all():
                return True
            else:
                return False
        elif permiso == SolicitudPrivilegio.PRIVILEGIO_MIEMBRO:
            if self in usuario.unidades_miembros.all():
                return True
            else:
                return False
        elif permiso == SolicitudPrivilegio.PRIVILEGIO_RESPONSABLE:
            if usuario == self.responsable:
                return True
            else:
                return False
                

#haaa
class SolicitudPrivilegio(models.Model):
    mensaje= models.TextField()
    solicitante = models.ForeignKey(User)
    unidad = models.ForeignKey(Unidad)
    fecha = models.DateField(auto_now=True)
    PRIVILEGIO_SOLICITANTE = 1
    PRIVILEGIO_MIEMBRO = 2
    PRIVILEGIO_RESPONSABLE = 3
    PRIVILEGIO_CHOICES = (
            (PRIVILEGIO_SOLICITANTE, 'Solicitante'),
            (PRIVILEGIO_MIEMBRO, 'Miembro de Unidad'),
            (PRIVILEGIO_RESPONSABLE, 'Responsable de Unidad'))
    privilegio = models.IntegerField(choices=PRIVILEGIO_CHOICES)
    ESTADO_ESPERA = 1
    ESTADO_ACEPTADO = 2
    ESTADO_NEGADO = 3
    ESTADO_CHOICES = (
                      (ESTADO_ESPERA,'En espera'),
                      (ESTADO_ACEPTADO,'Aceptado'),
                      (ESTADO_NEGADO, 'Negado'),
                      )
    estado = models.IntegerField(choices=ESTADO_CHOICES,default=ESTADO_ESPERA)
    class Meta:
        permissions = (
            ("aceptar_privilegio_solicitante", "Puede aceptar los privilegios para ser solicitante"),
            ("aceptar_privilegio_miembro", "Puede aceptar los privilegios para ser miembros de unidad"),
            ("aceptar_privilegio_responsable", "Puede aceptar los privilegios para ser responsables de unidad"),
            # TODOS puedenn realizar solicitud de privilegio
            ("realizar_solicitud", "Puede realizar una solicitud de privilegio"),
            
        )

