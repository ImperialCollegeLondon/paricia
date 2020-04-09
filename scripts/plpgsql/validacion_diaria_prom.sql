-- FUNCTION: public.reporte_validacion_diario_temperaturaaire(integer, timestamp with time zone, timestamp with time zone)

DROP FUNCTION public.reporte_validacion_diario_temperaturaaire(integer, timestamp with time zone, timestamp with time zone);

CREATE OR REPLACE FUNCTION public.reporte_validacion_diario_temperaturaaire(
	_estacion_id integer,
	_fecha_inicio timestamp with time zone,
	_fecha_fin timestamp with time zone)
    RETURNS TABLE(numero_fila bigint, dia timestamp with time zone, valor numeric, maximo numeric, minimo numeric, porcentaje numeric, class_valor text, class_maximo text, class_minimo text, class_porcentaje text)
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE
    ROWS 1000
AS $BODY$

BEGIN
	RETURN QUERY
	WITH
	estacion AS (SELECT * FROM estacion_estacion est WHERE est.est_id = _estacion_id),
	variable AS (SELECT * FROM variable_variable var WHERE var.var_id = 2),
	--Seleccionar los datos de la tabla validados
    validacion AS (
        SELECT v.id, v.fecha, 0 AS tipo, v.valor, v.maximo, v.minimo, TRUE AS existe_en_validacion
        FROM validacion_temperaturaaire v WHERE v.estacion_id = (SELECT est_id FROM estacion) AND v.fecha >= _fecha_inicio AND v.fecha <= _fecha_fin
        AND (v.valor != 'Nan'::numeric AND v.maximo != 'Nan'::numeric AND v.minimo != 'Nan'::numeric )
        AND (v.valor IS NOT NULL AND v.maximo IS NOT NULL AND v.minimo IS NOT NULL)
    ),
    --Seleccionar los datos de la tabla medicion
    medicion AS (
        SELECT m.id, m.fecha, 1 AS tipo, m.valor, m.maximo, m.minimo,
            EXISTS(SELECT * FROM validacion v WHERE v.fecha = m.fecha AND v.valor = m.valor) AS existe_en_validacion
        FROM medicion_temperaturaaire m WHERE m.estacion_id = (SELECT est_id FROM estacion) AND m.fecha >= _fecha_inicio AND m.fecha <= _fecha_fin
        AND (m.valor != 'Nan'::numeric AND m.maximo != 'Nan'::numeric AND m.minimo != 'Nan'::numeric )
        AND (m.valor IS NOT NULL AND m.maximo IS NOT NULL AND m.minimo IS NOT NULL)
    ),
    --unir las tablas medicion y validacion en una tabla
    union_med_val AS (
        SELECT * FROM validacion UNION SELECT * FROM medicion
    ),
    --Seleccionar una serie única de los validados y los crudos
    tabla_base AS (
        SELECT
            --row_number() OVER (ORDER BY umv.fecha ASC, umv.tipo ASC, umv.id DESC) as numero_fila,
            *
        FROM union_med_val umv WHERE NOT (umv.existe_en_validacion = TRUE AND umv.tipo = 1)
    ),
    tabla_acumulada AS (
        SELECT date_trunc('day',tb.fecha) as dia, COUNT(tb.valor) numero_datos,
        AVG(tb.valor) as valor, AVG(tb.maximo) as maximo, AVG(tb.minimo) as minimo

        FROM tabla_base tb GROUP BY dia ORDER by dia
    ),

    tabla_datos_esperados AS (
        SELECT ta.dia, ta.numero_datos,
        (SELECT CAST(1440/f.fre_valor AS INT) ndatos FROM frecuencia_frecuencia f WHERE f.fre_valor <= 60
            and f.est_id_id = (SELECT e.est_id FROM estacion e) AND f.var_id_id = 1
            AND f.fre_fecha_ini <= ta.dia
            AND (f.fre_fecha_fin >= ta.dia OR f.fre_fecha_fin IS NULL)
        ORDER BY f.fre_fecha_ini DESC LIMIT 1) as numero_datos_esperado
        FROM tabla_acumulada ta ORDER by ta.dia
    ),
    tabla_calculo AS (
        SELECT tde.dia, tde.numero_datos, tde.numero_datos_esperado,
        (tde.numero_datos::decimal/tde.numero_datos_esperado)*100 as porcentaje
        FROM tabla_datos_esperados tde
    ),
    reporte AS (
        SELECT
        row_number() OVER (ORDER BY ta.dia ASC) as numero_fila,
        ta.dia, ta.valor, ta.maximo, ta.minimo,
        (SELECT tc.porcentaje FROM tabla_calculo tc WHERE tc.dia = ta.dia) as porcentaje,
        ta.valor > (SELECT var_maximo FROM variable) OR ta.valor < (SELECT var_minimo FROM variable) AS valor_error,
        ta.maximo > (SELECT var_maximo FROM variable) OR ta.maximo < (SELECT var_minimo FROM variable) AS maximo_error,
        ta.minimo > (SELECT var_maximo FROM variable) OR ta.minimo < (SELECT var_minimo FROM variable) AS minimo_error,
        (SELECT tc.porcentaje FROM tabla_calculo tc WHERE tc.dia = ta.dia) < (SELECT umbral_completo FROM variable) as porcentaje_error
        FROM tabla_acumulada ta

    ),
    reporte_css AS  (
        SELECT *,
            CASE WHEN r.valor_error THEN 'valor error' ELSE 'valor normal' END AS class_valor,
            CASE WHEN r.maximo_error THEN 'maximo error' ELSE 'maximo normal' END AS class_maximo,
            CASE WHEN r.minimo_error THEN 'minimo error' ELSE 'minimo normal' END AS class_minimo,
            CASE WHEN r.porcentaje_error THEN 'porcentaje error' ELSE 'porcentaje normal' END AS class_porcentaje
        FROM reporte r

    )
    --SELECT * FROM fechas0 order by fecha_grupo
    SELECT rc.numero_fila,rc.dia, rc.valor, rc.maximo, rc.minimo, rc.porcentaje,
    rc.class_valor, rc.class_maximo, rc.class_minimo, rc.class_porcentaje FROM reporte_css rc;

END;

$BODY$;

ALTER FUNCTION public.reporte_validacion_diario_temperaturaaire(integer, timestamp with time zone, timestamp with time zone)
    OWNER TO postgres;

