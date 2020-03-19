# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class ConsultaGenericaFechaHoraGrafico(models.Model):
    fila = models.AutoField(primary_key=True)
    id = models.IntegerField()
    fecha = models.DateTimeField()
    valor = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    salto = models.BooleanField()

    class Meta:
        # Para que no se cree en la migracion
        # abstract = True
        managed = False


class ConsultaGenericaFechaHora(models.Model):
    fecha = models.DateTimeField(primary_key=True)
    valor = models.DecimalField(max_digits=14, decimal_places=6, null=True)

    class Meta:
        # Para que no se cree en la migracion
        managed = False


class ConsultaGenericaFecha(models.Model):
    fecha = models.DateField(primary_key=True)
    valor = models.DecimalField(max_digits=14, decimal_places=6, null=True)

    class Meta:
        # Para que no se cree en la migracion
        managed = False
