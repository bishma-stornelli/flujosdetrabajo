from django.db import models

class CAMPO(models.Model):
    idCampo = models.IntegerField()
    idPaso = models.IntegerField()
    responsable = models.IntegerField()
    tipo = models.IntegerField()
    esObligatorio = models.BooleanField()


class CRITERIO(models.Model):
    idCriterio = models.IntegerField()
    idCamino = models.IntegerField()
    descripcion = models.TextField()
    expresion = models.CharField(max_length=30)
    idPasoInicio = models.IntegerField()
    idPasoDestino = models.IntegerField()


class ESTA_COMPUESTO(models.Model):
    idPaso = models.ForeignKey(PASO)
    idFlujo = models.ForeignKey(FLUJO)


class EVALUA(models.Model):
    idCriterio = models.ForeignKey(CRITERIO)
    idCampo = models.ForeignKey(CAMPO)


class FLUJO(models.Model):
    idFLUJO = models.IntegerField()
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    estado = models.CharField(max_length=30)
    idUnidad = models.IntegerField()


class OBTIENE_DATOS_DE(models.Model):
    idCampo = models.ForeignKey(CAMPO)
    idPlantilla = models.ForeignKey(PLANTILLA)


class PASO(models.Model):
    idPASO = models.IntegerField()
    nombre = models.CharField(max_length=30)
    tipo = models.IntegerField(
    descripcion = models.TextField()
    idFlujo = models.IntegerField()

class REQUIERE(models.Model):
    idCampo = models.ForeignKey()
    idPaso =  models.ForeignKey(PASO)

class TIENE(models.Model):
    idFlujo = models.ForeignKey(FLUJO)
	idUnidad = models.ForeignKey(UNIDAD)