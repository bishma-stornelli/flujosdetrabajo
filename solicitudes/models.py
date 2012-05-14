# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User 
from flujos.models import Flujo, Paso, Campo

class Solicitud(models.Model):
    flujo = models.ForeignKey(Flujo)
    solicitantes = models.ForeignKey(User)
    fecha_de_solicitud = models.DateTimeField("Date published")
    pasos = models.ManyToMany(Paso,through='Registro')
    campos = models.MantyToMany(Campo, through='Respuesta')

class Respuesta(models.Model):
    valor = models.TextField() # En caso de ser archivo se guarda la ruta de este

class Registro(models.Model):
    fecha_de_entrada = models.DateTimeField("Fecha de entrada", auto_now_add=true)
    fecha_de_salida = models.DateTimeField(null=True)
    estado_choices = (('c','Completo'),('e','En proceso'))
    estado = models.CharField( max_length = 20)
