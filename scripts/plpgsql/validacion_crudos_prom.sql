DROP FUNCTION public.reporte_validacion_%%modelo%%(integer, timestamp with time zone, timestamp with time zone);

CREATE OR REPLACE FUNCTION public.reporte_validacion_%%modelo%%(
	_estacion_id integer,
	_fecha_inicio timestamp with time zone,
	_fecha_fin timestamp with time zone)
    RETURNS TABLE(id bigint, fecha timestamp with time zone,  valor numeric,maximo numeric, minimo numeric,
    existe_en_validacion boolean, estado boolean, fecha_error numeric, valor_error boolean,
    maximo_error boolean, minimo_error boolean, stddev_error boolean, comentario character varying)
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE
    ROWS 1000
AS $BODY$

BEGIN
	RETURN QUERY
	WITH
	estacion AS (SELECT * FROM estacion_estacion est WHERE est.est_id = _estacion_id),
	variable AS (SELECT * FROM variable_variable var WHERE var.var_id = %%var_id%%),
	--Seleccionar los datos de la tabla validados
    validacion AS (
        SELECT v.id, v.fecha, 0 AS tipo, v.valor, v.maximo, v.minimo, TRUE AS existe_en_validacion
        FROM validacion_%%modelo%% v WHERE v.estacion_id = (SELECT est_id FROM estacion) AND v.fecha >= _fecha_inicio AND v.fecha <= _fecha_fin
    ),
    --Seleccionar los datos de la tabla medicion
    medicion AS (
        SELECT m.id, m.fecha, 1 AS tipo, m.valor, m.maximo, m.minimo,
            EXISTS(SELECT * FROM validacion v WHERE v.fecha = m.fecha AND v.valor = m.valor) AS existe_en_validacion
        FROM medicion_%%modelo%% m WHERE m.estacion_id = (SELECT est_id FROM estacion) AND m.fecha >= _fecha_inicio AND m.fecha <= _fecha_fin
    ),
	union_med_val AS (
		SELECT * FROM validacion UNION SELECT * FROM medicion
	),
	fechas0 AS (
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
				 WHEN lapso_tiempo > periodo_esperado + 0.13 THEN 2
				ELSE 1
			END
		END AS fecha_valida
		FROM fechas0
	),
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
			CASE WHEN tb.numero_fila = 1 THEN TRUE ELSE CASE WHEN lag(tb.fecha) OVER (ORDER BY tb.numero_fila ASC) != tb.fecha THEN TRUE ELSE FALSE END END AS estado
			--(SELECT med.id FROM medicion med WHERE med.fecha = tb.fecha ORDER BY id ASC LIMIT 1) AS medicion_id
		FROM tabla_base tb
	),
	estadistica AS (
		SELECT e1.media AS media, e1.desv_est AS desv_est,
		e1.media - (e1.desv_est * (SELECT var_min FROM variable)) AS lim_inf_stddev,
		e1.media + (e1.desv_est * (SELECT var_min FROM variable)) AS lim_sup_stddev
		FROM (
			SELECT AVG(ts.valor) AS media, STDDEV_SAMP(ts.valor) AS desv_est
			FROM tabla_seleccion ts
			WHERE ts.valor IS NOT NULL AND ts.estado IS TRUE
		) e1
	),
	reporte AS (
		SELECT ts.numero_fila AS id, ts.fecha, ts.valor, ts.maximo, ts.minimo, ts.existe_en_validacion, ts.estado,
			(SELECT fecha_valida FROM fechas ff WHERE ff.fecha = ts.fecha)::numeric AS fecha_error,
			ts.valor > (SELECT var_maximo FROM variable) OR ts.valor < (SELECT var_minimo FROM variable) AS valor_error,
			ts.maximo > (SELECT var_maximo FROM variable) OR ts.maximo < (SELECT var_minimo FROM variable) AS maximo_error,
			ts.minimo > (SELECT var_maximo FROM variable) OR ts.minimo < (SELECT var_minimo FROM variable) AS minimo_error,
			ts.valor < (SELECT lim_inf_stddev FROM estadistica ) OR ts.valor > (SELECT lim_sup_stddev FROM estadistica)  AS stddev_error,
			CASE
				WHEN ts.existe_en_validacion THEN
					(SELECT vc.comentario FROM validacion_comentariovalidacion vc WHERE vc.estacion_id = (SELECT est_id FROM estacion) AND vc.variable_id = (SELECT var_id FROM variable) AND vc.validado_id = ts.id)
				ELSE NULL
			END AS comentario
		FROM tabla_seleccion ts
	)

	SELECT * FROM reporte;


END;
$BODY$;

ALTER FUNCTION public.reporte_validacion_%%modelo%%(integer, timestamp with time zone, timestamp with time zone)
    OWNER TO postgres;

