# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
# clase temporal para insertar datos
class Datos(models.Model):
    med_id = models.AutoField("Id", primary_key=True)
    var_id = models.IntegerField("Variable")
    est_id = models.IntegerField("Estación")
    mar_id = models.IntegerField("Marca Datalogger")
    med_fecha = models.DateTimeField("Fecha")
    med_valor = models.DecimalField("Valor", max_digits=14, decimal_places=6, blank=True, null=True)
    med_maximo = models.DecimalField("Máximo", max_digits=14, decimal_places=6, blank=True, null=True)
    med_minimo = models.DecimalField("Mínimo", max_digits=14, decimal_places=6, blank=True, null=True)
    med_estado = models.NullBooleanField("Estado", default=True)
