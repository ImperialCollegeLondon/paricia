DROP FUNCTION IF EXISTS  public.reporte_validacion_agua(integer, timestamp with time zone, timestamp with time zone, numeric, numeric);
CREATE OR REPLACE FUNCTION public.reporte_validacion_agua(
	_estacion_id integer,
	_fecha_inicio timestamp with time zone,
	_fecha_fin timestamp with time zone,
	_var_maximo numeric,
	_var_minimo numeric)
    RETURNS TABLE(id bigint, fecha timestamp with time zone,
    nivel numeric,
    caudal numeric,
    validado boolean, seleccionado boolean, estado boolean, fecha_error numeric,
    nivel_error boolean,
    caudal_error boolean,
    stddev_error boolean, comentario character varying, variacion_consecutiva numeric)
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE
    ROWS 1000
AS $BODY$

BEGIN
	RETURN QUERY
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
    --revision de lapsos de tiempo entre fechas
    lapsos_fechas AS (
        SELECT
            ff.fecha,
            row_number() OVER (ORDER BY ff.fecha ASC) as fecha_grupo,
            EXTRACT(EPOCH FROM ff.fecha - lag(ff.fecha) OVER (ORDER BY ff.fecha ASC))/60  as lapso_tiempo,
            (SELECT fre.fre_valor FROM frecuencia_frecuencia fre
                    WHERE fre.var_id_id = (SELECT var_id FROM variable) AND fre.est_id_id = (SELECT est_id FROM estacion) AND fre.fre_fecha_ini < ff.fecha
                    ORDER BY fre.fre_fecha_ini DESC LIMIT 1) AS periodo_esperado
        FROM (SELECT DISTINCT(umv.fecha) FROM union_med_val umv) ff ORDER BY fecha ASC
    ),
    fechas AS (
        SELECT *,
            CASE WHEN fecha_grupo = 1 THEN 1 ELSE
            CASE WHEN lapso_tiempo < periodo_esperado - 0.13 THEN 0
                 WHEN lapso_tiempo > periodo_esperado + 0.13 THEN 3
                 WHEN LEAD(lapso_tiempo) OVER (ORDER by lf.fecha) > periodo_esperado + 0.13 THEN 2
                ELSE 1
            END
        END AS fecha_valida
        FROM lapsos_fechas lf
    ),
    --Seleccionar una serie unica de los validados y los crudos
    tabla_base AS (
        SELECT
            row_number() OVER (ORDER BY umv.fecha ASC, umv.tipo ASC, --umv.validacion DESC--
            umv.id DESC) as numero_fila,
            *

        FROM union_med_val umv WHERE NOT (umv.existe_en_validacion = TRUE AND umv.tipo = 1)
    ),
    -- Excluir los datos duplicados
    tabla_seleccion AS (
        SELECT *,
            (SELECT fecha_grupo FROM fechas f WHERE f.fecha = tb.fecha) AS fecha_grupo,
            CASE WHEN tb.numero_fila = 1 THEN TRUE ELSE CASE WHEN lag(tb.fecha) OVER (ORDER BY tb.numero_fila ASC) != tb.fecha THEN TRUE ELSE FALSE END END AS seleccionado
            --(SELECT med.id FROM medicion med WHERE med.fecha = tb.fecha ORDER BY id ASC LIMIT 1) AS medicion_id
        FROM tabla_base tb --WHERE tb.valor IS NOT NULL
    ),
    tabla_variacion AS (
		SELECT *,
			(SELECT t1.valor - (SELECT tanterior.valor FROM tabla_seleccion tanterior
								WHERE tanterior.fecha_grupo = t1.fecha_grupo - 1
								AND tanterior.seleccionado IS TRUE) ) AS variacion_consecutiva,
			CASE WHEN t1.seleccionado THEN t1.valor ELSE NULL END AS valor_seleccionado
		FROM tabla_seleccion t1
	),
    estadistica AS (
        SELECT e1.media AS media, e1.desv_est AS desv_est,
        e1.media - (e1.desv_est * (SELECT var_min FROM variable)) AS lim_inf_stddev,
        e1.media + (e1.desv_est * (SELECT var_min FROM variable)) AS lim_sup_stddev
        FROM (
            SELECT AVG(ts.nivel) AS media, STDDEV_SAMP(ts.nivel) AS desv_est
            FROM tabla_seleccion ts
            WHERE ts.nivel IS NOT NULL AND ts.seleccionado IS TRUE
        ) e1
    ),
    reporte AS (
        SELECT ts.numero_fila AS id, ts.fecha, ts.nivel, ts.caudal,
            ts.existe_en_validacion, ts.seleccionado,
            CASE WHEN ts.nivel is NULL AND ts.caudal is NULL THEN FALSE ELSE TRUE END as estado,
            (SELECT fecha_valida FROM fechas ff WHERE ff.fecha = ts.fecha)::numeric AS fecha_error,
            ts.nivel > _var_maximo OR ts.nivel < _var_minimo AS nivel_error,
            ts.caudal > (SELECT var_maximo FROM caudal) OR ts.nivel < (SELECT var_minimo FROM caudal) AS caudal_error,
            ts.nivel < (SELECT lim_inf_stddev FROM estadistica ) OR
            ts.nivel > (SELECT lim_sup_stddev FROM estadistica)  AS stddev_error,
            CASE
                WHEN ts.existe_en_validacion THEN
                    (SELECT vc.comentario FROM validacion_comentariovalidacion vc WHERE vc.estacion_id = (SELECT est_id FROM estacion) AND vc.variable_id = (SELECT var_id FROM variable) AND vc.validado_id = ts.id)
                ELSE NULL
            END AS comentario,
			ts.variacion_consecutiva as variacion_consecutiva
		FROM tabla_variacion ts
    )
    SELECT * FROM reporte;

END;
$BODY$;

ALTER FUNCTION public.reporte_validacion_agua(integer, timestamp with time zone, timestamp with time zone, numeric, numeric)
    OWNER TO usuario1;
