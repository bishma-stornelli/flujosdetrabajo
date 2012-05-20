# -*- coding: utf-8 -*-
from django.db import models

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
    paso = models.ForeignKey(Paso)
    criterio = models.ForeignKey(Criterio)
    planilla = models.ForeignKey(Plantilla)
    solicitud = models.ForeignKey('solicitudes.models.Solicitud')
	nombre = models.CharField(max_length=30)
    responsable = models.IntegerField()
    tipo = models.IntegerField()
    esObligatorio = models.BooleanField()

class Criterio(models.Model):
    campo = models.ForeignKey(Campo)
    descripcion = models.TextField()
    expresion = models.CharField(max_length=30)
	
class Paso(models.Model):	
	flujo = models.ForeignKey()
	solicitud = models.ForeignKey()
    nombre = models.CharField(max_length=30)
    tipo = models.IntegerField(
    descripcion = models.TextField()
	alertas = models.ManyToManyField(Alerta)
	informes = models.ManyToManyField(Informe)
	campos = models.ManyToManyField(Campo)

class Flujo(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    estado = models.CharField(max_length=30)
    unidad = models.ForeignKey('unidades.models.Unidad')
	solicitud = models.ManyToManyField('solicitudes.models.Solicitud')
	paso = models.ManyToManyField(Paso)
	
class Camino(models.Model):
	paso_origen = models.ManyToManyField(Paso, through = 'Criterio')
	paso_destino = models.ManyToManyField(Paso)