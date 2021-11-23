-- FUNCTION: public.reporte_validacion_viento(integer, timestamp with time zone, timestamp with time zone, numeric, numeric)

-- DROP FUNCTION public.reporte_validacion_viento(integer, timestamp with time zone, timestamp with time zone, numeric, numeric);

CREATE OR REPLACE FUNCTION public.reporte_validacion_viento(
	_estacion_id integer,
	_fecha_inicio timestamp with time zone,
	_fecha_fin timestamp with time zone,
	_var_maximo numeric,
	_var_minimo numeric)
    RETURNS TABLE(id bigint, fecha timestamp with time zone, valor numeric, maximo numeric, minimo numeric, direccion numeric, categoria numeric, validado boolean, seleccionado boolean, estado boolean, fecha_error numeric, valor_error boolean, maximo_error boolean, minimo_error boolean, stddev_error boolean, comentario character varying, variacion_consecutiva numeric) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
    
AS $BODY$

BEGIN
	RETURN QUERY
	WITH
	estacion AS (SELECT * FROM estacion_estacion est WHERE est.est_id = _estacion_id),
	variable AS (SELECT * FROM variable_variable var WHERE var.var_id = 4),
	--Seleccionar los datos de la tabla validados
    --validacion AS (
    --    SELECT v_vvi.id, v_vvi.fecha, 0 AS tipo, v_vvi.valor, v_vvi.maximo, v_vvi.minimo, v_dvi.valor as direccion,
    --    TRUE AS existe_en_validacion, FALSE as valor_vacio
    --    FROM validacion_velocidadviento v_vvi, medicion_direccionviento v_dvi WHERE v_vvi.estacion_id = (SELECT est_id FROM estacion)
    --    AND v_vvi.fecha >= _fecha_inicio AND v_vvi.fecha <= _fecha_fin AND v_vvi.fecha = v_dvi.fecha AND v_dvi.estacion_id = v_vvi.estacion_id
    --),
    validacion AS (
        SELECT v_vvi.id, date_trunc('minute',v_vvi.fecha) as fecha, 0 AS tipo, v_vvi.valor, v_vvi.maximo, v_vvi.minimo, v_vvi.direccion as direccion,
        TRUE AS existe_en_validacion, FALSE as valor_vacio
        FROM validacion_viento v_vvi WHERE v_vvi.estacion_id = (SELECT est_id FROM estacion)
        AND v_vvi.fecha >= _fecha_inicio AND v_vvi.fecha <= _fecha_fin
    ),
    --Seleccionar los datos de la tabla medicion
    medicion AS (
        SELECT m_vvi.id, date_trunc('minute',m_vvi.fecha) as fecha, 1 AS tipo, CASE WHEN m_vvi.valor = 'NaN' THEN NULL ELSE m_vvi.valor END AS valor ,
        CASE WHEN m_vvi.maximo = 'NaN' THEN NULL ELSE m_vvi.maximo END AS maximo , CASE WHEN m_vvi.minimo = 'NaN' THEN NULL ELSE m_vvi.minimo END AS minimo ,
        CASE WHEN m_dvi.valor = 'NaN' THEN NULL ELSE m_dvi.valor END AS direccion ,
        EXISTS(SELECT * FROM validacion v_vvi WHERE v_vvi.fecha = date_trunc('minute',m_vvi.fecha) AND v_vvi.valor = m_vvi.valor) AS existe_en_validacion,
        EXISTS(SELECT * FROM validacion v_vvi WHERE v_vvi.fecha = date_trunc('minute',m_vvi.fecha)) AS valor_vacio
        FROM medicion_var4medicion m_vvi, medicion_var5medicion m_dvi WHERE m_vvi.estacion_id = (SELECT est_id FROM estacion)
        AND m_vvi.fecha >= _fecha_inicio AND m_vvi.fecha <= _fecha_fin AND m_vvi.fecha = m_dvi.fecha AND m_dvi.estacion_id = m_vvi.estacion_id
        --AND NOT (m_vvi.valor IS NULL OR m_vvi.valor = 'NaN'::numeric) AND NOT (m_dvi.valor IS NULL OR m_vvi.valor = 'NAN'::numeric)
        --AND NOT (m_dvi.valor IS NULL OR m_dvi.valor = 'NaN'::numeric)
    ),
	--unir las tablas medicion y validacion
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
	tabla_base AS (
		SELECT
			row_number() OVER (ORDER BY umv.fecha ASC, umv.tipo ASC,umv.id DESC) as numero_fila,
			*,

        CASE WHEN umv.direccion IS NULL OR umv.direccion = 'NaN'::numeric THEN NULL ELSE
            CASE WHEN umv.direccion<= 22.5 OR umv.direccion> 337.5 THEN 1 ELSE
                CASE WHEN umv.direccion> 22.5 AND umv.direccion<= 67.5 THEN 2 ELSE
                    CASE WHEN umv.direccion> 67.5 AND umv.direccion<= 112.5 THEN 3 ELSE
                        CASE WHEN umv.direccion> 112.5 AND umv.direccion<= 157.5 THEN 4 ELSE
                            CASE WHEN umv.direccion> 157.5 AND umv.direccion<= 202.5 THEN 5 ELSE
                                CASE WHEN umv.direccion> 202.5 AND umv.direccion<= 247.5 THEN 6 ELSE
                                    CASE WHEN umv.direccion> 247.5 AND umv.direccion<= 292.5 THEN 7 ELSE
                                        CASE WHEN umv.direccion> 292.5 AND umv.direccion<= 337.5 THEN 8 ELSE NULL END
                                    END
                                END
                            END
                        END
                    END
                END
            END
        END AS categoria

		FROM union_med_val umv WHERE NOT (umv.existe_en_validacion = TRUE AND umv.tipo = 1 OR umv.valor_vacio = TRUE)
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
			SELECT AVG(ts.valor) AS media, STDDEV_SAMP(ts.valor) AS desv_est
			FROM tabla_seleccion ts
			WHERE ts.valor IS NOT NULL AND ts.seleccionado IS TRUE
		) e1
	),
	reporte AS (
		SELECT ts.numero_fila AS id, ts.fecha, ts.valor, ts.maximo, ts.minimo,
		    ts.direccion, ts.categoria::numeric,
			ts.existe_en_validacion, ts.seleccionado,
		    CASE WHEN ts.valor is NULL AND ts.maximo is NULL and ts.maximo is NULL THEN FALSE ELSE TRUE END as estado,
			(SELECT fecha_valida FROM fechas ff WHERE ff.fecha = ts.fecha)::numeric AS fecha_error,
			ts.valor > _var_maximo OR ts.valor < _var_minimo AS valor_error,
			ts.maximo > _var_maximo OR ts.maximo < _var_minimo AS maximo_error,
			ts.minimo > _var_maximo OR ts.minimo < _var_minimo AS minimo_error,

			ts.valor < (SELECT lim_inf_stddev FROM estadistica ) OR ts.valor > (SELECT lim_sup_stddev FROM estadistica)  AS stddev_error,
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

-- ALTER FUNCTION public.reporte_validacion_viento(integer, timestamp with time zone, timestamp with time zone, numeric, numeric)
--    OWNER TO usuario1;
