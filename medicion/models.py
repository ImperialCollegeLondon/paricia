# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from variable.models import Variable
from estacion.models import Estacion
from marca.models import Marca
from django.urls import reverse


class CurvaDescarga(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion = models.ForeignKey(Estacion, on_delete=models.SET_NULL, null=True, verbose_name="Estación")
    fecha = models.DateTimeField("Fecha")
    funcion = models.CharField("Funcion", max_length=80)

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse('medicion:curvadescarga_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('id',)
        unique_together = ('estacion', 'fecha')


class ValorDecimal:
    max_dig = 6
    dec_pla = 2

    def __init__(self, max_dig, dec_pla):
        self.max_dig = max_dig
        self.dec_pla = dec_pla


class DigVar:
    v1 = ValorDecimal(max_dig=6, dec_pla=2)
    v2 = ValorDecimal(max_dig=14, dec_pla=6)
    v3 = ValorDecimal(max_dig=14, dec_pla=6)
    v4 = ValorDecimal(max_dig=14, dec_pla=6)
    v5 = ValorDecimal(max_dig=14, dec_pla=6)
    v6 = ValorDecimal(max_dig=14, dec_pla=6)
    v7 = ValorDecimal(max_dig=14, dec_pla=6)
    v8 = ValorDecimal(max_dig=14, dec_pla=6)
    v9 = ValorDecimal(max_dig=14, dec_pla=6)
    v10 = ValorDecimal(max_dig=14, dec_pla=6)
    v11 = ValorDecimal(max_dig=14, dec_pla=6)
    v12 = ValorDecimal(max_dig=14, dec_pla=6)

class Precipitacion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v1.max_dig, decimal_places=DigVar.v1.dec_pla, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['estacion', 'fecha']),
            models.Index(fields=['fecha', 'estacion']),
        ]


class TemperaturaAire(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion = models.PositiveIntegerField("Estacion")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['estacion', 'fecha']),
            models.Index(fields=['fecha', 'estacion']),
        ]


class HumedadAire(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion = models.PositiveIntegerField("Estacion")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['estacion', 'fecha']),
            models.Index(fields=['fecha', 'estacion']),
        ]
        
        
class Viento(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion = models.PositiveIntegerField("Estacion")
    fecha = models.DateTimeField("Fecha")
    vel_valor = models.DecimalField("Valor", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    vel_maximo = models.DecimalField("Máximo", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    vel_minimo = models.DecimalField("Mínimo", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    dir_valor = models.DecimalField("Valor", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    dir_maximo = models.DecimalField("Máximo", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla,
                                     null=True)
    dir_minimo = models.DecimalField("Mínimo", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla,
                                     null=True)

    class Meta:
        indexes = [
            models.Index(fields=['estacion', 'fecha']),
            models.Index(fields=['fecha', 'estacion']),
        ]
        

class VelocidadViento(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion = models.PositiveIntegerField("Estacion")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['estacion', 'fecha']),
            models.Index(fields=['fecha', 'estacion']),
        ]


class DireccionViento(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion = models.PositiveIntegerField("Estacion")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['estacion', 'fecha']),
            models.Index(fields=['fecha', 'estacion']),
        ]
        

class HumedadSuelo(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion = models.PositiveIntegerField("Estacion")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['estacion', 'fecha']),
            models.Index(fields=['fecha', 'estacion']),
        ]


class RadiacionSolar(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion = models.PositiveIntegerField("Estacion")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['estacion', 'fecha']),
            models.Index(fields=['fecha', 'estacion']),
        ]
        

class PresionAtmosferica(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion = models.PositiveIntegerField("Estacion")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['estacion', 'fecha']),
            models.Index(fields=['fecha', 'estacion']),
        ]


class TemperaturaAgua(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion = models.PositiveIntegerField("Estacion")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['estacion', 'fecha']),
            models.Index(fields=['fecha', 'estacion']),
        ]


class Caudal(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion = models.PositiveIntegerField("Estacion")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['estacion', 'fecha']),
            models.Index(fields=['fecha', 'estacion']),
        ]


class NivelAgua(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion = models.PositiveIntegerField("Estacion")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v11.max_dig, decimal_places=DigVar.v11.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v11.max_dig, decimal_places=DigVar.v11.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v11.max_dig, decimal_places=DigVar.v11.dec_pla, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['estacion', 'fecha']),
            models.Index(fields=['fecha', 'estacion']),
        ]

class VoltajeBateria(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion = models.PositiveIntegerField("Estacion")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v12.max_dig, decimal_places=DigVar.v12.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v12.max_dig, decimal_places=DigVar.v12.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v12.max_dig, decimal_places=DigVar.v12.dec_pla, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['estacion', 'fecha']),
            models.Index(fields=['fecha', 'estacion']),
        ]