# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from variable.models import Variable
from estacion.models import Estacion
from django.urls import reverse


# Create your models here.
# validar el porcentaje de registro de la estacion por variable
class Validacion(models.Model):
    val_id = models.AutoField("Id", primary_key=True)
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
    val_fecha = models.DateField("Fecha")
    val_num_dat = models.IntegerField("Número de Datos", default=0)
    val_fre_reg = models.IntegerField("Número de Registros", default=0)
    val_porcentaje = models.DecimalField("Procentaje", max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return str(self.val_valor)

    def get_absolute_url(self):
        return reverse('validacion:validacion_index')

    class Meta:
        ordering = ('val_id', 'est_id', 'var_id',)
