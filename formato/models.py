# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from datalogger.models import Datalogger
from variable.models import Variable
from estacion.models import Estacion
from marca.models import Marca


# Create your models here.
class Extension(models.Model):
    ext_id = models.AutoField("Id", primary_key=True)
    ext_valor = models.CharField("Valor", max_length=5)

    def __str__(self):
        return str(self.ext_valor)

    def get_absolute_url(self):
        return reverse('formato:extension_detail', kwargs={'pk': self.pk})


class Delimitador(models.Model):
    del_id = models.AutoField("Id", primary_key=True)
    del_nombre = models.CharField("Nombre", max_length=100)
    del_caracter = models.CharField("Caracter", max_length=5)

    def __str__(self):
        return str(self.del_nombre)

    def get_absolute_url(self):
        return reverse('formato:delimitador_detail', kwargs={'pk': self.pk})


class Fecha(models.Model):
    fec_id = models.AutoField("Id", primary_key=True)
    fec_formato = models.CharField("Formato", max_length=20)
    fec_codigo = models.CharField("Código", max_length=20)

    def __str__(self):
        return str(self.fec_formato)

    class Meta:
        ordering = ('fec_id',)


class Hora(models.Model):
    hor_id = models.AutoField("Id", primary_key=True)
    hor_formato = models.CharField("Formato", max_length=20)
    hor_codigo = models.CharField("Código", max_length=20)

    def __str__(self):
        return str(self.hor_formato)

    class Meta:
        ordering = ('hor_id',)


class Formato(models.Model):
    TIPO_FORMATO = (
        ('automatico', 'automático'),
        ('convencional', 'convencional'),
    )
    for_id = models.AutoField(primary_key=True)
    ext_id = models.ForeignKey(
        Extension,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Extensión del Archivo")
    del_id = models.ForeignKey(
        Delimitador,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Delimitador")
    mar_id = models.ForeignKey(
        Marca,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Marca Datalogger")
    for_nombre = models.CharField("Nombre del Formato", max_length=50)
    for_descripcion = models.TextField("Descripción", null=True)
    for_ubicacion = models.CharField("Ubicación", max_length=300)
    for_archivo = models.CharField("Archivo", max_length=100, blank=True, null=True,
                                   help_text="Solo aplica para transmisión automática")
    for_fil_ini = models.IntegerField("Fila de inicio")
    fec_id = models.ForeignKey(
        Fecha,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Formato de Fecha")
    for_col_fecha = models.IntegerField("Columna fecha")
    hor_id = models.ForeignKey(
        Hora,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Formato de Hora"
    )

    for_col_hora = models.IntegerField("Columna de hora")
    for_tipo = models.CharField("Tipo de Formato", max_length=50, choices=TIPO_FORMATO)
    for_estado = models.BooleanField("Estado", default=True)

    def __str__(self):
        return str(self.for_descripcion)

    def get_absolute_url(self):
        return reverse('formato:formato_clasificacion', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('for_id',)


class Clasificacion(models.Model):
    cla_id = models.AutoField("Id", primary_key=True)
    for_id = models.ForeignKey(
        Formato,
        on_delete=models.CASCADE,
        verbose_name="Formato")
    var_id = models.ForeignKey(
        Variable,
        on_delete=models.CASCADE,
        verbose_name="Variable")
    cla_valor = models.IntegerField("Columna valor")
    cla_maximo = models.IntegerField("Columna valor máximo", blank=True, null=True)
    cla_minimo = models.IntegerField("Columna valor mínimo", blank=True, null=True)

    def __str__(self):
        return str(self.cla_id)

    def get_absolute_url(self):
        return reverse('formato:clasificacion_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('var_id',)


class Asociacion(models.Model):
    aso_id = models.AutoField("Id", primary_key=True)
    for_id = models.ForeignKey(
        Formato,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Formato")
    est_id = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )

    def get_absolute_url(self):
        return reverse('formato:asociacion_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('aso_id',)
