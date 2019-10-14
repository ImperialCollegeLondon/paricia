-- FUNCTION: public.reporte_validacion_var1(integer, timestamp with time zone, timestamp with time zone)

-- DROP FUNCTION public.reporte_validacion_var1(integer, timestamp with time zone, timestamp with time zone);

CREATE OR REPLACE FUNCTION public.reporte_validacion_precipitacion(
	_estacion_id integer,
	_fecha_inicio timestamp with time zone,
	_fecha_fin timestamp with time zone)
    RETURNS TABLE(numero_fila bigint, seleccionado boolean, fecha timestamp with time zone, valor_seleccionado numeric, valor numeric, variacion_consecutiva numeric, comentario character varying, class_fila text, class_fecha text, class_validacion text, class_valor text, class_variacion_consecutiva text, class_stddev_error text)
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE
    ROWS 1000
AS $BODY$

BEGIN
	RETURN QUERY
	WITH
	estacion AS (SELECT * FROM estacion_estacion est WHERE est.est_id = _estacion_id),
	variable AS (SELECT * FROM variable_variable var WHERE var.var_id = 1),
	validacion AS (
		SELECT v.id, v.fecha, 0 AS tipo, v.valor, v.validacion, TRUE AS existe_en_validacion
		FROM validacion_precipitacion v WHERE v.estacion_id = (SELECT est_id FROM estacion) AND v.fecha >= _fecha_inicio AND v.fecha <= _fecha_fin
	),
	medicion AS (
		SELECT m.id, m.fecha, 1 AS tipo, m.valor, CAST(NULL AS smallint) AS validacion,
			EXISTS(SELECT * FROM validacion v WHERE v.fecha = m.fecha AND v.valor = m.valor) AS existe_en_validacion
		FROM medicion_precipitacion m WHERE m.estacion = (SELECT est_id FROM estacion) AND m.fecha >= _fecha_inicio AND m.fecha <= _fecha_fin
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
			CASE WHEN lapso_tiempo < periodo_esperado - 0.04 THEN 0
				 WHEN lapso_tiempo > periodo_esperado + 0.04 THEN 2
				ELSE 1
			END
		END AS fecha_valida
		FROM fechas0
	),
	tabla_base AS (
		SELECT
			row_number() OVER (ORDER BY umv.fecha ASC, umv.tipo ASC, umv.validacion DESC, umv.id DESC) as numero_fila,
			*
		FROM union_med_val umv WHERE NOT (umv.existe_en_validacion = TRUE AND umv.tipo = 1)
	),
	tabla1 AS (
		SELECT *,
			(SELECT fecha_grupo FROM fechas f WHERE f.fecha = tb.fecha) AS fecha_grupo,
			CASE WHEN tb.numero_fila = 1 THEN TRUE ELSE CASE WHEN lag(tb.fecha) OVER (ORDER BY tb.numero_fila ASC) != tb.fecha THEN TRUE ELSE FALSE END END AS seleccionado,
			(SELECT med.id FROM medicion med WHERE med.fecha = tb.fecha ORDER BY id ASC LIMIT 1) AS medicion_id
		FROM tabla_base tb
	),
	tabla2 AS (
		SELECT *,
			(SELECT t1.valor - (SELECT tanterior.valor FROM tabla1 tanterior WHERE tanterior.fecha_grupo = t1.fecha_grupo - 1 AND tanterior.seleccionado IS TRUE) ) AS variacion_consecutiva,
			CASE WHEN t1.seleccionado THEN t1.valor ELSE NULL END AS valor_seleccionado
		FROM tabla1 t1
	),
	estadistica AS (
		SELECT e1.media AS media, e1.desv_est AS desv_est,
		e1.media - (e1.desv_est * (SELECT var_min FROM variable)) AS lim_inf_stddev,
		e1.media + (e1.desv_est * (SELECT var_min FROM variable)) AS lim_sup_stddev
		FROM (
			SELECT AVG(t2.valor) AS media, STDDEV_SAMP(t2.valor) AS desv_est
			FROM tabla2 t2
			WHERE t2.valor IS NOT NULL AND t2.seleccionado IS TRUE
		) e1
	),
	reporte AS (
		SELECT *,
			(SELECT fecha_valida FROM fechas ff WHERE ff.fecha = t2.fecha) AS fecha_error,
			t2.valor > (SELECT var_maximo FROM variable) OR t2.valor < (SELECT var_minimo FROM variable) AS valor_error,
			CASE
				WHEN ABS(t2.variacion_consecutiva) <= (SELECT var_sos FROM variable) THEN 0
				WHEN (ABS(t2.variacion_consecutiva) > (SELECT var_sos FROM variable) AND ABS(t2.variacion_consecutiva) <= (SELECT var_err FROM variable)) THEN 1
				WHEN ABS(t2.variacion_consecutiva) > (SELECT var_sos FROM variable) THEN 2
				ELSE 0
			END AS variacion_nivel,
			t2.valor < (SELECT lim_inf_stddev FROM estadistica ) OR t2.valor > (SELECT lim_sup_stddev FROM estadistica)  AS stddev_error,
			CASE
				WHEN existe_en_validacion THEN
					(SELECT vc.comentario FROM validacion_comentariovalidacion vc WHERE vc.estacion_id = (SELECT est_id FROM estacion) AND vc.variable_id = (SELECT var_id FROM variable) AND vc.validado_id = t2.id)
				ELSE NULL
			END AS comentario
		FROM tabla2 t2
	),
	-- Reporte_con_clases_para_html pudiera ser removido para reducir consumo de memoria RAM
	reporte_con_clases_para_html AS (
		SELECT *,
			CASE
			    WHEN r.seleccionado THEN CAST(fecha_grupo AS text) || ' seleccionado'
			    ELSE CAST(fecha_grupo AS text)  || ' no-seleccionado' END  AS class_fila,
			CASE WHEN fecha_error = 0 THEN 'fecha error' WHEN fecha_error = 1 THEN 'fecha normal' ELSE 'fecha salto' END AS class_fecha,
			CASE WHEN existe_en_validacion THEN 'validacion validado' ELSE 'validacion no-validado' END AS class_validacion,
			CASE WHEN valor_error THEN 'valor error' ELSE 'valor normal' END AS class_valor,
			CASE variacion_nivel WHEN 0 THEN  'var_con normal' WHEN 1 THEN 'var_con sospechoso' WHEN 2 THEN 'var_con error' END AS class_variacion_consecutiva,
			CASE WHEN stddev_error THEN 'stddev error' ELSE 'stddev normal' END AS class_stddev_error
		FROM reporte r
	)
	SELECT rf.numero_fila, rf.seleccionado, rf.fecha, rf.valor_seleccionado, rf.valor, rf.variacion_consecutiva, rf.comentario, rf.class_fila, rf.class_fecha, rf.class_validacion,
		rf.class_valor, rf.class_variacion_consecutiva, rf.class_stddev_error FROM reporte_con_clases_para_html rf;
END; $BODY$;

ALTER FUNCTION public.reporte_validacion_precipitacion(integer, timestamp with time zone, timestamp with time zone)
    OWNER TO postgres;