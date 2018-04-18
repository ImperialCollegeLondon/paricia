# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from estacion.models import Estacion
from variable.models import Variable
from django.urls import reverse


# Create your models here.
class Cruce(models.Model):
    cru_id = models.AutoField("Id", primary_key=True)
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

    def __str__(self):
        return str(self.cru_id)

    def get_absolute_url(self):
        return reverse('cruce:cruce_index')

    class Meta:
        ordering = ('cru_id', 'est_id', 'var_id',)
