########################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos
# (iMHEA)basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#           Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS),
#           Ecuador.
#           Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones
#  creadoras, ya sea en uso total o parcial del código.
########################################################################################

from django.db import models


class ValidationReport(models.Model):
    """
    NOTE: No idea what this one does. Why is there a model definition outside of
    models.py, anyway?
    """

    id = models.BigAutoField(primary_key=True)
    estado = models.BooleanField()
    fecha = models.DateTimeField()
    valor_seleccionado = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    valor = models.DecimalField(max_digits=14, decimal_places=6, null=True)
    variacion_consecutiva = models.DecimalField(
        max_digits=14, decimal_places=6, null=True
    )
    comentario = models.CharField(max_length=350)
    class_fila = models.CharField(max_length=30)
    class_fecha = models.CharField(max_length=30)
    class_validacion = models.CharField(max_length=30)
    class_valor = models.CharField(max_length=30)
    class_variacion_consecutiva = models.CharField(max_length=30)
    class_stddev_error = models.CharField(max_length=30)

    class Meta:
        managed = False


class LevelFunctionTable(models.Model):
    """
    NOTE: No idea what this one does. Why is there a model definition outside of
    models.py, anyway?
    """

    id = models.SmallIntegerField(primary_key=True)
    funcion = models.CharField("Función", max_length=80)
    level_inf = models.DecimalField("Level Inf. (cm)", max_digits=5, decimal_places=1)
    level_1 = models.DecimalField("Level 1", max_digits=5, decimal_places=1)
    level_2 = models.DecimalField("Level 2", max_digits=5, decimal_places=1)
    level_3 = models.DecimalField("Level 3", max_digits=5, decimal_places=1)
    level_4 = models.DecimalField("Level 4", max_digits=5, decimal_places=1)
    level_5 = models.DecimalField("Level 5", max_digits=5, decimal_places=1)
    level_sup = models.DecimalField("Level Sup. (cm)", max_digits=5, decimal_places=1)
    flow_inf = models.DecimalField("Flow Inf. (cm)", max_digits=10, decimal_places=5)
    flow_1 = models.DecimalField("Flow 1", max_digits=10, decimal_places=5)
    flow_2 = models.DecimalField("Flow 2", max_digits=10, decimal_places=5)
    flow_3 = models.DecimalField("Flow 3", max_digits=10, decimal_places=5)
    flow_4 = models.DecimalField("Flow 4", max_digits=10, decimal_places=5)
    flow_5 = models.DecimalField("Flow 5", max_digits=10, decimal_places=5)
    flow_sup = models.DecimalField("Flow Sup. (cm)", max_digits=10, decimal_places=5)

    class Meta:
        managed = False
        default_permissions = ()
        ordering = ("level_inf",)


def level_function_table(curvadescarga_id):
    sql = """
    WITH base AS (
        select nv.id,
        nv.funcion,
        coalesce( lag(nv.level) OVER (ORDER BY nv.level ASC), 0.0 ) AS level_inf,
        nv.level AS level_sup
        from medicion_levelfuncion nv 
        WHERE nv.curvadescarga_id = %s
    ),
    leveles AS (
        select 
        b.id,
        b.funcion,
        b.level_inf,
        (SELECT  ROUND(b.level_inf + (b.level_sup - b.level_inf)/6.0, 1)) AS level1,
        (SELECT  ROUND(b.level_inf + 2*(b.level_sup - b.level_inf)/6.0, 1)) AS level2,
        (SELECT  ROUND(b.level_inf + 3*(b.level_sup - b.level_inf)/6.0, 1)) AS level3,
        (SELECT  ROUND(b.level_inf + 4*(b.level_sup - b.level_inf)/6.0, 1)) AS level4,
        (SELECT  ROUND(b.level_inf + 5*(b.level_sup - b.level_inf)/6.0, 1)) AS level5,
        b.level_sup 
        from base b	ORDER BY b.level_inf
    ),
    funciones AS (
        SELECT *,
        replace(n.funcion, 'H', CAST(n.level_inf AS VarChar) ) AS f_inf,
        replace(n.funcion, 'H', CAST(n.level1 AS VarChar) ) AS f1,
        replace(n.funcion, 'H', CAST(n.level2 AS VarChar) ) AS f2,
        replace(n.funcion, 'H', CAST(n.level3 AS VarChar) ) AS f3,
        replace(n.funcion, 'H', CAST(n.level4 AS VarChar) ) AS f4,
        replace(n.funcion, 'H', CAST(n.level5 AS VarChar) ) AS f5,
        replace(n.funcion, 'H', CAST(n.level_sup AS VarChar) ) AS f_sup
        from leveles n
    )
    select 	
    f.id,
    f.funcion,
    f.level_inf,
    f.level1,
    f.level2,
    f.level3,
    f.level4,
    f.level5,
    f.level_sup,
    (SELECT eval_math(f.f_inf)) AS flow_inf,
    (SELECT eval_math(f.f1)) AS flow1,
    (SELECT eval_math(f.f2)) AS flow2,
    (SELECT eval_math(f.f3)) AS flow3,
    (SELECT eval_math(f.f4)) AS flow4,
    (SELECT eval_math(f.f5)) AS flow5,
    (SELECT eval_math(f.f_sup)) AS flow_sup
    FROM funciones f ORDER BY f.level_inf;    
    """
    return LevelFunctionTable.objects.raw(sql, [curvadescarga_id])
