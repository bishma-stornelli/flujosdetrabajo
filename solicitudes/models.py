# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from flujos.models import Paso, Campo, Flujo
from django.template.defaultfilters import default

class Solicitud(models.Model):
    flujo = models.ForeignKey(Flujo)
    solicitante = models.ForeignKey(User, related_name="solicitantes")
    fecha_de_solicitud = models.DateTimeField(auto_now_add=True)
    pasos = models.ManyToManyField(Paso,through='Registro')
    campos = models.ManyToManyField(Campo, through='Respuesta')
    ESTADO_ACTIVO = 1;
    ESTADO_RETIRADO = 2;
    estado_choices = ((ESTADO_ACTIVO,'Activo'),(ESTADO_RETIRADO,'Retirado'))
    estado = models.IntegerField(choices=estado_choices, default=1)

class Respuesta(models.Model):
    solicitud = models.ForeignKey(Solicitud, related_name="respuestas")
    campo = models.ForeignKey(Campo, related_name="respuestas")
    valor = models.TextField() # En caso de ser archivo se guarda la ruta de este

class Registro(models.Model):
    solicitud = models.ForeignKey(Solicitud, related_name="registros")
    paso = models.ForeignKey(Paso, related_name="registros")
    fecha_de_entrada = models.DateTimeField("Fecha de entrada", auto_now_add=True)
    fecha_de_salida = models.DateTimeField(null=True)
    ESTADO_COMPLETO = 1;
    ESTADO_EN_PROCESO = 2;
    estado_choices = ((ESTADO_COMPLETO,'Completo'),(ESTADO_EN_PROCESO,'En proceso'))
    estado = models.IntegerField(choices=estado_choices, default=ESTADO_EN_PROCESO)
