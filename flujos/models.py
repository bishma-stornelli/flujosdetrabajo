# -*- coding: utf-8 -*-
from django.db import models
from unidades.models import Unidad

# Create your models here.
class Alerta(models.Model):
    
    descripcion = models.TextField()
    mostar_al_llegar = models.BooleanField(help_text="Si se marca, la alerta será "
        + "mostrada al llegar al paso. Sino, será mostrada al salir del paso.")
    paso = models.ForeignKey('Paso')
    plantilla = models.ForeignKey("Plantilla")
    miembro_es_receptor = models.BooleanField()
    solicitante_es_receptor = models.BooleanField()
    tipos = models.ManyToManyField('TipoAlerta', related_name='alertas')

class TipoAlerta(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=256)
    
    # Recibe una plantilla renderizada y la envia
    def enviar_alerta(self, plantilla):
        pass
    
class Informe(models.Model):
    descripcion = models.TextField()
    paso = models.ForeignKey("Paso")
    plantilla = models.ForeignKey("Plantilla")
    miembro_es_receptor = models.BooleanField()
    solicitante_es_receptor = models.BooleanField()
   
class Plantilla(models.Model):
    formato = models.TextField()

class Campo(models.Model):
    nombre = models.CharField(max_length=30)
    llenado_por_miembro = models.BooleanField()
    llenado_por_solicitante = models.BooleanField()
    TIPO_TEXT = 1
    TIPO_TEXTAREA = 2
    TIPO_CHECKBOX = 3
    TIPO_FILE = 4
    TIPO_NUMBER = 5
    TIPO_EMAIL = 6
    TIPO_FECHA = 7
    TIPO_CHOICES = (
                    (TIPO_TEXT, "Campo de texto"),
                    (TIPO_TEXTAREA, "Área de texto"),
                    (TIPO_CHECKBOX, "Caja de verificación"),
                    (TIPO_FILE, "Archivo"),
                    (TIPO_NUMBER, "Número"),
                    (TIPO_EMAIL, "Correo"),
                    (TIPO_FECHA, "Fecha"))
    tipo = models.IntegerField(choices=TIPO_CHOICES)
    esObligatorio = models.BooleanField()
    paso = models.ForeignKey('Paso', related_name="campos")

class Criterio(models.Model):
    paso_origen = models.ForeignKey('Paso', related_name='criterios_origen')
    paso_destino = models.ForeignKey('Paso', related_name='criterios_destino')
    descripcion = models.TextField()
    expresion = models.TextField()
    campos = models.ManyToManyField(Campo)

class Paso(models.Model):
    nombre = models.CharField(max_length=30)
    TIPO_INICIAL = 1
    TIPO_FINAL = 2
    TIPO_DIVISION = 3
    TIPO_UNION = 4
    TIPO_CHOICES = (
                    (TIPO_INICIAL, "Inicial"),
                    (TIPO_FINAL, "Final"),
                    (TIPO_DIVISION, "División"),
                    (TIPO_UNION, "Union"))    
    tipo = models.IntegerField(choices=TIPO_CHOICES)
    descripcion = models.TextField()
    flujo = models.ForeignKey('Flujo')
    sucesores = models.ManyToManyField('Paso', 
                                       related_name='predecesores', 
                                       null=True, 
                                       blank=True,
                                       symmetrical=False,
                                       through='Criterio')

class Flujo(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    ESTADO_BORRADOR = 1
    ESTADO_PUBLICO = 2
    ESTADO_OBSOLETO = 3
    ESTADO_CHOICES = ((ESTADO_BORRADOR, "Borrador"),
                    (ESTADO_PUBLICO, "Publico"),
                    (ESTADO_OBSOLETO, "Obsoleto"))
    estado = models.IntegerField(choices=ESTADO_CHOICES, default=ESTADO_BORRADOR)
    unidad = models.ForeignKey(Unidad,related_name='flujos')
