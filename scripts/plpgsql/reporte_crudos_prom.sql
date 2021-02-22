DROP FUNCTION IF EXISTS  public.reporte_crudos_%%modelo%%(integer, timestamp with time zone, timestamp with time zone, numeric, numeric);


CREATE OR REPLACE FUNCTION public.reporte_crudos_%%modelo%%(
	_estacion_id integer,
	_fecha_inicio timestamp with time zone,
	_fecha_fin timestamp with time zone,
	_var_maximo numeric,
	_var_minimo numeric)
    RETURNS TABLE( id bigint, fecha timestamp with time zone, valor numeric, maximo numeric, minimo numeric,
     estado boolean, seleccionado boolean,
     comentario character varying)
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
        SELECT v.id, v.fecha, v.valor
        FROM validacion_%%variable%%validado v WHERE v.estacion_id = (SELECT est_id FROM estacion)
        AND  date_trunc('day',v.fecha) >= _fecha_inicio AND  date_trunc('day',v.fecha) <= _fecha_fin
    ),
    --Seleccionar los datos de la tabla medicion
    medicion AS (
        SELECT m.id, m.fecha, m.valor, m.maximo, m.minimo,
            EXISTS(SELECT * FROM validacion v WHERE v.fecha = m.fecha) AS existe_en_validacion
        FROM medicion_%%variable%%medicion m WHERE m.estacion_id = (SELECT est_id FROM estacion)
        AND  date_trunc('day',m.fecha) >= _fecha_inicio AND  date_trunc('day',m.fecha) <= _fecha_fin
    ),
	tabla_base AS (
		SELECT
			m.fecha, m.valor, m.maximo, m.minimo
		FROM medicion m WHERE m.existe_en_validacion = FALSE
		GROUP BY m.fecha, m.valor, m.maximo, m.minimo
		HAVING COUNT(*)=1
	),
	reporte AS (
		SELECT row_number() OVER (ORDER BY ts.fecha ASC) as id,ts.fecha,
			CASE WHEN ts.valor> _var_maximo OR ts.valor < _var_minimo THEN NULL ELSE ts.valor END AS valor,
			CASE WHEN ts.maximo> _var_maximo OR ts.maximo < _var_minimo THEN NULL ELSE ts.maximo END AS maximo,
			CASE WHEN ts.minimo> _var_maximo OR ts.minimo < _var_minimo THEN NULL ELSE ts.minimo END AS minimo,
		    CASE WHEN ts.valor is NULL THEN FALSE ELSE TRUE END as estado,
		    TRUE as seleccionado, NULL::character varying as comentario
		FROM tabla_base ts
	)

	SELECT * FROM reporte order by fecha;


END;
$BODY$;

ALTER FUNCTION public.reporte_validacion_%%modelo%%(integer, timestamp with time zone, timestamp with time zone, numeric, numeric)
    OWNER TO usuario1;
