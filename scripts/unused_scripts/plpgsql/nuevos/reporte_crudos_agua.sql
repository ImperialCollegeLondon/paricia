-- FUNCTION: public.reporte_crudos_agua(integer, timestamp with time zone, timestamp with time zone, numeric, numeric)

-- DROP FUNCTION public.reporte_crudos_agua(integer, timestamp with time zone, timestamp with time zone, numeric, numeric);

CREATE OR REPLACE FUNCTION public.reporte_crudos_agua(
	_estacion_id integer,
	_fecha_inicio timestamp with time zone,
	_fecha_fin timestamp with time zone,
	_var_maximo numeric,
	_var_minimo numeric)
    RETURNS TABLE(id bigint, fecha timestamp with time zone, nivel numeric, caudal numeric, estado boolean, seleccionado boolean, comentario character varying) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
    
AS $BODY$

BEGIN
	RETURN QUERY
	
    WITH
	estacion AS (SELECT * FROM estacion_estacion est WHERE est.est_id = _estacion_id),
	variable_nivel AS (SELECT * FROM variable_variable var WHERE var.var_id = 11),
	variable_caudal AS (SELECT * FROM variable_variable var WHERE var.var_id = 10),
	--Seleccionar los datos de la tabla validados
    validacion AS (
        SELECT v.fecha, v.nivel
        FROM validacion_agua v WHERE v.estacion_id = (SELECT est_id FROM estacion)
        AND  date_trunc('day',v.fecha) >= _fecha_inicio AND  date_trunc('day',v.fecha) <= _fecha_fin
    ),
    --Seleccionar los datos de la tabla medicion
    medicion AS (

    	SELECT m_nag.fecha, CASE WHEN m_nag.valor = 'NaN' THEN NULL ELSE m_nag.valor END AS nivel_valor, 
        CASE WHEN m_cau.valor = 'NaN' THEN NULL ELSE m_cau.valor END AS caudal_valor,
            EXISTS(SELECT * FROM validacion v WHERE v.fecha = m_nag.fecha) AS existe_en_validacion
        FROM medicion_var11medicion m_nag, medicion_var10medicion m_cau WHERE m_nag.estacion_id = (SELECT est_id FROM estacion)
        AND m_nag.estacion_id = m_cau.estacion_id AND m_nag.fecha = m_cau.fecha
        AND  date_trunc('day',m_nag.fecha) >= _fecha_inicio AND  date_trunc('day',m_nag.fecha) <= _fecha_fin
    ),
	tabla_base AS (
		SELECT
			m.fecha, m.nivel_valor, m.caudal_valor
		FROM medicion m WHERE m.existe_en_validacion = FALSE
		GROUP BY m.fecha, m.nivel_valor, m.caudal_valor
		HAVING COUNT(*)=1
	),
	reporte AS (
		SELECT row_number() OVER (ORDER BY ts.fecha ASC) as id, ts.fecha,
			CASE WHEN ts.nivel_valor> _var_maximo OR ts.nivel_valor < _var_minimo THEN NULL ELSE ts.nivel_valor END AS nivel_valor,
			CASE WHEN ts.caudal_valor> (SELECT var_maximo FROM variable_caudal) OR ts.caudal_valor < (SELECT var_minimo FROM variable_caudal) THEN NULL ELSE ts.caudal_valor END AS caudal_valor,
		    CASE WHEN ts.nivel_valor is NULL THEN FALSE ELSE TRUE END as estado,
		    TRUE as seleccionado, NULL::character varying as comentario		
		FROM tabla_base ts
	)

	SELECT * FROM reporte order by fecha;

END;
$BODY$;

-- ALTER FUNCTION public.reporte_crudos_agua(integer, timestamp with time zone, timestamp with time zone, numeric, numeric)
--    OWNER TO usuario1;
