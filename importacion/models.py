# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.utils import timezone
from estacion.models import Estacion
from formato.models import Formato
from marca.models import Marca
from django.contrib.auth.models import User
from django.utils import timezone


class Importacion(models.Model):
    imp_id = models.AutoField("Id", primary_key=True)
    est_id = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación")
    for_id = models.ForeignKey(
        Formato,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Formato"
    )
    imp_fecha = models.DateTimeField("Fecha", auto_now_add=True)
    imp_fecha_ini = models.DateTimeField("Fecha Inicial", default=timezone.now)
    imp_fecha_fin = models.DateTimeField("Fecha Final", default=timezone.now)
    imp_archivo = models.FileField("Archivo", upload_to='archivos/')
    imp_observacion = models.TextField("Observaciones/Anotaciones", blank=True, null=True, default="Carga de Datos")
    imp_tipo = models.CharField("Tipo", max_length=1, default="c")
    usuario = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Usuario"
    )

    def get_absolute_url(self):
        return reverse('importacion:importacion_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('-imp_fecha',)
