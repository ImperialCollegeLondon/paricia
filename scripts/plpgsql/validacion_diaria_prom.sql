DROP FUNCTION public.reporte_validacion_diario_modelo(integer, timestamp with time zone, timestamp with time zone);
CREATE OR REPLACE FUNCTION public.reporte_validacion_diario_modelo(
	_estacion_id integer,
	_fecha_inicio timestamp with time zone,
	_fecha_fin timestamp with time zone)
    RETURNS TABLE(id bigint, dia timestamp with time zone,
    	valor numeric, maximo numeric, minimo numeric, porcentaje numeric,
        valor_error boolean, maximo_error boolean, minimo_error boolean,
        valor_numero numeric, maximo_numero numeric, minimo_numero numeric, estado boolean)
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE
    ROWS 1000
AS $BODY$

BEGIN
	RETURN QUERY
	WITH
	estacion AS (SELECT * FROM estacion_estacion est WHERE est.est_id = _estacion_id),
	variable AS (SELECT * FROM variable_variable var WHERE var.var_id = __var_id__),
	--Seleccionar los datos de la tabla validados
    validacion AS (
        SELECT v.id, v.fecha, 0 AS tipo, v.valor, v.maximo, v.minimo, TRUE AS existe_en_validacion
        FROM validacion_modelo v WHERE v.estacion_id = (SELECT est_id FROM estacion) AND v.fecha >= _fecha_inicio AND v.fecha <= _fecha_fin

    ),
    --Seleccionar los datos de la tabla medicion
    medicion AS (
        SELECT m.id, m.fecha, 1 AS tipo, m.valor, m.maximo, m.minimo,
            EXISTS(SELECT * FROM validacion v WHERE v.fecha = m.fecha AND v.valor = m.valor) AS existe_en_validacion
        FROM medicion_modelo m WHERE m.estacion_id = (SELECT est_id FROM estacion) AND m.fecha >= _fecha_inicio AND m.fecha <= _fecha_fin
    ),
    --unir las tablas medicion y validacion en una tabla
    union_med_val AS (
        SELECT * FROM validacion UNION SELECT * FROM medicion
    ),
    --Seleccionar una serie nica de los validados y los crudos
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
        ROUND((tde.numero_datos::decimal/tde.numero_datos_esperado)*100,2) as porcentaje
        FROM tabla_datos_esperados tde
    ),
    tabla_valores_sos AS (
        SELECT ta.dia,
            (SELECT COUNT(tb.valor) nsvalor FROM tabla_base tb WHERE date(tb.fecha) = ta.dia
                AND (tb.valor>(SELECT var_maximo FROM variable) OR tb.valor < (SELECT var_minimo FROM variable) )
            )::numeric as numero_valor_sospechoso,
            (SELECT COUNT(tb.maximo) nsvalor FROM tabla_base tb WHERE date(tb.fecha) = ta.dia
                AND (tb.maximo>(SELECT var_maximo FROM variable) OR tb.maximo < (SELECT var_minimo FROM variable) )
            )::numeric as numero_maximo_sospechoso,
            (SELECT COUNT(tb.minimo) nsvalor FROM tabla_base tb WHERE date(tb.fecha) = ta.dia
                AND (tb.minimo>(SELECT var_maximo FROM variable) OR tb.minimo < (SELECT var_minimo FROM variable) )
            )::numeric as numero_minimo_sospechoso
        FROM tabla_acumulada ta ORDER BY ta.dia
    ),
    reporte AS (
        SELECT
        row_number() OVER (ORDER BY ta.dia ASC) as id,
        ta.dia, ROUND(ta.valor,2)::numeric, ROUND(ta.maximo,2)::numeric, ROUND(ta.minimo,2)::numeric,
        (SELECT tc.porcentaje FROM tabla_calculo tc WHERE tc.dia = ta.dia) as porcentaje,
        ta.valor > (SELECT var_maximo FROM variable) OR ta.valor < (SELECT var_minimo FROM variable) AS valor_error,
        ta.maximo > (SELECT var_maximo FROM variable) OR ta.maximo < (SELECT var_minimo FROM variable) AS maximo_error,
        ta.minimo > (SELECT var_maximo FROM variable) OR ta.minimo < (SELECT var_minimo FROM variable) AS minimo_error,
        (SELECT tvs.numero_valor_sospechoso FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia) as valor_numero,
        (SELECT tvs.numero_maximo_sospechoso FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia) as maximo_numero,
        (SELECT tvs.numero_minimo_sospechoso FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia) as minimo_numero,
        TRUE as estado
        FROM tabla_acumulada ta

    )
    SELECT * FROM reporte;

END;
$BODY$;

ALTER FUNCTION public.reporte_validacion_diario_modelo(integer, timestamp with time zone, timestamp with time zone)
    OWNER TO postgres;