from django.db import models
from estacion.models import Estacion
from medicion.models import DigVar

class Precipitacion(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField("Valor", max_digits=(DigVar.v1.max_dig+1), decimal_places=DigVar.v1.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo umbral %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['usado_para_mensual', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]

class TemperaturaAire(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v2.max_dig + 1, decimal_places=DigVar.v2.dec_pla + 1, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla + 1, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla + 1, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo umbral %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['usado_para_mensual', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class HumedadAire(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo umbral %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['usado_para_mensual', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class VelocidadViento(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo umbral %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['usado_para_mensual', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class DireccionViento(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo umbral %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['usado_para_mensual', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class HumedadSuelo(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo umbral %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['usado_para_mensual', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class RadiacionSolar(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo umbral %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['usado_para_mensual', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class PresionAtmosferica(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo umbral %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['usado_para_mensual', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class TemperaturaAgua(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo umbral %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['usado_para_mensual', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Caudal(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo umbral %", max_digits=4, decimal_places=1)
    usado_para_mensual = models.BooleanField("Usado para mes", default=False)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['usado_para_mensual', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]

