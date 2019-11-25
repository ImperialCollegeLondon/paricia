from django.db import models
from estacion.models import Estacion
from medicion.models import DigVar

# Create your models here.
class Precipitacion(models.Model):
    # estacion = models.ForeignKey( Estacion, on_delete=models.CASCADE)
    estacion_id = models.PositiveIntegerField("estacion_id", db_index=True)
    fecha = models.DateField("Fecha", db_index=True)
    valor = models.DecimalField("Valor", max_digits=(DigVar.v1.max_dig+2), decimal_places=DigVar.v1.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo Umbral %", max_digits=4, decimal_places=1)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['fecha', 'estacion_id']),
        ]

class TemperaturaAire(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id", db_index=True)
    fecha = models.DateField("Fecha", db_index=True)
    valor = models.DecimalField("Valor", max_digits=DigVar.v2.max_dig + 1, decimal_places=DigVar.v2.dec_pla + 1, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla + 1, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla + 1, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo Umbral %", max_digits=4, decimal_places=1)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class HumedadAire(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id", db_index=True)
    fecha = models.DateField("Fecha", db_index=True)
    valor = models.DecimalField("Valor", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo Umbral %", max_digits=4, decimal_places=1)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class VelocidadViento(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id", db_index=True)
    fecha = models.DateField("Fecha", db_index=True)
    valor = models.DecimalField("Valor", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo Umbral %", max_digits=4, decimal_places=1)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class DireccionViento(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id", db_index=True)
    fecha = models.DateField("Fecha", db_index=True)
    valor = models.DecimalField("Valor", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo Umbral %", max_digits=4, decimal_places=1)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class HumedadSuelo(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id", db_index=True)
    fecha = models.DateField("Fecha", db_index=True)
    valor = models.DecimalField("Valor", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo Umbral %", max_digits=4, decimal_places=1)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class RadiacionSolar(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id", db_index=True)
    fecha = models.DateField("Fecha", db_index=True)
    valor = models.DecimalField("Valor", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo Umbral %", max_digits=4, decimal_places=1)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class PresionAtmosferica(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id", db_index=True)
    fecha = models.DateField("Fecha", db_index=True)
    valor = models.DecimalField("Valor", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo Umbral %", max_digits=4, decimal_places=1)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class TemperaturaAgua(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id", db_index=True)
    fecha = models.DateField("Fecha", db_index=True)
    valor = models.DecimalField("Valor", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo Umbral %", max_digits=4, decimal_places=1)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Caudal(models.Model):
    estacion_id = models.PositiveIntegerField("estacion_id", db_index=True)
    fecha = models.DateField("Fecha", db_index=True)
    valor = models.DecimalField("Valor", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    max_abs = models.DecimalField("Máximo", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    min_abs = models.DecimalField("Mínimo", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    max_del_prom = models.DecimalField("Máximo del promedio", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    min_del_prom = models.DecimalField("Mínimo del promedio", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    completo_mediciones = models.DecimalField("Completo mediciones %", max_digits=4, decimal_places=1)
    completo_umbral = models.DecimalField("Completo Umbral %", max_digits=4, decimal_places=1)

    class Meta:
        unique_together = ('estacion_id', 'fecha')
        indexes = [
            models.Index(fields=['fecha', 'estacion_id']),
        ]

