-- FUNCTION: public.reporte_validacion_diario_agua(integer, timestamp with time zone, timestamp with time zone, numeric, numeric)

-- DROP FUNCTION public.reporte_validacion_diario_agua(integer, timestamp with time zone, timestamp with time zone, numeric, numeric);

CREATE OR REPLACE FUNCTION public.reporte_validacion_diario_agua(
	_estacion_id integer,
	_fecha_inicio timestamp with time zone,
	_fecha_fin timestamp with time zone,
	_var_maximo numeric,
	_var_minimo numeric)
    RETURNS TABLE(id bigint, fecha timestamp with time zone, fecha_error numeric, fecha_numero numeric, nivel numeric, caudal numeric, porcentaje numeric, porcentaje_error boolean, nivel_error boolean, nivel_numero numeric, caudal_error boolean, caudal_numero numeric, estado boolean, validado boolean) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
    
AS $BODY$

BEGIN
	RETURN QUERY
	--pruebas_validacion_diaria_agua
    WITH
    estacion AS (SELECT * FROM estacion_estacion est WHERE est.est_id = _estacion_id),
    variable AS (SELECT * FROM variable_variable var WHERE var.var_id = 11),
    caudal AS (SELECT * FROM variable_variable var WHERE var.var_id = 10),
    --Seleccionar los datos de la tabla validados
    validacion AS (
        SELECT v.id, v.fecha, 0 AS tipo, v.nivel as nivel,
        v.caudal as caudal,
        TRUE AS existe_en_validacion
        FROM validacion_agua v WHERE v.estacion_id = (SELECT est_id FROM estacion)
        AND v.fecha >= _fecha_inicio AND v.fecha <= _fecha_fin
    ),
    --Seleccionar los datos de la tabla medicion
    medicion AS (
        SELECT m_nag.id, m_nag.fecha, 1 AS tipo, CASE WHEN m_nag.valor = 'NaN' THEN NULL ELSE m_nag.valor END AS nivel,
        CASE WHEN m_cau.valor = 'NaN' THEN NULL ELSE m_cau.valor END AS caudal,
            EXISTS(SELECT * FROM validacion v_nag WHERE v_nag.fecha = m_nag.fecha) AS existe_en_validacion
        FROM medicion_var11medicion m_nag, medicion_var10medicion m_cau WHERE m_nag.estacion_id = (SELECT est_id FROM estacion)
        AND m_nag.fecha >= _fecha_inicio AND m_nag.fecha <= _fecha_fin AND m_nag.fecha = m_cau.fecha AND m_cau.estacion_id = m_nag.estacion_id
        AND NOT (m_nag.valor IS NULL OR m_nag.valor = 'NaN'::numeric) AND NOT (m_cau.valor IS NULL OR m_nag.valor = 'NAN'::numeric)
        AND NOT (m_cau.valor IS NULL OR m_cau.valor = 'NaN'::numeric)
    ),
    --unir las tablas medicion y validacion en una tabla
    union_med_val AS (
        SELECT * FROM validacion UNION SELECT * FROM medicion
    ),
    --Seleccionar una serie unica de los validados y los crudos
    --Seleccionar una serie unica de los validados y los crudos
    tabla_base AS (
        SELECT *
        FROM union_med_val umv WHERE NOT (umv.existe_en_validacion = TRUE AND umv.tipo = 1)
    ),
    -- valores duplicados por cada fecha
    tabla_duplicados AS (
        SELECT tb.fecha, date_trunc('day',tb.fecha) as dia, COUNT(*) AS num_duplicados
        FROM tabla_base tb
        GROUP BY tb.fecha
        HAVING COUNT(*) > 1
        ORDER BY tb.fecha
    ),
    -- acumular los datos a diario
    tabla_acumulada AS (
        SELECT date_trunc('day',tb.fecha) as dia, COUNT(tb.nivel) numero_datos,
        ROUND(AVG(tb.nivel),2) as nivel,
        ROUND(AVG(tb.caudal),2) as caudal,
        bool_and(tb.existe_en_validacion) as existe_en_validacion
        FROM tabla_base tb GROUP BY dia ORDER by dia
    ),
    -- Numero de datos esperados por d?a
    tabla_datos_esperados AS (
        SELECT ta.dia, SUM(ta.numero_datos) as numero_datos,
        (SELECT CAST(1440/f.fre_valor AS INT) ndatos FROM frecuencia_frecuencia f WHERE f.fre_valor <= 60
            and f.est_id_id = (SELECT e.est_id FROM estacion e) AND f.var_id_id = (SELECT var_id FROM variable)
            AND f.fre_fecha_ini <= ta.dia
            AND (f.fre_fecha_fin >= ta.dia OR f.fre_fecha_fin IS NULL)
        ORDER BY f.fre_fecha_ini DESC LIMIT 1) as numero_datos_esperado
        FROM tabla_acumulada ta GROUP BY ta.dia ORDER by ta.dia
    ),
    tabla_calculo AS (
        SELECT tde.dia, tde.numero_datos, tde.numero_datos_esperado,
        ROUND((tde.numero_datos::decimal/tde.numero_datos_esperado)*100,2) as porcentaje,
        CASE WHEN ROUND((tde.numero_datos::decimal/tde.numero_datos_esperado)*100,2) < (SELECT umbral_completo FROM variable)
        THEN TRUE ELSE FALSE END AS porcentaje_error
        FROM tabla_datos_esperados tde
    ),
    tabla_valores_sos AS (
        SELECT ta.dia,
            (SELECT COUNT(tb.nivel) FROM tabla_base tb WHERE date(tb.fecha) = ta.dia
                AND (tb.nivel>_var_maximo OR tb.nivel < _var_minimo)
            )::numeric as ns_nivel,

            (SELECT COUNT(tb.caudal) FROM tabla_base tb WHERE date(tb.fecha) = ta.dia
                AND (tb.caudal > (SELECT var_maximo FROM caudal) OR tb.caudal < (SELECT var_minimo FROM caudal) )
            )::numeric as ns_caudal

        FROM tabla_calculo ta ORDER BY ta.dia
    ),
    -- revision de lapsos de tiempo entre fechas
    lapsos_dias AS (
        SELECT
            ff.dia,
            row_number() OVER (ORDER BY ff.dia ASC) as fecha_grupo,
            EXTRACT(EPOCH FROM ff.dia - lag(ff.dia) OVER (ORDER BY ff.dia ASC))/86400 as lapso_tiempo
        FROM (SELECT tc.dia FROM tabla_calculo tc) ff ORDER BY dia ASC
    ),
    error_lapsos AS (
        SELECT *,
            CASE WHEN fecha_grupo = 1 THEN 1 ELSE
            CASE WHEN lapso_tiempo < 1 THEN 0
                 WHEN lapso_tiempo > 1 THEN 3
                 WHEN LEAD (lapso_tiempo) OVER (ORDER BY ld.dia) > 1 THEN 2
                ELSE 1
            END
        END AS fecha_valida
        FROM lapsos_dias ld
    ),
    reporte AS (
        SELECT
        row_number() OVER (ORDER BY ta.dia ASC) as id,
        ta.dia, (SELECT el.fecha_valida FROM error_lapsos el WHERE el.dia = ta.dia)::numeric as dia_error,
        (SELECT SUM(td.num_duplicados) FROM tabla_duplicados td WHERE td.dia = ta.dia)::numeric as fecha_numero,
        ta.nivel::numeric as nivel,
        ta.caudal::numeric as caudal,
        (SELECT tc.porcentaje FROM tabla_calculo tc WHERE tc.dia = ta.dia) as porcentaje,
        (SELECT tc.porcentaje_error FROM tabla_calculo tc WHERE tc.dia = ta.dia) as porcentaje_error,

        CASE WHEN (SELECT tvs.ns_nivel FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia)> 0 THEN
        true ELSE false END as nivel_error,

        (SELECT tvs.ns_nivel FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia) as nivel_numero,

        CASE WHEN (SELECT tvs.ns_caudal FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia)> 0 THEN
        true ELSE false END as caudal_error,

        (SELECT tvs.ns_caudal FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia) as caudal_numero,

        TRUE as estado,
        ta.existe_en_validacion as validado
        FROM tabla_acumulada ta

    )
    SELECT * FROM reporte;

END;
$BODY$;

-- ALTER FUNCTION public.reporte_validacion_diario_agua(integer, timestamp with time zone, timestamp with time zone, numeric, numeric)
--    OWNER TO usuario1;
