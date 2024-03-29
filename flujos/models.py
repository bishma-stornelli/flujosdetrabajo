# -*- coding: utf-8 -*-
from django.db import models
from django.utils import encoding
from unidades.models import Unidad

# Create your models here.
class Alerta(models.Model):
    nombre = models.CharField(max_length=30)
    mostar_al_llegar = models.BooleanField(help_text="Si se marca, la alerta será "
        + "mostrada al llegar al paso. Sino, será mostrada al salir del paso.")
    paso = models.ForeignKey("Paso",related_name="alertas_paso")
    miembro_es_receptor = models.BooleanField()
    solicitante_es_receptor = models.BooleanField()
    tipos = models.ManyToManyField('TipoAlerta', related_name='alertas', verbose_name="Tipo de alerta")
    formato = models.TextField()

    def clone(self):
        a = Alerta()
        a.descripcion = self.descripcion
        a.mostar_al_llegar = self.mostar_al_llegar
        a.paso = self.paso
        a.miembro_es_receptor = self.miembro_es_receptor
        a.solicitante_es_receptor = self.solicitante_es_receptor
        a.tipos = self.tipos
        return a

class TipoAlerta(models.Model):
    nombre = models.CharField(max_length=30)
    # Recibe una plantilla renderizada y la envia
    def enviar_alerta(self, plantilla):
        pass

    def clone(self):
        a = TipoAlerta()
        a.nombre = self.nombre
        a.descripcion = self.descripcion
        alertas = a.alertas.all()
        alertas_nuevas = []
        for i in range(0,alertas.length):
            #alertas_nuevas[i] = alerta[i].clone()
            alertas_nuevas[i].alertas = a 
        return a
    
    def __str__(self):
        return self.nombre
    
    
class Informe(models.Model):
    nombre = models.CharField(max_length=30)
    paso = models.ForeignKey("Paso", related_name="informes")
    miembro_es_receptor = models.BooleanField()
    solicitante_es_receptor = models.BooleanField()
    formato = models.TextField()

    def clone(self):
        a = Informe()
        a.descripcion = self.descripcion
        a.paso = self.paso
        a.miembro_es_receptor = self.miembro_es_receptor
        a.solicitante_es_receptor = self.solicitante_es_receptor
        return a 
    
   
#class Plantilla(models.Model):
#    formato = models.TextField()
#    
#    def clone(self):
#        a = Plantilla()
#        a.formato = self.formato
#        informe = a.plantillas_de_informe.all()
#        informe_nuevos = []
#        for i in range(0,informe.length):
#            informe_nuevos[i] = informe[i].clone()
#            informe_nuevos[i].plantilla = a 
#        alerta = a.plantillas_de_alerta.all()
#        alertas_nuevas = []
#        for i in range(0,informe.length):
#            alertas_nuevas[i] = alerta[i].clone()
#            alertas_nuevas[i].plantilla = a 
#        return a 
#
#    def __str__(self):
#        return self.formato


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
    #TIPO_SOLICITANTE = 1
    #TIPO_MIEMBRO= 2
    #TIPO_CHOICES2 = (
     #               (TIPO_SOLICITANTE, "Solicitante"),
     #               (TIPO_MIEMBRO, "Miembro de Unidad"))
    #responsable = models.IntegerField(choices=TIPO_CHOICES2, null=True, blank=True)

    def clone(self):
        a = Campo()
        a.nombre = self.nombre
        a.llenado_por_miembro = self.llenado_por_miembro
        a.llenado_por_solicitante = self.llenado_por_solicitante
        a.tipo = self.tipo
        a.esObligatorio = self.esObligatorio
        a.paso = self.paso
        return a

    def __str__(self):
        return self.nombre

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
        #for i in range(0,c.length):
        #    criterios_destino_nuevo[i] = criterios_destino[i].clone()
        #    criterios_destino_nuevo[i].paso_destino = a 
        alertas = a.alertas.all()
        alertas_nuevas = []
        for i in range(0,alertas.length):
            alertas_nuevas[i] = alertas[i].clone()
            alertas_nuevas[i].paso = a 
        informes = a.informes.all()
        informe_nuevos = []
        for i in range(0,informes.length):
            informe_nuevos[i] = informes[i].clone()
            informe_nuevos[i].paso = a 
        campos = a.campos.all()
        campos_nuevos = []
        for i in range(0,campos.length):
            campos_nuevos[i] = campos[i].clone()
            campos_nuevos[i].paso = a 
            
        return a

    def __str__(self):
        return self.nombre
   


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
    
        #for i in range(0,b.length):
        #    c[i] = b[i].clone()
        #    c[i].flujo = a 
        #a.estado = default
        self.estado = "OBSOLETO"
        
        return a

    def is_valid(self):
        errores = []
        if len(Paso.objects.filter(flujo=self, tipo = Paso.TIPO_INICIAL)) != 1:
            errores.append("El flujo no tiene paso inicial.")
        if len(Paso.objects.filter(flujo=self, tipo = Paso.TIPO_FINAL)) == 0:
            errores.append("El flujo no tiene paso final.")
        if len(errores) == 0:
            inicial = Paso.objects.get(tipo = Paso.TIPO_INICIAL)
            pasosAbiertos = [inicial]
            recorrido = []
            while pasosAbiertos:
                pas = pasosAbiertos.pop()
                if not pas in recorrido:
                    recorrido.append(pas)
                p = list(pas.sucesores.all())
                if len(p) == 0 and pas.tipo != Paso.TIPO_FINAL:
                    errores.append("El paso '%s' no tiene sucesores y no es de tipo final" % pas.nombre)
                for k in p:
                    if k not in pasosAbiertos and k not in recorrido:
                        pasosAbiertos.append(k)
            for p in self.pasos.all():
                if not p in recorrido:
                    errores.append("El paso '%s' no es alcanzable desde el paso inicial." % p.nombre)
        if len(Flujo.objects.filter(nombre=self.nombre,unidad = self.unidad, estado=Flujo.ESTADO_PUBLICO)) > 0:
            errores.append("Ya existe un flujo público con el mismo nombre. Marque el otro como obsoleto primero.")
        return errores
