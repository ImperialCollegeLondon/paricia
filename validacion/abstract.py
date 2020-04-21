# -*- coding: utf-8 -*-

from django.db import models


class ReporteDiarioPrecipitacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField()
    valor = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    porcentaje = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    class_valor = models.CharField(max_length=30)
    class_porcentaje = models.CharField(max_length=30)
    estado = models.BooleanField()


class ReporteDiario(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField()
    valor = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    maximo = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    minimo = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    porcentaje = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    class_valor = models.CharField(max_length=30)
    class_maximo = models.CharField(max_length=30)
    class_minimo = models.CharField(max_length=30)
    class_porcentaje = models.CharField(max_length=30)

    class Meta:
        ### Para que no se cree en la migracion
        managed = False
