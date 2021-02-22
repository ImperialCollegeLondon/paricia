# -*- coding: utf-8 -*-

################################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos (iMHEA)
# basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#         Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS), Ecuador.
#         Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones creadoras,
#              ya sea en uso total o parcial del código.

from __future__ import unicode_literals

from django.db import models
from estacion.models import Estacion
from django.urls import reverse

class PermisosMedicion(models.Model):

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ('validar', 'usar interfaz de validación'),
        )


# # Este modelo posiblemente se lo usaría para compatibilidad con SEDC
# # Se necesita al menos en: reportes/views/datos_json_horarios
# # clase para almacenar los datos crudos del sistema
# class Medicion(models.Model):
#     med_id = models.BigAutoField("Id", primary_key=True)
#     var_id = models.ForeignKey(Variable, models.SET_NULL, blank=True, null=True, verbose_name="Variable")
#     est_id = models.ForeignKey(Estacion, models.SET_NULL, blank=True, null=True, verbose_name="Estación")
#     med_fecha = models.DateTimeField("Fecha")
#     med_valor = models.DecimalField("Valor", max_digits=14, decimal_places=6, blank=True, null=True)
#     med_maximo = models.DecimalField("Máximo", max_digits=14, decimal_places=6, blank=True, null=True)
#     med_minimo = models.DecimalField("Mínimo", max_digits=14, decimal_places=6, blank=True, null=True)
#     med_estado = models.NullBooleanField("Estado", default=True)
#
#     def __str__(self):
#         return str(self.med_fecha)
#
#     def get_absolute_url(self):
#         return reverse('medicion:medicion_index')
#
#     class Meta:
#         default_permissions = ()
#         ordering = ('med_fecha',)


class VientoPolar(models.Model):
    fecha = models.DateTimeField("Fecha")
    velocidad = models.DecimalField("Velocidad", max_digits=14, decimal_places=6, null=True)
    direccion = models.DecimalField("Direccion", max_digits=14, decimal_places=6, null=True)

    class Meta:
        ### Para que no se cree en la migracion
        default_permissions = ()
        managed = False


class CaudalViaEstacion(models.Model):
    id = models.AutoField("Id", primary_key=True)
    est_id = models.ForeignKey(Estacion, models.SET_NULL, blank=True, null=True, verbose_name="Estación")
    fecha_inicio = models.DateTimeField("Fecha inicio")
    fecha_fin = models.DateTimeField("Fecha fin")
    valor = models.DecimalField("Valor", max_digits=14, decimal_places=6, blank=True, null=True)
    calibracion_regleta_sensor = models.NullBooleanField("Calibracion", default=False)


class CurvaDescarga(models.Model):
    id = models.AutoField("Id", primary_key=True)
    estacion = models.ForeignKey(Estacion, on_delete=models.SET_NULL, null=True, verbose_name="Estación")
    fecha = models.DateTimeField("Fecha")
    funcion = models.CharField("Función", max_length=80)

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse('medicion:curvadescarga_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ('id',)
        unique_together = ('estacion', 'fecha')


class CursorDbclima(models.Model):
    estacion_id = models.IntegerField(primary_key=True)
    fecha = models.DateTimeField(null=True)


class CursorEmaaphidro(models.Model):
    est_id_paramh2o = models.IntegerField(primary_key=True)
    est_id_emaaphidro = models.SmallIntegerField()
    est_codigo = models.CharField(max_length=4)
    fecha = models.DateTimeField()

##############################################################

class ValorDecimal:
    max_dig = 6
    dec_pla = 2

    def __init__(self, max_dig, dec_pla):
        self.max_dig = max_dig
        self.dec_pla = dec_pla


class DigVar:
    v1 = ValorDecimal(max_dig=6, dec_pla=2)
    v2 = ValorDecimal(max_dig=5, dec_pla=2)
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
    v13 = ValorDecimal(max_dig=14, dec_pla=6)
    v14 = ValorDecimal(max_dig=14, dec_pla=6)
    v15 = ValorDecimal(max_dig=14, dec_pla=6)
    v16 = ValorDecimal(max_dig=14, dec_pla=6)
    v17 = ValorDecimal(max_dig=14, dec_pla=6)
    v18 = ValorDecimal(max_dig=14, dec_pla=6)
    v19 = ValorDecimal(max_dig=14, dec_pla=6)
    v20 = ValorDecimal(max_dig=14, dec_pla=6)
    v21 = ValorDecimal(max_dig=14, dec_pla=6)
    v22 = ValorDecimal(max_dig=14, dec_pla=6)
    v23 = ValorDecimal(max_dig=14, dec_pla=6)
    v24 = ValorDecimal(max_dig=14, dec_pla=6)

    # variable con profundidad
    v101 = ValorDecimal(max_dig=6, dec_pla=2)
    v102 = ValorDecimal(max_dig=6, dec_pla=2)
    v103 = ValorDecimal(max_dig=6, dec_pla=2)
    v104 = ValorDecimal(max_dig=7, dec_pla=2)
    v105 = ValorDecimal(max_dig=6, dec_pla=2)
    v106 = ValorDecimal(max_dig=6, dec_pla=2)
    v107 = ValorDecimal(max_dig=6, dec_pla=2)
    v108 = ValorDecimal(max_dig=6, dec_pla=2)


class Var1Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v1.max_dig, decimal_places=DigVar.v1.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var2Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v2.max_dig, decimal_places=DigVar.v2.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var3Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v3.max_dig, decimal_places=DigVar.v3.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var4Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v4.max_dig, decimal_places=DigVar.v4.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var5Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v5.max_dig, decimal_places=DigVar.v5.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var6Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v6.max_dig, decimal_places=DigVar.v6.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var7Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v7.max_dig, decimal_places=DigVar.v7.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var8Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v8.max_dig, decimal_places=DigVar.v8.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var9Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v9.max_dig, decimal_places=DigVar.v9.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var10Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v10.max_dig, decimal_places=DigVar.v10.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var11Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v11.max_dig, decimal_places=DigVar.v11.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v11.max_dig, decimal_places=DigVar.v11.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v11.max_dig, decimal_places=DigVar.v11.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var12Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v12.max_dig, decimal_places=DigVar.v12.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v12.max_dig, decimal_places=DigVar.v12.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v12.max_dig, decimal_places=DigVar.v12.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var13Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v13.max_dig, decimal_places=DigVar.v13.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var14Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha_importacion = models.DateTimeField("Fecha Importación")
    fecha_inicio = models.DateTimeField("Fecha inicio datos")
    fecha = models.DateTimeField("Fecha fin datos")
    calibrado = models.BooleanField("Calibrado")
    valor = models.DecimalField("Valor", max_digits=DigVar.v14.max_dig, decimal_places=DigVar.v14.dec_pla, null=True)
    incertidumbre = models.DecimalField("Incertidumbre", max_digits=DigVar.v14.max_dig, decimal_places=DigVar.v14.dec_pla, null=True)
    comentario = models.CharField("Comentario", null=True, max_length=250)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha_importacion']),
            models.Index(fields=['estacion_id', 'fecha_inicio', 'fecha']),
            models.Index(fields=['fecha_importacion']),
        ]


class Var15Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v15.max_dig, decimal_places=DigVar.v15.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v15.max_dig, decimal_places=DigVar.v15.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v15.max_dig, decimal_places=DigVar.v15.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var16Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v16.max_dig, decimal_places=DigVar.v16.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v16.max_dig, decimal_places=DigVar.v16.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v16.max_dig, decimal_places=DigVar.v16.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var17Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v17.max_dig, decimal_places=DigVar.v17.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v17.max_dig, decimal_places=DigVar.v17.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v17.max_dig, decimal_places=DigVar.v17.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var18Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v18.max_dig, decimal_places=DigVar.v18.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v18.max_dig, decimal_places=DigVar.v18.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v18.max_dig, decimal_places=DigVar.v18.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var19Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v19.max_dig, decimal_places=DigVar.v19.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v19.max_dig, decimal_places=DigVar.v19.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v19.max_dig, decimal_places=DigVar.v19.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]

    
class Var20Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v20.max_dig, decimal_places=DigVar.v20.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v20.max_dig, decimal_places=DigVar.v20.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v20.max_dig, decimal_places=DigVar.v20.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]

    
class Var21Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v21.max_dig, decimal_places=DigVar.v21.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v21.max_dig, decimal_places=DigVar.v21.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v21.max_dig, decimal_places=DigVar.v21.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var22Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v22.max_dig, decimal_places=DigVar.v22.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v22.max_dig, decimal_places=DigVar.v22.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v22.max_dig, decimal_places=DigVar.v22.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var23Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v23.max_dig, decimal_places=DigVar.v23.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v23.max_dig, decimal_places=DigVar.v23.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v23.max_dig, decimal_places=DigVar.v23.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]


class Var24Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    valor = models.DecimalField("Valor", max_digits=DigVar.v24.max_dig, decimal_places=DigVar.v24.dec_pla, null=True)
    maximo = models.DecimalField("Máximo", max_digits=DigVar.v24.max_dig, decimal_places=DigVar.v24.dec_pla, null=True)
    minimo = models.DecimalField("Mínimo", max_digits=DigVar.v24.max_dig, decimal_places=DigVar.v24.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'fecha']),
            models.Index(fields=['fecha', 'estacion_id']),
        ]

## Variables creadas para boya con diferentes profundidades

## Temperatura agua
##      Profundidad en centimetros
##      Unidad : grados Celcius
class Var101Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    valor = models.DecimalField("Valor", max_digits=DigVar.v101.max_dig, decimal_places=DigVar.v101.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'profundidad', 'fecha']),
        ]


## pH Acidez agua
##      Profundidad en centimetros
##      Unidad : pH
class Var102Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    valor = models.DecimalField("Valor", max_digits=DigVar.v102.max_dig, decimal_places=DigVar.v102.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'profundidad', 'fecha']),
        ]


## ORP : Potencial REDOX en agua
##      Profundidad en centimetros
##      Unidad : mV
class Var103Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    valor = models.DecimalField("Valor", max_digits=DigVar.v103.max_dig, decimal_places=DigVar.v103.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'profundidad', 'fecha']),
        ]


## Turp Turbidez en agua
##      Profundidad en centimetros
##      Unidad : NTU
class Var104Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    valor = models.DecimalField("Valor", max_digits=DigVar.v104.max_dig, decimal_places=DigVar.v104.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'profundidad', 'fecha']),
        ]


## Chl : Concentracion Cloro
##      Profundidad en centimetros
##      Unidad : ug/l
class Var105Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    valor = models.DecimalField("Valor", max_digits=DigVar.v105.max_dig, decimal_places=DigVar.v105.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'profundidad', 'fecha']),
        ]


## HDO : Oxígeno disuelto en agua
##      Profundidad en centimetros
##      Unidad : mg/l
class Var106Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    valor = models.DecimalField("Valor", max_digits=DigVar.v106.max_dig, decimal_places=DigVar.v106.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'profundidad', 'fecha']),
        ]


## % HDO : Porcentaje Oxígeno disuelto en agua
##      Profundidad en centimetros
##      Unidad : mg/l
class Var107Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    valor = models.DecimalField("Valor", max_digits=DigVar.v107.max_dig, decimal_places=DigVar.v107.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'profundidad', 'fecha']),
        ]


## BGAPC : Ficocianina
##      Profundidad en centimetros
##      Unidad :
class Var108Medicion(models.Model):
    id = models.BigAutoField("Id", primary_key=True)
    estacion_id = models.PositiveIntegerField("estacion_id")
    fecha = models.DateTimeField("Fecha")
    profundidad = models.PositiveSmallIntegerField("Profundidad")
    valor = models.DecimalField("Valor", max_digits=DigVar.v108.max_dig, decimal_places=DigVar.v108.dec_pla, null=True)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=['estacion_id', 'profundidad', 'fecha']),
        ]
