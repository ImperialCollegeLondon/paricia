from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from estacion.models import Estacion
from variable.models import Variable


class PrecipitacionAcumulada(models.Model):
    fecha = models.DateField(primary_key=True)
    valor = models.DecimalField(max_digits=14, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False


class PrecipitacionEventos(models.Model):
    fecha = models.DateField(primary_key=True)
    valor = models.DecimalField(max_digits=14, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False


class PrecipitacionMultianual(models.Model):
    año = models.PositiveSmallIntegerField()
    mes = models.PositiveSmallIntegerField()
    valor = models.DecimalField(max_digits=14, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False


class PrecipitacionAnual(models.Model):
    mes = models.PositiveSmallIntegerField()
    valor = models.DecimalField(max_digits=14, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False


############################################################################################
class TeleVariables(models.Model):
    nombre = models.CharField(primary_key=True, max_length=20)
    valor = models.DecimalField("valor", max_digits=14, decimal_places=6, blank=True, null=True)


###########################################################################################

class ConfigVisualizar(models.Model):
    estacion = models.ForeignKey(Estacion, on_delete=models.SET_NULL, null=True)
    variable = models.ForeignKey(Variable, on_delete=models.SET_NULL, null=True)
    umbral_superior = models.DecimalField("Umbral superior", max_digits=14, decimal_places=6, blank=True, null=True)
    umbral_inferior = models.DecimalField("Umbral inferior", max_digits=14, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return str(self.estacion.est_nombre + ' - ' + self.variable.var_nombre)

    def get_absolute_url(self):
        return reverse('telemetria:configvisualizar_detail', kwargs={'pk':self.pk})

    class Meta:
        indexes = [
            models.Index(fields=['variable', 'estacion']),
        ]
        unique_together = ('estacion', 'variable')


###########################################################################################

class AlarmaEmail(models.Model):
    email = models.EmailField(unique=True)


class AlarmaTipoEstado(models.Model):
    nombre = models.CharField(max_length=15, unique=True)
    descripcion = models.CharField(max_length=250)

    ## 0 NORMAL
    ## 1 EXPECTANTE  mas de 1 hora sin transmitir pero menos del periodo de alerta
    ## 2 FALLIDO ha superado el periodo de tolerancia. Se genera una alarma


class AlarmaEstado(models.Model):
    estacion = models.ForeignKey(Estacion, on_delete=models.SET_NULL, null=True)
    estado = models.ForeignKey(AlarmaTipoEstado, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['estacion', 'estado', 'fecha']),
            models.Index(fields=['estacion', 'fecha', 'estado']),
            models.Index(fields=['estado', 'estacion', 'fecha']),
            models.Index(fields=['estado', 'fecha', 'estacion']),
            models.Index(fields=['fecha', 'estacion', 'estado']),
            models.Index(fields=['fecha', 'estado', 'estacion']),
        ]