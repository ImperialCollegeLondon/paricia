# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from variable.models import Variable
from estacion.models import Estacion
from marca.models import Marca
from django.urls import reverse


# clase para almacenar los datos crudos del sistema
class Medicion(models.Model):
    med_id = models.AutoField("Id", primary_key=True)
    var_id = models.ForeignKey(
        Variable,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Variable")
    est_id = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación")
    mar_id = models.ForeignKey(
        Marca,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Marca Datalogger"
    )
    med_fecha = models.DateTimeField("Fecha", db_index=True)
    med_valor = models.DecimalField("Valor", max_digits=14, decimal_places=6, blank=True, null=True)
    med_maximo = models.DecimalField("Máximo", max_digits=14, decimal_places=6, blank=True, null=True)
    med_minimo = models.DecimalField("Mínimo", max_digits=14, decimal_places=6, blank=True, null=True)
    med_estado = models.NullBooleanField("Estado", default=True)

    def __str__(self):
        return str(self.med_fecha)

    def get_absolute_url(self):
        return reverse('medicion:medicion_index')

    class Meta:
        ordering = ('med_fecha',)
