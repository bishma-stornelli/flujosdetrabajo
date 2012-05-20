# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User 

class Solicitud(models.Model):
    flujo = models.ForeignKey('flujos.models.Flujo')
    solicitantes = models.ForeignKey(User)
    fecha_de_solicitud = models.DateTimeField("Date published")
    pasos = models.ManyToManyField('flujos.models.Paso',through='Registro')
    campos = models.ManyToManyField('flujos.models.Campo', through='Respuesta')

class Respuesta(models.Model):
    valor = models.TextField() # En caso de ser archivo se guarda la ruta de este

class Registro(models.Model):
    fecha_de_entrada = models.DateTimeField("Fecha de entrada", auto_now_add=True)
    fecha_de_salida = models.DateTimeField(null=True)
    ESTADO_COMPLETO = 1;
    ESTADO_EN_PROCESO = 2;
    estado_choices = ((ESTADO_COMPLETO,'Completo'),(ESTADO_EN_PROCESO,'En proceso'))
    estado = models.IntegerField(choices=estado_choices)
