from django.db import models
from django.contrib.auth.models import User, UserManager

class ALERTA(models.Model):
    responsable = models.IntegerField()
    tipo =  models.IntegerField()
    descripcion = models.TextField()
    llegada =  models.BooleanField()
    
class INFORME(models.Model):
    descripcion = models.TextField()
    responsable = models.IntegerField()
    
class PLANTILLA(models.Model):
    formato =  models.CharField(max_length=30)
    
class PERFIL(User):
    dni = models.CharField(max_length=30)
    objects = UserManager() 

class PerfilDeUsuario(models.Model):
    user = models.OneToOneField(User)
    dni =  models.IntegerField()

    
class PRODUCEALERTA(models.Model):
    idPaso = models.ForeignKey(PASO)
    idAlerta = models.ForeignKey(ALERTA)

class GENERA(models.Model):
    idPaso = models.ForeignKey(PASO)
    idInforme = models.ForeignKey(INFORME)

class IBASADAEN(models.Model):
    idInforme = models.ForeignKey(INFORME)
    idPlantilla = models.ForeignKey(PLANTILLA)
    
class ABASADAEN(models.Model):
    idAlerta = models.ForeignKey(ALERTA)
    idPlantilla = models.ForeignKey(PLANTILLA)
