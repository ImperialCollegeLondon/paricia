from __future__ import unicode_literals

from django.db import models
from variable.models import Variable
from estacion.models import Estacion
from django.urls import reverse


# Create your models here.
class Bitacora(models.Model):
    bit_id = models.AutoField("Id", primary_key=True)
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
        verbose_name="Estacion")
    bit_fecha_ini = models.DateField("Fecha de inicio")
    bit_fecha_fin = models.DateField("fecha de fin", blank=True, null=True)
    bit_observacion = models.CharField("Observacion", max_length=500, blank=True)

    def __str__(self):
        return str(self.bit_id)

    def get_absolute_url(self):
        return reverse('bitacora:bitacora_index')

    class Meta:
        ordering = ('bit_id', 'est_id', 'var_id',)
