# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from estacion.models import Estacion
from variable.models import Variable
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
# frecuencia de registro de la estación. 
class Frecuencia(models.Model):
    fre_id = models.AutoField("Id", primary_key=True)
    est_id = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación")
    var_id = models.ForeignKey(
        Variable,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Variable")
    fre_valor = models.IntegerField("Frecuencia (min)", null=True,
                                    validators=[MaxValueValidator(1500), MinValueValidator(0)])
    fre_fecha_ini = models.DateField("Fecha inicio")
    fre_fecha_fin = models.DateField("Fecha fin", blank=True, null=True)

    def get_absolute_url(self):
        return reverse('frecuencia:frecuencia_detail', kwargs={'pk': self.pk})
