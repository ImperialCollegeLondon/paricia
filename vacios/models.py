# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from estacion.models import Estacion
from variable.models import Variable


# Create your models here.

class Vacios(models.Model):
    vac_id = models.AutoField("Id", primary_key=True)
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
    vac_fecha_ini = models.DateField("Fecha inicio")
    vac_hora_ini = models.TimeField("Hora inicio")
    vac_fecha_fin = models.DateField("Fecha fin")
    vac_hora_fin = models.TimeField("Hora fin")
    vac_observacion = models.TextField("Observación", null=True)

    def get_absolute_url(self):
        return reverse('vacios:vacios_detail', kwargs={'pk': self.pk})
