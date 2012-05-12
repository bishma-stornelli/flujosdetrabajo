from django.db import models

class Solicitud(models.Model):
    idSOLICITUD = models.IntegerField()
    idFlujo = models.ForeignKey(Flujo)
    solicitante = models.ForeignKey(Solicitante)
    fechaSolicitud = models.DateTimeField("Date published")
    idPasos = models.ManyToMany(PASO,through='REGISTRO')    

class Respuesta(models.Model):
    valor = models.CharField( max_length = 20)

class Registro(models.Model):
    fechaEntrada = models.DateField(_("Fecha de entrada"), default = datetime.date.today)
    fechaSalida = models.CharField( max_length = 15)
    estado = models.CharField( max_length = 20)
 
class Participa(models.Model)
    solp = models.ForeignKey(Flujo)

class Responde(models.Model):
    idSolicitudes = models.ManyToManyField(Solicitud)
    nombres = models.ManyToManyField(Campo)

    
