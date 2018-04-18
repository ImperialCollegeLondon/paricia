# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datalogger.models import Datalogger
from estacion.models import Estacion
from django.urls import reverse


# Create your models here.
class Instalacion(models.Model):
    ins_id = models.AutoField("Id", primary_key=True)
    est_id = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación")
    dat_id = models.ForeignKey(
        Datalogger,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Datalogger")
    ins_fecha_ini = models.DateField("Fecha de inicio")
    ins_fecha_fin = models.DateField("fecha de fin", blank=True, null=True)
    ins_en_uso = models.BooleanField("En uso", default=True)
    ins_observacion = models.CharField("Observacion", max_length=500, blank=True)

    def __str__(self):
        return str(self.ins_id)

    def get_absolute_url(self):
        return reverse('instalacion:instalacion_index')

    class Meta:
        ordering = ('ins_id', 'est_id', 'dat_id',)
