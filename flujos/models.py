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