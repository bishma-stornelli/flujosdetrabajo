from django.contrib.auth.models import User
from django.db import models

class Unidad(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    miembros = models.ManyToManyField(User, related_name="unidades_miembro")
    responsable = models.ForeignKey(User, related_name="unidades_responsable")

    def __unicode__(self):
        return self.nombre

#haaa
class SolicitudPrivilegio(models.Model):
    posibles_privilegios = (
			      ("Miembro de Unidad","Miembro de Unidad"),
			      ("Responsable de Unidad","Responsable de Unidad"),
			      ("Solicitante","Solicitante"),
			    )
    posibles_estados = (
                            ("En espera","En espera"),
                            ("Aceptado","Aceptado"),
                        )
    estado = models.CharField(max_length=30,choices = posibles_estados,default="En espera")
    privilegio = models.CharField(max_length=30,choices = posibles_privilegios)
    mensaje= models.TextField()
    solicitante = models.ForeignKey(User)
    unidad = models.ForeignKey(Unidad)
    fecha = models.DateField(auto_now=True)
    #PRIVILEGIO_SOLICITANTE = 1
    #PRIVILEGIO_MIEMBRO = 2
    #PRIVILEGIO_RESPONSABLE = 3
    #PRIVILEGIO_CHOICES = (
    #        (PRIVILEGIO_SOLICITANTE, 'Solicitante'),
    #        (PRIVILEGIO_MIEMBRO, 'Miembro de Unidad'),
    #        (PRIVILEGIO_RESPONSABLE, 'Responsable de Unidad'))
    #privilegio = models.IntegerField(choices=PRIVILEGIO_CHOICES)
    class Meta:
        permissions = (
            ("aceptar_privilegio_solicitante", "Puede aceptar los privilegios para ser solicitante"),
            ("aceptar_privilegio_miembro", "Puede aceptar los privilegios para ser miembros de unidad"),
            ("aceptar_privilegio_responsable", "Puede aceptar los privilegios para ser responsables de unidad"),
            ("realizar_solicitud", "Puede realizar una solicitud de privilegio"),
            
        )

