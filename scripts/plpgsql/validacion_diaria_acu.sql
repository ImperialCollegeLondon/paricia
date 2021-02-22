DROP FUNCTION  IF EXISTS  public.reporte_validacion_diario_precipitacion(integer, timestamp with time zone, timestamp with time zone, numeric, numeric);
--DROP FUNCTION public.reporte_validacion_diario_precipitacion(integer, timestamp with time zone, timestamp with time zone);
CREATE OR REPLACE FUNCTION public.reporte_validacion_diario_precipitacion(
	_estacion_id integer,
	_fecha_inicio timestamp with time zone,
	_fecha_fin timestamp with time zone,
	_var_maximo numeric,
	_var_minimo numeric)
    RETURNS TABLE(id bigint, fecha timestamp with time zone,fecha_error numeric, fecha_numero numeric,
        valor numeric,porcentaje numeric, porcentaje_error boolean,
        --valor_error boolean, maximo_error boolean, minimo_error boolean,
        valor_numero numeric, valor_error boolean, media_historica numeric, estado boolean, validado boolean,c_varia_err numeric)
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
        SELECT v.id, v.fecha, 0 AS tipo, v.valor, v.validacion, TRUE AS existe_en_validacion, FALSE as valor_vacio
        FROM validacion_var1validado v WHERE v.estacion_id = (SELECT est_id FROM estacion) AND v.fecha >= _fecha_inicio AND v.fecha <= _fecha_fin
    ),
    medicion AS (
        SELECT m.id, m.fecha, 1 AS tipo, m.valor, CAST(NULL AS smallint) AS validacion,
            EXISTS(SELECT * FROM validacion v WHERE v.fecha = m.fecha AND v.valor = m.valor) AS existe_en_validacion,
            EXISTS(SELECT * FROM validacion v WHERE v.fecha = m.fecha ) AS valor_vacio
        FROM medicion_var1medicion m WHERE m.estacion_id = (SELECT est_id FROM estacion) AND m.fecha >= _fecha_inicio AND m.fecha <= _fecha_fin
    ),
    --unir las tablas medicion y validacion en una tabla
    union_med_val AS (
        SELECT * FROM validacion UNION SELECT * FROM medicion
    ),
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
				 WHEN lapso_tiempo = 0 THEN 0
				 WHEN LEAD(lapso_tiempo) OVER (ORDER by lf.fecha) > periodo_esperado + 0.13 THEN 2
				ELSE 1
			END
		END AS fecha_valida
		FROM lapsos_fechas lf
	),
    --Seleccionar una serie unica de los validados y los crudos
    tabla_base AS (
        SELECT
            row_number() OVER (ORDER BY umv.fecha ASC, umv.tipo ASC, umv.id DESC) as numero_fila,
            *
        FROM union_med_val umv WHERE NOT (umv.existe_en_validacion = TRUE AND umv.tipo = 1 OR umv.valor_vacio = TRUE)
    ),
    tabla_seleccion AS (
		SELECT *,
			(SELECT fecha_grupo FROM fechas f WHERE f.fecha = tb.fecha) AS fecha_grupo,
			CASE WHEN tb.numero_fila = 1 THEN TRUE ELSE CASE
		WHEN lag(tb.fecha) OVER (ORDER BY tb.numero_fila ASC) != tb.fecha THEN TRUE
		ELSE FALSE END END AS seleccionado
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
        SELECT date_trunc('day',tb.fecha) as dia, COUNT(tb.valor) numero_datos, SUM(tb.valor) as valor,
        bool_and(tb.existe_en_validacion) as existe_en_validacion
        --(SELECT AVG(valor) FROM diario_precipitacion dp WHERE estacion_id = (SELECT est_id FROM estacion) AND
          ---  date_part('day',dp.fecha)= date_part('day', tb.fecha) AND date_part('month',dp.fecha)= date_part('month',tb.fecha)) as media_historica

        FROM tabla_base tb GROUP BY dia ORDER by dia
    ),
    -- Numero de datos esperados por d?a
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
        ROUND((tde.numero_datos::decimal/tde.numero_datos_esperado)*100,2) as porcentaje,
        CASE WHEN ROUND((tde.numero_datos::decimal/tde.numero_datos_esperado)*100,2) < (SELECT umbral_completo FROM variable)
        OR ROUND((tde.numero_datos::decimal/tde.numero_datos_esperado)*100,2) > 100
        THEN TRUE ELSE FALSE END AS porcentaje_error
        FROM tabla_datos_esperados tde
    ),
    tabla_valores_sos AS (
        SELECT ta.dia,
            (SELECT COUNT(tb.valor) nsvalor FROM tabla_base tb WHERE date(tb.fecha) = ta.dia
                AND (tb.valor>_var_maximo OR tb.valor < _var_minimo )
            )::numeric as numero_valor_sospechoso
        FROM tabla_acumulada ta ORDER BY ta.dia
    ),
    tabla_varia_err AS (
        SELECT ta.dia,
            (SELECT COUNT(tv.variacion_consecutiva) nsvalor FROM tabla_variacion tv WHERE date(tv.fecha) = ta.dia
                AND (tv.variacion_consecutiva <= -(select abs(var_err) from variable where var_id = 1) )
            )::numeric as varia_error
        FROM tabla_acumulada ta ORDER BY ta.dia
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
        ROUND(ta.valor,2)::numeric as valor,
        (SELECT tc.porcentaje FROM tabla_calculo tc WHERE tc.dia = ta.dia) as porcentaje,
        (SELECT tc.porcentaje_error FROM tabla_calculo tc WHERE tc.dia = ta.dia) as porcentaje_error,
        (SELECT tvs.numero_valor_sospechoso FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia) as valor_numero,
        CASE WHEN (SELECT tvs.numero_valor_sospechoso FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia)>0 THEN true ELSE false END AS valor_error,
        ROUND((SELECT AVG(dp.valor) FROM diario_var1diario dp WHERE dp.estacion_id = (SELECT est_id FROM estacion) AND
            date_part('day',dp.fecha)= date_part('day', ta.dia) AND date_part('month',dp.fecha)= date_part('month',ta.dia)),2) as media_historica,

        TRUE as estado,
        ta.existe_en_validacion as validado,
		(select tve.varia_error from tabla_varia_err tve where tve.dia = ta.dia) as c_varia_err
        --ta.valor > (SELECT var_maximo*288 FROM variable) OR ta.valor < (SELECT var_minimo*288 FROM variable) AS valor_error,
        --(SELECT tc.porcentaje FROM tabla_calculo tc WHERE tc.dia = ta.dia) < (SELECT umbral_completo FROM variable) as porcentaje_error
        FROM tabla_acumulada ta

    )
    SELECT * FROM reporte;


END;
$BODY$;

ALTER FUNCTION public.reporte_validacion_diario_precipitacion(integer, timestamp with time zone, timestamp with time zone, numeric, numeric)
    OWNER TO usuario1;