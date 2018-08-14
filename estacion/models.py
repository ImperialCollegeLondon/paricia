# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Provincia(models.Model):
    pro_nombre = models.CharField(max_length=40)

    def __str__(self):
        return str(self.pro_nombre)


class Tipo(models.Model):
    tip_nombre = models.CharField(max_length=40)

    def __str__(self):
        return str(self.tip_nombre)


class Estacion(models.Model):
    TIPO_ESTACION = (
        ('M', 'Meteorológica'),
        ('P', 'Pluviométrica'),
        ('H', 'Hidrológica'),
    )
    est_id = models.AutoField("Id", primary_key=True)
    est_codigo = models.CharField("Código", max_length=10)
    est_nombre = models.CharField("Nombre", max_length=100)
    est_tipo = models.CharField("Tipo", max_length=25, choices=TIPO_ESTACION)
    est_estado = models.BooleanField("Activo", default=True)
    est_provincia = models.CharField("Provincia", max_length=50, null=True)
    est_latitud = models.DecimalField("Y UTM", max_digits=10, decimal_places=2, null=True)
    est_longitud = models.DecimalField("X UTM", max_digits=10, decimal_places=2, null=True)
    est_altura = models.IntegerField("Altura", null=True, validators=[MaxValueValidator(6000), MinValueValidator(0)])
    est_ficha = models.FileField("Fichas", upload_to='documents/')
    est_fecha_inicio = models.DateField("Fecha Inicio Operaciones", null=True)
    provincia = models.ForeignKey(Provincia,  on_delete=models.CASCADE, verbose_name="Provincia", null=True, blank=True)
    tipo = models.ForeignKey(Tipo,  on_delete=models.CASCADE, verbose_name="Tipo", null=True, blank=True)

    def __str__(self):
        return str(self.est_codigo)

    def get_absolute_url(self):
        return reverse('estacion:estacion_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('est_id',)
