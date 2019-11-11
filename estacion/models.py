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


class Sistema(models.Model):
    id = models.AutoField("Id", primary_key=True)
    nombre = models.CharField(max_length=40)
    imagen = models.FileField("Imagen", upload_to='estacion/sistema_imagen/', null=True)

    def __str__(self):
        return str(self.nombre)

    def get_absolute_url(self):
        return reverse('estacion:sistema_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('id',)


class Cuenca(models.Model):
    id = models.AutoField("Id", primary_key=True)
    nombre = models.CharField(max_length=40)
    imagen = models.FileField("Imagen", upload_to='estacion/cuenca_imagen/', null=True)

    def __str__(self):
        return str(self.nombre)

    def get_absolute_url(self):
        return reverse('estacion:cuenca_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('id',)


class SistemaCuenca(models.Model):
    id = models.AutoField("Id", primary_key=True)
    sistema = models.ForeignKey(Sistema, on_delete=models.SET_NULL, null=True, verbose_name="Sistema")
    cuenca = models.ForeignKey(Cuenca, on_delete=models.SET_NULL, null=True, verbose_name="Cuenca")
    imagen = models.FileField("Imagen", upload_to='estacion/sistemacuenca_imagen/', null=True)

    def __str__(self):
        return str(self.sistema) + ' - ' + str(self.cuenca)

    def get_absolute_url(self):
        return reverse('estacion:sistemacuenca_detail', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ("sistema", "cuenca")
        ordering = ('id',)




class Estacion(models.Model):
    TIPO_ESTACION = (
        ('M', 'Meteorológica'),
        ('P', 'Pluviométrica'),
        ('H', 'Hidrológica'),
    )
    est_id = models.AutoField("Id", primary_key=True)
    est_codigo = models.CharField("Código", max_length=10)
    est_nombre = models.CharField("Nombre", max_length=100)
    est_estado = models.BooleanField("Activo", default=True)
    est_latitud = models.DecimalField("Latitud", max_digits=12, decimal_places=8, null=True)
    est_longitud = models.DecimalField("Longitud", max_digits=12, decimal_places=8, null=True)
    est_utmy = models.DecimalField("Y UTM", max_digits=10, decimal_places=2, null=True)
    est_utmx = models.DecimalField("X UTM", max_digits=10, decimal_places=2, null=True)
    est_altura = models.IntegerField("Altura", null=True, validators=[MaxValueValidator(6000), MinValueValidator(0)])
    est_ficha = models.FileField("Fichas", upload_to='documents/')
    est_fecha_inicio = models.DateField("Fecha Inicio Operaciones", null=True)
    provincia = models.ForeignKey(Provincia,  on_delete=models.CASCADE, verbose_name="Provincia", null=True, blank=True)
    tipo = models.ForeignKey(Tipo,  on_delete=models.CASCADE, verbose_name="Tipo", null=True, blank=True)
    transmision = models.BooleanField("Trasmision",default=False, null=True, blank=True)
    sistemacuenca = models.ForeignKey(SistemaCuenca, on_delete=models.SET_NULL, null=True, verbose_name="SistemaCuenca")
    est_externa = models.BooleanField("Externa",default=True);

    def __str__(self):
        return str(self.est_codigo)

    def get_absolute_url(self):
        return reverse('estacion:estacion_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('est_id',)


# modelo para almacenar las estaciones del INAMHI
class Inamhi(models.Model):
    identificador = models.IntegerField("Id")
    codigo = models.CharField("Código", max_length=10)
    nombre = models.CharField("Nombre", max_length=100)
    transmision = models.CharField("Transmision", max_length=100)
    latitud = models.DecimalField("Latitud", max_digits=12, decimal_places=8, null=True)
    longitud = models.DecimalField("Longitud", max_digits=12, decimal_places=8, null=True)
    provincia = models.CharField("Nombre", max_length=50)
    canton = models.CharField("Cantón", max_length=50)
    parroquia = models.CharField("Parroquia", max_length=50)
    categoria = models.CharField("Categoria", max_length=20)

    def __str__(self):
        return str(self.codigo) + ' ' + str(self.nombre)




