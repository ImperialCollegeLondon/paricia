from django.db import models
from medicion.models import DigVar

"""
1   Precipitacion
2   TemperaturaAire
3   HumedadAire
4   VelocidadViento
5   DireccionViento
6   HumedadSuelo
7   RadiacionSolar
8   PresionAtmosferica
9   TemperaturaAgua
10  Caudal
11 Nivel agua
"""

###############################
class Precipitacion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id" )
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v1.max_dig, decimal_places=DigVar.v1.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    usado_para_diario = models.BooleanField("Usado para diario", default=False)

    class Meta:
        indexes = [
            #models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['usado_para_diario', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]
        unique_together = ('estacion_id', 'fecha')


class TemperaturaAire(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v2.max_dig + 1, decimal_places=DigVar.v2.dec_pla + 1, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    usado_para_diario = models.BooleanField("Usado para diario", default=False)

    class Meta:
        indexes = [
            #models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['usado_para_diario', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]
        unique_together = ('estacion_id', 'fecha')


class HumedadAire(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    usado_para_diario = models.BooleanField("Usado para diario", default=False)

    class Meta:
        indexes = [
            #models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['usado_para_diario', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]
        unique_together = ('estacion_id', 'fecha')


class DireccionViento(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    usado_para_diario = models.BooleanField("Usado para diario", default=False)

    class Meta:
        indexes = [
            #models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['usado_para_diario', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]
        unique_together = ('estacion_id', 'fecha')

class VelocidadViento(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    usado_para_diario = models.BooleanField("Usado para diario", default=False)

    class Meta:
        indexes = [
            #models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['usado_para_diario', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]
        unique_together = ('estacion_id', 'fecha')


class HumedadSuelo(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    usado_para_diario = models.BooleanField("Usado para diario", default=False)

    class Meta:
        indexes = [
            #models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['usado_para_diario', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]
        unique_together = ('estacion_id', 'fecha')


class RadiacionSolar(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    usado_para_diario = models.BooleanField("Usado para diario", default=False)

    class Meta:
        indexes = [
            #models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['usado_para_diario', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]
        unique_together = ('estacion_id', 'fecha')


class PresionAtmosferica(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    usado_para_diario = models.BooleanField("Usado para diario", default=False)

    class Meta:
        indexes = [
            #models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['usado_para_diario', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]
        unique_together = ('estacion_id', 'fecha')


class TemperaturaAgua(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    usado_para_diario = models.BooleanField("Usado para diario", default=False)

    class Meta:
        indexes = [
            #models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['usado_para_diario', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]
        unique_together = ('estacion_id', 'fecha')


class Caudal(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    usado_para_diario = models.BooleanField("Usado para diario", default=False)

    class Meta:
        indexes = [
            #models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['usado_para_diario', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]
        unique_together = ('estacion_id', 'fecha')

class NivelAgua(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    usado_para_diario = models.BooleanField("Usado para diario", default=False)

    class Meta:
        indexes = [
            #models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['usado_para_diario', 'id']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]
        unique_together = ('estacion_id', 'fecha')
