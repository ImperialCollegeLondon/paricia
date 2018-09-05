# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from marca.models import Marca


# Create your models here.
class Tipo(models.Model):
    tip_nombre = models.CharField("Tipo", max_length=25)

    def __str__(self):
        return str(self.tip_nombre)


class Sensor(models.Model):
    sen_id = models.AutoField("Id", primary_key=True)
    sen_codigo = models.CharField("Codigo", max_length=20, null=True)
    mar_id = models.ForeignKey(
        Marca,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Marca"
    )
    tipo = models.ForeignKey(
        Tipo,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Tipo"
    )
    sen_modelo = models.CharField("Modelo", max_length=150, null=True)
    sen_serial = models.CharField("Serial", max_length=20, null=True)
    sen_estado = models.BooleanField("Estado", default=True)

    def __str__(self):
        return str(self.sen_serial)

    def get_absolute_url(self):
        return reverse('sensor:sensor_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('sen_codigo', 'tipo', 'sen_modelo', 'sen_serial',)
