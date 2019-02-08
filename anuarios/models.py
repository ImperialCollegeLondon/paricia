# -*- coding: utf-8 -*-
# Create your models here.
from __future__ import unicode_literals

from django.db import models
from estacion.models import Estacion

# constante para los label de la velocidad promedio por dirección
LBL_VEL = "Promedio de Velocidad(m/s) al "
# constante para los label del porcentaje de velocidad promedio por dirección
LBL_POR = "Porcentaje de velocidad(m/s) al "


class Precipitacion(models.Model):
    pre_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    pre_periodo = models.IntegerField("Año")
    pre_mes = models.IntegerField("Mes")
    pre_suma = models.DecimalField("Precipitación", max_digits=7, decimal_places=2)
    pre_maximo = models.DecimalField("Máximo en 24H", max_digits=7, decimal_places=2)
    pre_maximo_dia = models.IntegerField("Día")
    pre_dias = models.IntegerField("Total de días con precipitacion")

    class Meta:
        ordering = ('pre_mes',)
        indexes = [
            models.Index(fields=['est_id', 'pre_periodo']),
        ]


class TemperaturaAire(models.Model):
    tai_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    tai_periodo = models.IntegerField("Año", default=2000)
    tai_mes = models.IntegerField("Mes")
    tai_maximo_abs = models.DecimalField("Máximo Absoluto", max_digits=7, decimal_places=2)
    tai_maximo_dia = models.IntegerField("Día")
    tai_minimo_abs = models.DecimalField("Mínimo Absoluto", max_digits=7, decimal_places=2)
    tai_minimo_dia = models.IntegerField("Día")
    tai_maximo = models.DecimalField("Máximo", max_digits=7, decimal_places=2)
    tai_minimo = models.DecimalField("Mínimo", max_digits=7, decimal_places=2)
    tai_promedio = models.DecimalField("Promedio", max_digits=7, decimal_places=2)

    class Meta:
        ordering = ('tai_mes',)
        indexes = [
            models.Index(fields=['est_id', 'tai_periodo']),
        ]


class HumedadAire(models.Model):
    hai_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    hai_periodo = models.IntegerField("Año", default=2000)
    hai_mes = models.IntegerField("Mes")
    hai_maximo = models.DecimalField("Máximo Absoluto", max_digits=7, decimal_places=2)
    hai_maximo_dia = models.IntegerField("Día")
    hai_minimo = models.DecimalField("Máximo Absoluto", max_digits=7, decimal_places=2)
    hai_minimo_dia = models.IntegerField("Día")
    hai_promedio = models.DecimalField("Máximo Absoluto", max_digits=7, decimal_places=2)

    class Meta:
        ordering = ('hai_mes',)
        indexes = [
            models.Index(fields=['est_id', 'hai_periodo']),
        ]


class Viento(models.Model):
    vie_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    vie_periodo = models.IntegerField("Año", default=2000)
    vie_mes = models.IntegerField("Mes")
    vie_vel_N = models.DecimalField(LBL_VEL + "Norte", max_digits=7, decimal_places=2)
    vie_por_N = models.DecimalField(LBL_POR + "Norte", max_digits=7, decimal_places=2)
    vie_vel_NE = models.DecimalField(LBL_VEL + "Noreste", max_digits=7, decimal_places=2)
    vie_por_NE = models.DecimalField(LBL_POR + "Noreste", max_digits=7, decimal_places=2)
    vie_vel_E = models.DecimalField(LBL_VEL + "Este", max_digits=7, decimal_places=2)
    vie_por_E = models.DecimalField(LBL_POR + "Este", max_digits=7, decimal_places=2)
    vie_vel_SE = models.DecimalField(LBL_VEL + "Sureste", max_digits=7, decimal_places=2)
    vie_por_SE = models.DecimalField(LBL_POR + "Sureste", max_digits=7, decimal_places=2)
    vie_vel_S = models.DecimalField(LBL_VEL + "Sur", max_digits=7, decimal_places=2)
    vie_por_S = models.DecimalField(LBL_POR + "Sur", max_digits=7, decimal_places=2)
    vie_vel_SO = models.DecimalField(LBL_VEL + "Suroeste", max_digits=7, decimal_places=2)
    vie_por_SO = models.DecimalField(LBL_POR + "Suroeste", max_digits=7, decimal_places=2)
    vie_vel_O = models.DecimalField(LBL_VEL + "Oeste", max_digits=7, decimal_places=2)
    vie_por_O = models.DecimalField(LBL_POR + "Oeste", max_digits=7, decimal_places=2)
    vie_vel_NO = models.DecimalField(LBL_VEL + "Noroeste", max_digits=7, decimal_places=2)
    vie_por_NO = models.DecimalField("Noroeste", max_digits=7, decimal_places=2)
    vie_calma = models.DecimalField("Calma", max_digits=7, decimal_places=2)
    vie_obs = models.IntegerField("Numero de Observaciones", default=2000)
    vie_vel_max = models.DecimalField("Velocidad Mayor m/s", max_digits=7, decimal_places=2)
    vie_vel_dir = models.CharField("Dirección Velocidad Mayor", max_length=2)
    vie_vel_med = models.DecimalField("Velocidad Media Km/h", max_digits=7, decimal_places=2)

    class Meta:
        ordering = ('vie_mes',)
        indexes = [
            models.Index(fields=['est_id', 'vie_periodo']),
        ]


class HumedadSuelo(models.Model):
    hsu_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    hsu_periodo = models.IntegerField("Año", default=2000)
    hsu_mes = models.IntegerField("Mes")
    hsu_maximo = models.DecimalField("Máximo", max_digits=7, decimal_places=2)
    hsu_minimo = models.DecimalField("Mínimo", max_digits=7, decimal_places=2)
    hsu_promedio = models.DecimalField("Promedio", max_digits=7, decimal_places=2)

    class Meta:
        ordering = ('hsu_mes',)
        indexes = [
            models.Index(fields=['est_id', 'hsu_periodo']),
        ]


class RadiacionSolar(models.Model):
    rad_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    rad_periodo = models.IntegerField("Año", default=2000)
    rad_mes = models.IntegerField("Mes")
    rad_hora = models.IntegerField("Hora")
    rad_maximo = models.DecimalField("Máximo", max_digits=7, decimal_places=2)
    rad_minimo = models.DecimalField("Mínimo", max_digits=7, decimal_places=2)


class RadiacionMaxima(models.Model):
    rad_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    rad_periodo = models.IntegerField("Año", default=2000)
    rad_mes = models.IntegerField("Mes")
    rad_5 = models.DecimalField("5", max_digits=7, decimal_places=2)
    rad_6 = models.DecimalField("6", max_digits=7, decimal_places=2)
    rad_7 = models.DecimalField("7", max_digits=7, decimal_places=2)
    rad_8 = models.DecimalField("8", max_digits=7, decimal_places=2)
    rad_9 = models.DecimalField("9", max_digits=7, decimal_places=2)
    rad_10 = models.DecimalField("10", max_digits=7, decimal_places=2)
    rad_11 = models.DecimalField("11", max_digits=7, decimal_places=2)
    rad_12 = models.DecimalField("12", max_digits=7, decimal_places=2)
    rad_13 = models.DecimalField("13", max_digits=7, decimal_places=2)
    rad_14 = models.DecimalField("14", max_digits=7, decimal_places=2)
    rad_15 = models.DecimalField("15", max_digits=7, decimal_places=2)
    rad_16 = models.DecimalField("16", max_digits=7, decimal_places=2)
    rad_17 = models.DecimalField("17", max_digits=7, decimal_places=2)
    rad_18 = models.DecimalField("18", max_digits=7, decimal_places=2)
    rad_max = models.DecimalField("Máximo", max_digits=7, decimal_places=2)
    rad_hora = models.DecimalField("Hora", max_digits=7, decimal_places=2)

    class Meta:
        ordering = ('rad_mes',)
        indexes = [
            models.Index(fields=['est_id', 'rad_periodo']),
        ]


class RadiacionMinima(models.Model):
    rad_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    rad_periodo = models.IntegerField("Año", default=2000)
    rad_mes = models.IntegerField("Mes")
    rad_5 = models.DecimalField("5", max_digits=7, decimal_places=2)
    rad_6 = models.DecimalField("6", max_digits=7, decimal_places=2)
    rad_7 = models.DecimalField("7", max_digits=7, decimal_places=2)
    rad_8 = models.DecimalField("8", max_digits=7, decimal_places=2)
    rad_9 = models.DecimalField("9", max_digits=7, decimal_places=2)
    rad_10 = models.DecimalField("10", max_digits=7, decimal_places=2)
    rad_11 = models.DecimalField("11", max_digits=7, decimal_places=2)
    rad_12 = models.DecimalField("12", max_digits=7, decimal_places=2)
    rad_13 = models.DecimalField("13", max_digits=7, decimal_places=2)
    rad_14 = models.DecimalField("14", max_digits=7, decimal_places=2)
    rad_15 = models.DecimalField("15", max_digits=7, decimal_places=2)
    rad_16 = models.DecimalField("16", max_digits=7, decimal_places=2)
    rad_17 = models.DecimalField("17", max_digits=7, decimal_places=2)
    rad_18 = models.DecimalField("18", max_digits=7, decimal_places=2)
    rad_max = models.DecimalField("Mínima", max_digits=7, decimal_places=2)
    rad_hora = models.DecimalField("Hora", max_digits=7, decimal_places=2)
    class Meta:
        ordering = ('rad_mes',)
        indexes = [
            models.Index(fields=['est_id', 'rad_periodo']),
        ]


class PresionAtmosferica(models.Model):
    pat_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    pat_periodo = models.IntegerField("Año", default=2000)
    pat_mes = models.IntegerField("Mes")
    pat_maximo = models.DecimalField("Máximo", max_digits=7, decimal_places=2)
    pat_minimo = models.DecimalField("Mínimo", max_digits=7, decimal_places=2)
    pat_promedio = models.DecimalField("Promedio", max_digits=7, decimal_places=2)

    class Meta:
        ordering = ('pat_mes',)
        indexes = [
            models.Index(fields=['est_id', 'pat_periodo']),
        ]


class TemperaturaAgua(models.Model):
    tag_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    tag_periodo = models.IntegerField("Año", default=2000)
    tag_mes = models.IntegerField("Mes")
    tag_maximo = models.DecimalField("Máximo", max_digits=7, decimal_places=2)
    tag_minimo = models.DecimalField("Mínimo", max_digits=7, decimal_places=2)
    tag_promedio = models.DecimalField("Promedio", max_digits=7, decimal_places=2)

    class Meta:
        ordering = ('tag_mes',)
        indexes = [
            models.Index(fields=['est_id', 'tag_periodo']),
        ]


class Caudal(models.Model):
    cau_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    cau_periodo = models.IntegerField("Año", default=2000)
    cau_mes = models.IntegerField("Mes")
    cau_maximo = models.DecimalField("Máximo", max_digits=7, decimal_places=2)
    cau_minimo = models.DecimalField("Mínimo", max_digits=7, decimal_places=2)
    cau_promedio = models.DecimalField("Promedio", max_digits=7, decimal_places=2)

    class Meta:
        ordering = ('cau_mes',)
        indexes = [
            models.Index(fields=['est_id', 'cau_periodo']),
        ]


class NivelAgua(models.Model):
    nag_id = models.AutoField(primary_key=True)
    est_id = models.ForeignKey(
        Estacion,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Estación"
    )
    nag_periodo = models.IntegerField("Año", default=2000)
    nag_mes = models.IntegerField("Mes")
    nag_maximo = models.DecimalField("Máximo", max_digits=7, decimal_places=2)
    nag_minimo = models.DecimalField("Mínimo", max_digits=7, decimal_places=2)
    nag_promedio = models.DecimalField("Promedio", max_digits=7, decimal_places=2)

    class Meta:
        ordering = ('nag_mes',)
        indexes = [
            models.Index(fields=['est_id', 'nag_periodo']),
        ]
