# -*- coding: utf-8 -*-
from django.db import models
# PV necesitamos poder vincular con el User
from django.contrib.auth.models import User
#import settings
#import uuid
#import os


class Lugar(models.Model):
    """Un lugar es una ciudad, canton, parroquia, que requiera ser mencionado"""
    nombre = models.CharField(max_length=1024, unique=True)

    class Meta:
        verbose_name_plural = u"lugares"

    def __unicode__(self):
        return "%s" % self.nombre


class Recurso(models.Model):
    """Un recurso es algo que usará el empleado para cumplir con su trabajo"""
    UNIDADES = (
        (u"m", u"metro"),
        (u"h", u"hora"),
        (u"u", u"unidad"),
        (u"u", u"unidad"),
    )
    recurso = models.CharField(max_length=1024, null=False)
    unidad = models.CharField(max_length=50, null=False, choices=UNIDADES)
    costo = models.DecimalField(max_digits=8, decimal_places=2)

    def __unicode__(self):
        return "%s(%s) @ $%s" % (self.recurso, self.unidad, self.costo)


class RecursoXActividad(models.Model):
    """Una relación que lleva la cuenta de que recursos usa alguna actividad"""
    cant = models.IntegerField('cantidad', choices=[(n, u"%s" % n) for n in range(1, 50)], default=u"1")
    recurso = models.ForeignKey(Recurso)
    actividad = models.ForeignKey('Actividad', related_name="recursos")


class Actividad(models.Model):
    """Una actividad es una tarea/componente de un proyecto"""
    DURACIONES = (
        (15, u"15 min"),
        (30, u"30 min"),
        (60, u"1 hora"),
        (120, u"2 horas"),
    )

    class Meta:
        verbose_name_plural = u"actividades"  # hacer que el admin muestre bien las inflectiones

    actividad = models.CharField(max_length=2048, null=False)
    objetivos = models.CharField(max_length=2048, null=False)
    lugar = models.ForeignKey('Lugar', null=True, blank=True)
    fecha_hora = models.DateTimeField(u"día y hora")
    duracion = models.IntegerField(u"duración", blank=False, choices=DURACIONES, default=u"60")
    fecha_creacion = models.DateTimeField(u"fecha creación", auto_now_add=True, blank=False)
    proyecto = models.ForeignKey('Proyecto', related_name="actividades", null=True, blank=True)
    empleado = models.ForeignKey('Empleado', related_name="actividades")

    def get_url_absoluta(self):
        return "/actividad/%s" % self.id

    def __unicode__(self):
        return self.actividad


class Proyecto(models.Model):
    """proyecto"""

    ESTADOS = (
        (u"ejecucion", u"ejecucion"),
        (u"terminado", u"terminado"),
        (u"cancelado", u"cancelado")
    )

    nombre = models.CharField(max_length=1024, null=False)
    estado = models.CharField(max_length=255, choices=ESTADOS)
    fecha_inicio = models.DateField('fecha inicio', null=True)  # cuando inicia el proyecto
    fecha_fin = models.DateField('fecha fin', null=True)
    porcentaje = models.PositiveIntegerField(default=0)  # el porcentaje de avance (podemos hacerlo en función a los dias transcurridos)
    empleado = models.ForeignKey('Empleado', related_name="proyectos")
    #actividades = models.OneToMany(Recurso)

    def __unicode__(self):
        return self.nombre


class Empleado(models.Model):
    user = models.ForeignKey(User, unique=True)
    url = models.URLField("Website", blank=True)
    departamento = models.CharField(max_length=50, blank=True)

    def get_actividades(self):
        """obtener las actividades en un consolidado de este usuario """
        return self.actividades.filter(empleado=self).all()

    def __unicode__(self):
        return "%s %s (%s)" % (self.user.first_name, self.user.last_name, self.user.username)

# PV crearle el profile a un usuario si es que no lo tiene
User.profile = property(lambda u: Empleado.objects.get_or_create(user=u)[0])
