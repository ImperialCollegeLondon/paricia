# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from variable.models import Variable
from estacion.models import Estacion
from django.urls import reverse
from medicion.models import DigVar
from datetime import datetime
from django.utils import timezone


class Validacion(models.Model):
    val_id = models.AutoField("Id", primary_key=True)
    var_id = models.ForeignKey(Variable, models.SET_NULL, blank=True, null=True, verbose_name="Variable")
    est_id = models.ForeignKey(Estacion, models.SET_NULL, blank=True, null=True, verbose_name="Estación")
    fecha_validacion = models.DateField("Fecha validación")
    fecha_inicio_datos = models.DateTimeField("Fecha inicio datos")
    fecha_fin_datos = models.DateTimeField("Fecha fin datos")
    comentario = models.CharField("Comentario", max_length=350)

    def __str__(self):
        return str(self.var_id) + ' -- ' + str(self.est_id) + ' -- ' + str(self.fecha_validacion)

    def get_absolute_url(self):
        return reverse('validacion:validacion_index')

    class Meta:
        ordering = ('val_id', 'est_id', 'var_id',)
        indexes = [
            models.Index(fields=['var_id', 'est_id']),
        ]


########################################################################################################################
class ComentarioValidacion(models.Model):
    variable_id = models.SmallIntegerField(db_index=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    validado_id = models.PositiveIntegerField("Validación")
    comentario = models.CharField("Comentario", max_length=350)

    class Meta:
        indexes = [
            models.Index(fields=['variable_id', 'estacion_id', 'validado_id']),
            models.Index(fields=['variable_id', 'validado_id', 'estacion_id']),
            models.Index(fields=['estacion_id', 'variable_id', 'validado_id']),
            models.Index(fields=['estacion_id', 'validado_id', 'variable_id']),
            models.Index(fields=['validado_id', 'estacion_id', 'variable_id']),
            models.Index(fields=['validado_id', 'variable_id', 'estacion_id']),
        ]


class Precipitacion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v1.max_dig, decimal_places=DigVar.v1.dec_pla, null=True)
    usado_para_horario = models.BooleanField("Usado en horario", default=False)
    validacion = models.PositiveSmallIntegerField("Validación")

    class Meta:
        unique_together = ('estacion_id', 'fecha', 'validacion')
        indexes = [
            # models.Index(fields=['estacion_id', 'fecha']),  #Al hacer unique together se crea un INDEX
            models.Index(fields=['fecha', 'estacion_id']),
            models.Index(fields=['usado_para_horario', 'id']),
        ]


class TemperaturaAire(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla, null=True)
    usado_para_horario = models.BooleanField("Usado en horario", default=False)
    validacion = models.PositiveSmallIntegerField("Validación")

    class Meta:
        unique_together = ('estacion_id', 'fecha', 'validacion')
        indexes = [
            # models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
            models.Index(fields=['usado_para_horario', 'id']),
        ]


class HumedadAire(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    usado_para_horario = models.BooleanField("Usado en horario", default=False)
    validacion = models.PositiveSmallIntegerField("Validación")

    class Meta:
        unique_together = ('estacion_id', 'fecha', 'validacion')
        indexes = [
            # models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
            models.Index(fields=['usado_para_horario', 'id']),
        ]


class VelocidadViento(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    usado_para_horario = models.BooleanField("Usado en horario", default=False)
    validacion = models.PositiveSmallIntegerField("Validación")

    class Meta:
        unique_together = ('estacion_id', 'fecha', 'validacion')
        indexes = [
            # models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
            models.Index(fields=['usado_para_horario', 'id']),
        ]


class DireccionViento(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    usado_para_horario = models.BooleanField("Usado en horario", default=False)
    validacion = models.PositiveSmallIntegerField("Validación")

    class Meta:
        unique_together = ('estacion_id', 'fecha', 'validacion')
        indexes = [
            # models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
            models.Index(fields=['usado_para_horario', 'id']),
        ]


class HumedadSuelo(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    usado_para_horario = models.BooleanField("Usado en horario", default=False)
    validacion = models.PositiveSmallIntegerField("Validación")

    class Meta:
        unique_together = ('estacion_id', 'fecha', 'validacion')
        indexes = [
            # models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
            models.Index(fields=['usado_para_horario', 'id']),
        ]


class RadiacionSolar(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    usado_para_horario = models.BooleanField("Usado en horario", default=False)
    validacion = models.PositiveSmallIntegerField("Validación")

    class Meta:
        unique_together = ('estacion_id', 'fecha', 'validacion')
        indexes = [
            # models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
            models.Index(fields=['usado_para_horario', 'id']),
        ]


class PresionAtmosferica(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    usado_para_horario = models.BooleanField("Usado en horario", default=False)
    validacion = models.PositiveSmallIntegerField("Validación")

    class Meta:
        unique_together = ('estacion_id', 'fecha', 'validacion')
        indexes = [
            # models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
            models.Index(fields=['usado_para_horario', 'id']),
        ]


class TemperaturaAgua(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    usado_para_horario = models.BooleanField("Usado en horario", default=False)
    validacion = models.PositiveSmallIntegerField("Validación")

    class Meta:
        unique_together = ('estacion_id', 'fecha', 'validacion')
        indexes = [
            # models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
            models.Index(fields=['usado_para_horario', 'id']),
        ]


class Caudal(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    usado_para_horario = models.BooleanField("Usado en horario", default=False)
    validacion = models.PositiveSmallIntegerField("Validación")

    class Meta:
        unique_together = ('estacion_id', 'fecha', 'validacion')
        indexes = [
            # models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
            models.Index(fields=['usado_para_horario', 'id']),
        ]


class NivelAgua(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v11.max_dig, decimal_places=DigVar.v11.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v11.max_dig, decimal_places=DigVar.v11.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v11.max_dig, decimal_places=DigVar.v11.dec_pla, null=True)
    usado_para_horario = models.BooleanField("Usado en horario", default=False)
    validacion = models.PositiveSmallIntegerField("Validación")

    class Meta:
        unique_together = ('estacion_id', 'fecha', 'validacion')
        indexes = [
            # models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
            models.Index(fields=['usado_para_horario', 'id']),
        ]
