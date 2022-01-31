DROP FUNCTION IF EXISTS reporte_validacion_var%%var_id%%(integer,timestamp with time zone,timestamp with time zone);
CREATE OR REPLACE FUNCTION reporte_validacion_var%%var_id%%(_estacion_id INT, _fecha_inicio TIMESTAMP WITH TIME ZONE, _fecha_fin TIMESTAMP WITH TIME ZONE)
RETURNS TABLE (
	numero_fila BIGINT,
	seleccionado BIGINT,
	fecha TIMESTAMP WITH TIME ZONE,
	valor_seleccionado NUMERIC,
	valor NUMERIC,
	variacion_consecutiva NUMERIC,
	comentario VARCHAR,
	class_fila TEXT,
	class_fecha TEXT,
	class_validacion TEXT,
	class_valor TEXT,
	class_variacion_consecutiva TEXT,
	class_stddev_error TEXT
)
AS $$

BEGIN
	RETURN QUERY
	WITH
	estacion AS (SELECT * FROM estacion_estacion est WHERE est.est_id = _estacion_id),
	variable AS (SELECT * FROM variable_variable var WHERE var.var_id = %%var_id%%),
	medicion AS (
		SELECT
			ROW_NUMBER() OVER (ORDER BY date_trunc('minute', m.fecha) ASC, m.id DESC) as numero_fila,
			m.id,
			date_trunc('minute', m.fecha) AS fecha_trunc,
			m.fecha,
			m.valor,
			ROW_NUMBER() OVER (PARTITION BY date_trunc('minute', m.fecha) ORDER BY m.id DESC) AS seleccionado,
			DENSE_RANK() OVER (ORDER BY date_trunc('minute', m.fecha)) AS grupo_fecha
		FROM medicion_var%%var_id%%medicion m WHERE m.estacion_id = (SELECT est_id FROM estacion)
		AND m.fecha >= _fecha_inicio AND m.fecha <= _fecha_fin
		ORDER BY 1
	),
	seleccionado AS (
		SELECT m.numero_fila, m.id, m.fecha_trunc, m.fecha, m.valor, m.seleccionado, m.grupo_fecha
		FROM medicion m
		WHERE m.seleccionado = 1 ORDER BY m.numero_fila
	),
	calculos1 AS (
		SELECT
			s.numero_fila, s.id, s.fecha_trunc, s.fecha, s.valor, s.seleccionado, s.grupo_fecha
			, EXTRACT(EPOCH FROM s.fecha_trunc - lag(s.fecha_trunc) OVER (ORDER BY s.fecha_trunc ASC))/60  as lapso_tiempo
			, (SELECT fre.fre_valor FROM frecuencia_frecuencia fre
					WHERE fre.var_id_id = (SELECT var_id FROM variable) AND fre.est_id_id = (SELECT est_id FROM estacion)
		   			AND fre.fre_fecha_ini < s.fecha_trunc
					ORDER BY fre.fre_fecha_ini DESC LIMIT 1) AS periodo_esperado
		FROM seleccionado s
		ORDER BY s.grupo_fecha
	),
	calculos2 AS (
		SELECT c.numero_fila, c.id, c.fecha_trunc, c.fecha, c.valor, c.seleccionado, c.grupo_fecha, c.lapso_tiempo,
		    c.periodo_esperado,
			CASE WHEN c.grupo_fecha = 1 THEN 1 ELSE
				CASE WHEN c.lapso_tiempo < c.periodo_esperado THEN 0 -- Tiempo menor al esperado
					 WHEN c.lapso_tiempo > c.periodo_esperado THEN 2 -- Tiempo mayor al esperado (SALTOS)
					ELSE 1 -- Tiempo esperado (OK)
				END
			END AS fecha_error,
			c.valor - lag(c.valor) OVER (ORDER BY c.fecha_trunc ASC) AS variacion_consecutiva
		FROM calculos1 c
	),
	estadistica1 AS (
		SELECT AVG(s.valor) AS media, STDDEV_SAMP(s.valor) AS desv_est
		FROM seleccionado s
		WHERE s.valor IS NOT NULL
	),
	estadistica2 AS (
		SELECT e1.media AS media, e1.desv_est AS desv_est,
		e1.media - (e1.desv_est * (SELECT var_min FROM variable)) AS lim_inf_stddev,
		e1.media + (e1.desv_est * (SELECT var_min FROM variable)) AS lim_sup_stddev
		FROM estadistica1 e1
	),
	reporte AS (
		SELECT *,
			t2.valor > (SELECT var_maximo FROM variable) OR t2.valor < (SELECT var_minimo FROM variable) AS valor_error,
			CASE
				WHEN ABS(t2.variacion_consecutiva) <= (SELECT var_sos FROM variable) THEN 0
				WHEN (ABS(t2.variacion_consecutiva) > (SELECT var_sos FROM variable)
				    AND ABS(t2.variacion_consecutiva) <= (SELECT var_err FROM variable)) THEN 1
				WHEN ABS(t2.variacion_consecutiva) > (SELECT var_sos FROM variable) THEN 2
				ELSE 0
			END AS variacion_nivel,
			t2.valor < (SELECT lim_inf_stddev FROM estadistica2 ) OR t2.valor > (SELECT lim_sup_stddev FROM estadistica2)
			    AS stddev_error,
			(SELECT vc.comentario FROM validacion_comentariovalidacion vc
				WHERE vc.estacion_id = (SELECT est_id FROM estacion)
					AND vc.variable_id = (SELECT var_id FROM variable) AND vc.validado_id = t2.id)
			 AS comentario
		FROM calculos2 t2
	),
	reporte_union AS ( -- Une los datos seleccionados con los NO SELECCIONADOS
		SELECT r.numero_fila, r.id, r.fecha_trunc, r.fecha, r.valor, r.seleccionado, r.grupo_fecha, r.lapso_tiempo,
		    r.periodo_esperado, r.fecha_error, r.variacion_consecutiva, r.valor_error, r.variacion_nivel,
		    r.stddev_error, r.comentario
			FROM reporte r
		UNION
		SELECT ns.numero_fila, ns.id, ns.fecha_trunc, ns.fecha, ns.valor, ns.seleccionado, ns.grupo_fecha, NULL, NULL,
		NULL, NULL, NULL, NULL, NULL, NULL
		FROM medicion ns WHERE ns.seleccionado > 1
	),
	-- Reporte_con_clases_para_html pudiera ser removido para reducir consumo de memoria RAM
	reporte_con_clases_para_html AS (
		SELECT *,
			CASE
			    WHEN r.seleccionado = 1 THEN CAST(grupo_fecha AS text) || ' seleccionado'
			    ELSE CAST(grupo_fecha AS text)  || ' no-seleccionado' END  AS class_fila,
			CASE WHEN fecha_error = 0 THEN 'fecha error' WHEN fecha_error = 1 THEN 'fecha normal' ELSE 'fecha salto' END
			    AS class_fecha,
			--CASE WHEN existe_en_validacion THEN 'validacion validado' ELSE 'validacion no-validado' END
			--    AS class_validacion,
			(SELECT 'validacion no-validado') AS class_validacion,
			CASE WHEN valor_error THEN 'valor error' ELSE 'valor normal' END AS class_valor,
			CASE variacion_nivel WHEN 0 THEN  'var_con normal' WHEN 1 THEN 'var_con sospechoso'
			    WHEN 2 THEN 'var_con error' END AS class_variacion_consecutiva,
			CASE WHEN stddev_error THEN 'stddev error' ELSE 'stddev normal' END AS class_stddev_error
		FROM reporte_union r
	)
	SELECT rf.numero_fila, rf.seleccionado, rf.fecha, rf.valor /*rf.valor_seleccionado*/ AS valor_seleccionado, rf.valor, rf.variacion_consecutiva,
	    rf.comentario, rf.class_fila, rf.class_fecha, rf.class_validacion, rf.class_valor,
	    rf.class_variacion_consecutiva, rf.class_stddev_error
		FROM reporte_con_clases_para_html rf
		ORDER BY rf.numero_fila;
END; $$
LANGUAGE 'plpgsql';
