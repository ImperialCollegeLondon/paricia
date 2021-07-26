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

from .models import consulta

def consultar_vacios(estacion_id, variable_id):
    sql = """
    WITH 
    umbral AS (SELECT 3600 AS val),
    medicion AS (
        SELECT fecha, EXTRACT(EPOCH FROM fecha)::int as epoch_ 
        FROM medicion_var%%var_id%%medicion m 
        WHERE estacion_id = %%est_id%% ORDER by m.fecha ASC
    ),
    diff1 AS (
        SELECT fecha,
        lead(med.epoch_) OVER (ORDER BY fecha ASC) - med.epoch_ AS diff_pre
        FROM medicion med
    ),
    diff2 AS (
        SELECT fecha, diff_pre, lag (diff_pre) OVER (ORDER BY fecha ASC) AS diff_pos
        FROM diff1
    ),
    uniendo AS (
        (SELECT fecha AS fecha, 0 AS diff_pre, NULL AS diff_pos FROM medicion ORDER BY fecha ASC LIMIT 1)
        UNION
        (SELECT * FROM diff2 WHERE diff_pre > (SELECT val FROM umbral) OR  diff_pos > (SELECT val FROM umbral))
        UNION
        (SELECT fecha AS fecha, 0 AS diff_pre, NULL AS diff_pos FROM medicion ORDER BY fecha DESC LIMIT 1)
    ), 
    reporte AS (
        select 
        (CASE WHEN diff_pre > (SELECT val FROM umbral) THEN 'vacio' ELSE 'datos' END) AS tipo,
        fecha AS fecha_inicio,
        lead(fecha) OVER (ORDER BY fecha) AS fecha_fin,
        (CASE WHEN diff_pre > (SELECT val FROM umbral) THEN diff_pre/3600 ELSE NULL END) AS intervalo_horas
        from uniendo ORDER BY fecha	
    )
    select tipo, fecha_inicio, fecha_fin, intervalo_horas from reporte WHERE fecha_fin IS NOT NULL ORDER BY fecha_inicio
    ;
    """
    sql = sql.replace("%%var_id%%", str(variable_id))
    sql = sql.replace("%%est_id%%", str(estacion_id))
    res = consulta.objects.raw(sql)
    return res
