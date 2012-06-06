# -*- coding: utf-8 -*-
from django.db import models
from django.utils import encoding
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

    def clone(self):
        a = Alerta()
        a.descripcion = self.descripcion
        a.mostar_al_llegar = self.mostar_al_llegar
        a.paso = self.paso
        a.plantilla = self.plantilla
        a.miembro_es_receptor = self.miembro_es_receptor
        a.solicitante_es_receptor = self.solicitante_es_receptor
        a.tipos = self.tipos
        return a

class TipoAlerta(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=256)
    
    # Recibe una plantilla renderizada y la envia
    def enviar_alerta(self, plantilla):
        pass

    def clone(self):
        a = TipoAlerta()
        a.nombre = self.nombre
        a.descripcion = self.descripcion
        return a
    
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

    def clone(self):
        a = Campo()
        a.nombre = self.nombre
        a.llenado_por_miembro = self.llenado_por_miembro
        a.llenado_por_solicitante = self.llenado_por_solicitante
        a.tipo = self.tipo
        a.esObligatorio = self.esObligatorio
        a.paso = self.paso
        return a

class Criterio(models.Model):
    paso_origen = models.ForeignKey('Paso', related_name='criterios_origen')
    paso_destino = models.ForeignKey('Paso', related_name='criterios_destino')
    descripcion = models.TextField()
    expresion = models.TextField()
    campos = models.ManyToManyField(Campo)
    
    def clone(self):
        a = Criterio()
        a.paso_origen = self.nombre
        a.paso_destino = self.paso_destino
        a.descripcion = self.descripcion
        a.expresion = self.expresion
        a.campos = self.campos
        return a

class Paso(models.Model):
    nombre = models.CharField(max_length=30)
    TIPO_INICIAL = 1
    TIPO_FINAL = 2
    TIPO_DIVISION = 3
    TIPO_UNION = 4 
    TIPO_NORMAL = 5
    TIPO_CHOICES = (
                    (TIPO_NORMAL, "Normal"),
                    (TIPO_INICIAL, "Inicial"),
                    (TIPO_FINAL, "Final"),
                    (TIPO_DIVISION, "División"),
                    (TIPO_UNION, "Union"))    
    tipo = models.IntegerField(choices=TIPO_CHOICES, default=TIPO_NORMAL)
    descripcion = models.TextField()


    flujo = models.ForeignKey('Flujo', related_name='pasos')
    sucesores = models.ManyToManyField('Paso', 
                                       related_name='predecesores', 
                                       null=True, 
                                       blank=True,
                                       symmetrical=False,
                                       through='Criterio')
    fecha_de_creacion = models.DateTimeField(auto_now = True)
    
    def clone(self):
        a = Paso()
        a.nombre = self.nombre
        a.tipo = self.tipo 
        a.descripcion = self.descripcion
        a.flujo = self.flujo
        a.sucesores = self.sucesores
        a.fecha_de_creacion = self.fecha_de_creacion
        criterios_origen = a.criterios_origen.all()
        criterios_destino = a.criterios_destino.all()
        criterios_origen_nuevo = []
        criterios_destino_nuevo = []
        for i in range(0,a.length):
            criterios_origen_nuevo[i] = criterios_origen[i].clone()
            criterios_origen_nuevo[i].paso_origen = a 
        for i in range(0,c.length):
            criterios_destino_nuevo[i] = criterios_destino[i].clone()
            criterios_destino_nuevo[i].paso_destino = a 
        campos = a.campos.all()
        campos_nuevos = []
        for i in range(0,campos.length):
            campos_nuevos[i] = campos[i].clone()
            campos_nuevos[i].paso = a 
            
        return a

   


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
    
    def __unicode__ (self):
        s = self.nombre
        return s
    
    def clone(self):
        a = Flujo()
        a.nombre = self.nombre
        a.descripcion = self.descripcion
        a.estado = self.estado
        a.unidad = self.unidad
        b = a.pasos.all()
    
        for i in range(0,b.length):
            c[i] = b[i].clone()
            c[i].flujo = a 
        
        return a
    
    def inicial_final(self):
        valido=False
        pasos_final = Paso.objects.filter(flujo=self, tipo = Paso.TIPO_FINAL)
        if pasos_final != Paso.objects.none():
            valido=True
        elif pasos_final == Paso.objects.none():
            valido=False
        pasos_inicial= Paso.objects.filter(flujo=self, tipo = Paso.TIPO_INICIAL)
        if pasos_inicial != Paso.objects.none():
            valido=True
        elif pasos_inicial == Paso.objects.none():
            valido=False
        return valido
    
    def nombre_parecido(self):
        parecidos_nombre = Flujo.objects.filter(nombre=self.nombre,unidad = self.unidad, estado=Flujo.ESTADO_PUBLICO)
        return parecidos_nombre
