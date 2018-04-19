# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from marca.models import Marca


# Create your models here.
class Sensor(models.Model):
    # TIPO_NOMBRE = (
    #     ('Termómetro', 'Termómetro'),
    #     ('Higrómetro', 'Higrómetro'),
    #     ('Pluviógrafo', 'Pluviógrafo'),
    #     ('Veleta', 'Veleta'),
    #     ('Anemómetro', 'Anemómetro'),
    #     ('Barómetro', 'Barómetro'),
    #     ('TDR', 'TDR'),
    #     ('Piranómetro', 'Piranómetro'),
    #     ('Termómetro de agua', 'Termómetro de agua'),
    #     ('Sensor de nivel', 'Sensor de nivel'),
    # )

    TIPO_NOMBRE = (
        ('Dirección del viento', 'Dirección del viento'),
        ('Humedad y Temperatura', 'Humedad y Temperatura'),
        ('Pluviómetro', 'Pluviómetro'),
        ('Presión Barométrica', 'Presión Barométrica'),
        ('Radiación Solar', 'Radiación Solar'),
        ('Sensor de viento', 'Sensor de viento'),
        ('Sonda Piezométrico', 'Sonda Piezométrico'),
        ('Sonda Ultrasónico', 'Sonda Ultrasónico'),
        ('Velocidad del viento', 'Velocidad del viento'),
     )

    sen_id = models.AutoField("Id", primary_key=True)
    sen_codigo = models.CharField("Codigo", max_length=20, null=True, unique=True)
    sen_nombre = models.CharField("Nombre", max_length=40, choices=TIPO_NOMBRE)
    mar_id = models.ForeignKey(
        Marca,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Marca"
    )
    sen_modelo = models.CharField("Modelo", max_length=20, null=True)
    sen_serial = models.CharField("Serial", max_length=20, null=True)
    sen_estado = models.BooleanField("Estado", default=True)

    def __str__(self):
        return (self.sen_codigo + " " + self.sen_nombre + " " + self.sen_modelo + " " + self.sen_serial).encode('utf-8')

    def get_absolute_url(self):
        return reverse('sensor:sensor_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('sen_codigo', 'sen_nombre', 'sen_modelo', 'sen_serial',)
