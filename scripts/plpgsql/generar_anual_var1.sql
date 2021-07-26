-- DROP FUNCTION public.generar_anual_var1();

CREATE OR REPLACE FUNCTION public.generar_anual_var1(
	)
    RETURNS boolean
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE

AS $BODY$
DECLARE _resultado boolean;
BEGIN

WITH
	variable AS (
		SELECT umbral_completo AS umbral FROM variable_variable v WHERE var_id = 1 LIMIT 1
	),
    dato AS (
        SELECT * FROM mensual_var1mensual d
        WHERE d.usado_para_anual = FALSE
        LIMIT 1
    ),
    anio_inicio AS (
        SELECT date_trunc('year', (SELECT d.fecha FROM dato d)) AS anio_inicio LIMIT 1
    ),
    anio_fin AS (
        SELECT (SELECT mi.anio_inicio FROM anio_inicio mi) + interval '12 month' - interval '1 second' AS anio_fin LIMIT 1
    ),
	bloque AS (
        SELECT * FROM mensual_var1mensual d
        WHERE d.estacion_id = (SELECT da.estacion_id FROM dato da)
            AND d.fecha >= (SELECT anio_inicio FROM anio_inicio)
		AND d.fecha < (SELECT anio_fin FROM anio_fin)
	),
    calculo AS (
        SELECT
			(select count(d.estacion_id) from dato d) as cuenta,
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT m.anio_inicio FROM anio_inicio m) AS fecha,
            (SELECT SUM(b.valor) FROM bloque b WHERE b.valor IS NOT NULL) AS valor,
            (SELECT SUM(b.completo_mediciones)::decimal/(SELECT count(fecha) FROM bloque) FROM bloque b
			 	WHERE b.completo_mediciones IS NOT NULL) AS completo_mediciones ,
            (SELECT COUNT(*)::decimal/(SELECT count(fecha) FROM bloque) * 100 FROM bloque b
			 	WHERE b.completo_umbral >= (SELECT umbral FROM variable) ) AS completo_umbral,
			(select EXTRACT(MONTH FROM b.fecha) from  bloque b
				WHERE (select count(*) from bloque) > 10 order by b.valor desc limit 1 ) as mes_lluvioso,
			(select EXTRACT(MONTH FROM b.fecha) from  bloque b
				WHERE (select count(*) from bloque) > 10 order by b.valor asc limit 1) as mes_seco,
			(select max(b.valor) from  bloque b WHERE (select count(*) from bloque) > 10) as mes_lluvioso_valor,
			(select min(valor) from  bloque b WHERE (select count(*) from bloque) > 10) as mes_seco_valor,
			(select * from dias_cons_igua_lluvia((SELECT d.estacion_id FROM dato d)::integer,
												 (SELECT m.anio_inicio FROM anio_inicio m)::date,
												 (SELECT m.anio_fin FROM anio_fin m)::date,0.0)) as dias_sin_rr,
			(select * from dias_cons_mayor_lluvia((SELECT d.estacion_id FROM dato d)::integer,
												  (SELECT m.anio_inicio FROM anio_inicio m)::date,
												  (SELECT m.anio_fin FROM anio_fin m)::date,0.1)) as dias_con_rr,
			(select * from estacionalidad((SELECT d.estacion_id FROM dato d)::integer,
												  (SELECT m.anio_inicio FROM anio_inicio m)::date,
												  (SELECT m.anio_fin FROM anio_fin m)::date)) as estacionalidad
		where (Select count(*) from bloque) > 0

    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_umbral >= 0)
        AS es_valido
        FROM calculo
    ),
	update_anual AS (
        UPDATE anual_var1anual SET
            valor = (SELECT c.valor FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
            completo_umbral = (SELECT c.completo_umbral FROM calculo c),
			dias_con_lluvia = (SELECT c.dias_con_rr FROM calculo c),
			dias_sin_lluvia = (SELECT c.dias_sin_rr FROM calculo c),
			mes_lluvioso = (SELECT c.mes_lluvioso FROM calculo c),
			mes_seco = (SELECT c.mes_seco FROM calculo c),
			mes_lluvioso_valor = (SELECT c.mes_lluvioso_valor FROM calculo c),
			mes_seco_valor = (SELECT c.mes_seco_valor FROM calculo c),
			estacionalidad = (SELECT c.estacionalidad FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)

        RETURNING *
    ),
    insert_anual AS (
        INSERT INTO anual_var1anual(estacion_id, fecha, valor, completo_mediciones, completo_umbral, dias_con_lluvia, dias_sin_lluvia,
										mes_lluvioso, mes_seco, mes_lluvioso_valor, mes_seco_valor,estacionalidad)
        (SELECT estacion_id, fecha, valor, completo_mediciones, completo_umbral, dias_con_rr, dias_sin_rr,
		mes_lluvioso,mes_seco, mes_lluvioso_valor, mes_seco_valor,estacionalidad FROM calculo
        WHERE NOT EXISTS (SELECT id FROM update_anual)
        AND (SELECT es_valido FROM es_valido))
        RETURNING *
    ),
	update_USADO_PARA_ANUAL AS (
        UPDATE mensual_var1mensual SET usado_para_anual = TRUE
        WHERE id = ANY(ARRAY(SELECT b.id FROM bloque b))
        AND (EXISTS (SELECT id FROM update_anual) OR EXISTS (SELECT 1 FROM insert_anual))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE
            WHEN EXISTS (SELECT id FROM update_USADO_PARA_ANUAL) THEN TRUE
            ELSE FALSE
            END) AS resultado
    )

	--SELECT b.completo_mediciones FROM bloque b WHERE b.completo_mediciones IS NOT NULL
	--select * from variable
    --lect * from dato, anio_inicio, anio_fin
    --select * from mes_inicio
	--select * from mes_fin
	--select * from bloque
	--select count(*) from bloque b
	--SELECT COUNT(*)::decimal/(SELECT count(fecha) FROM bloque) * 100 FROM bloque b WHERE b.completo_umbral >= (SELECT umbral FROM variable)
    --select * from calculo
	--SELECT es_valido FROM es_valido
	--SELECT id FROM update_anual
	--SELECT estacion_id, fecha, valor, completo_mediciones , completo_umbral, dias_con_rr, dias_sin_rr, mes_lluvioso, mes_seco, mes_lluvioso_valor, mes_seco_valor FROM calculo
    --select * from es_valido
    --select * from update_anual
    --select * from insert_anual
    --select * from update_USADO_PARA_ANUAL
    --select * from resultado

	SELECT r.resultado INTO _resultado FROM resultado r;
    RETURN _resultado;

END;
$BODY$;

