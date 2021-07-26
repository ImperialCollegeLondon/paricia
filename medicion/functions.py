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

from django.db import models


class ReporteValidacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    estado = models.BooleanField()
    fecha = models.DateTimeField()
    valor_seleccionado = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    valor = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    variacion_consecutiva = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    comentario = models.CharField(max_length=350)
    class_fila = models.CharField(max_length=30)
    class_fecha = models.CharField(max_length=30)
    class_validacion = models.CharField(max_length=30)
    class_valor = models.CharField(max_length=30)
    class_variacion_consecutiva = models.CharField(max_length=30)
    class_stddev_error = models.CharField(max_length=30)
    class Meta:
        managed = False ### Para que no se cree en la migracion

    class Meta:
        ### Para que no se cree en la migracion
        managed = False


class NivelFuncionTabla(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    funcion = models.CharField("Función", max_length=80)
    nivel_inf = models.DecimalField("Nivel Inf. (cm)", max_digits=5, decimal_places=1)
    nivel_1 = models.DecimalField("Nivel 1", max_digits=5, decimal_places=1)
    nivel_2 = models.DecimalField("Nivel 2", max_digits=5, decimal_places=1)
    nivel_3 = models.DecimalField("Nivel 3", max_digits=5, decimal_places=1)
    nivel_4 = models.DecimalField("Nivel 4", max_digits=5, decimal_places=1)
    nivel_5 = models.DecimalField("Nivel 5", max_digits=5, decimal_places=1)
    nivel_sup = models.DecimalField("Nivel Sup. (cm)", max_digits=5, decimal_places=1)
    caudal_inf = models.DecimalField("Caudal Inf. (cm)", max_digits=10, decimal_places=5)
    caudal_1 = models.DecimalField("Caudal 1", max_digits=10, decimal_places=5)
    caudal_2 = models.DecimalField("Caudal 2", max_digits=10, decimal_places=5)
    caudal_3 = models.DecimalField("Caudal 3", max_digits=10, decimal_places=5)
    caudal_4 = models.DecimalField("Caudal 4", max_digits=10, decimal_places=5)
    caudal_5 = models.DecimalField("Caudal 5", max_digits=10, decimal_places=5)
    caudal_sup = models.DecimalField("Caudal Sup. (cm)", max_digits=10, decimal_places=5)

    class Meta:
        managed = False
        default_permissions = ()
        ordering = ('nivel_inf',)


def nivelfunciontabla(curvadescarga_id):
    sql = """
    WITH base AS (
        select nv.id,
        nv.funcion,
        coalesce( lag(nv.nivel) OVER (ORDER BY nv.nivel ASC), 0.0 ) AS nivel_inf,
        nv.nivel AS nivel_sup
        from medicion_nivelfuncion nv 
        WHERE nv.curvadescarga_id = %s
    ),
    niveles AS (
        select 
        b.id,
        b.funcion,
        b.nivel_inf,
        (SELECT  ROUND(b.nivel_inf + (b.nivel_sup - b.nivel_inf)/6.0, 1)) AS nivel1,
        (SELECT  ROUND(b.nivel_inf + 2*(b.nivel_sup - b.nivel_inf)/6.0, 1)) AS nivel2,
        (SELECT  ROUND(b.nivel_inf + 3*(b.nivel_sup - b.nivel_inf)/6.0, 1)) AS nivel3,
        (SELECT  ROUND(b.nivel_inf + 4*(b.nivel_sup - b.nivel_inf)/6.0, 1)) AS nivel4,
        (SELECT  ROUND(b.nivel_inf + 5*(b.nivel_sup - b.nivel_inf)/6.0, 1)) AS nivel5,
        b.nivel_sup 
        from base b	ORDER BY b.nivel_inf
    ),
    funciones AS (
        SELECT *,
        replace(n.funcion, 'H', CAST(n.nivel_inf AS VarChar) ) AS f_inf,
        replace(n.funcion, 'H', CAST(n.nivel1 AS VarChar) ) AS f1,
        replace(n.funcion, 'H', CAST(n.nivel2 AS VarChar) ) AS f2,
        replace(n.funcion, 'H', CAST(n.nivel3 AS VarChar) ) AS f3,
        replace(n.funcion, 'H', CAST(n.nivel4 AS VarChar) ) AS f4,
        replace(n.funcion, 'H', CAST(n.nivel5 AS VarChar) ) AS f5,
        replace(n.funcion, 'H', CAST(n.nivel_sup AS VarChar) ) AS f_sup
        from niveles n
    )
    select 	
    f.id,
    f.funcion,
    f.nivel_inf,
    f.nivel1,
    f.nivel2,
    f.nivel3,
    f.nivel4,
    f.nivel5,
    f.nivel_sup,
    (SELECT eval_math(f.f_inf)) AS caudal_inf,
    (SELECT eval_math(f.f1)) AS caudal1,
    (SELECT eval_math(f.f2)) AS caudal2,
    (SELECT eval_math(f.f3)) AS caudal3,
    (SELECT eval_math(f.f4)) AS caudal4,
    (SELECT eval_math(f.f5)) AS caudal5,
    (SELECT eval_math(f.f_sup)) AS caudal_sup
    FROM funciones f ORDER BY f.nivel_inf;    
    """
    nivelfunciontabla = NivelFuncionTabla.objects.raw(sql, [curvadescarga_id])
    return nivelfunciontabla
