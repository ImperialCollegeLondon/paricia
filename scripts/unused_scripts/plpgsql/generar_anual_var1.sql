-- DROP FUNCTION public.generar_anual_var1();

CREATE OR REPLACE FUNCTION public.generar_anual_var1()
    RETURNS boolean
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE

AS $BODY$
DECLARE _resultado boolean;
BEGIN

    WITH
	dato AS (
        SELECT * FROM mensual_var1mensual d WHERE d.usado_para_anual = FALSE LIMIT 1
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
		    (SELECT 100.0 - (SUM(100-b.vacios)::decimal/12.0) FROM bloque b WHERE b.vacios IS NOT NULL) AS vacios,
			(select EXTRACT(MONTH FROM b.fecha) from  bloque b order by b.valor desc limit 1 ) as mes_lluvioso,
			(select EXTRACT(MONTH FROM b.fecha) from  bloque b order by b.valor asc limit 1) as mes_seco,
			(select max(b.valor) from  bloque b) as mes_lluvioso_valor,
			(select min(b.valor) from  bloque b) as mes_seco_valor,
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
            (fecha IS NOT NULL) AND (vacios >= 0.0) AND (vacios <= 100.0)
        AS es_valido
        FROM calculo
    ),
	update_anual AS (
        UPDATE anual_var1anual SET
            valor = (SELECT c.valor FROM calculo c),
            vacios = (SELECT c.vacios FROM calculo c),
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
        INSERT INTO anual_var1anual(estacion_id, fecha, valor, vacios, dias_con_lluvia, dias_sin_lluvia,
										mes_lluvioso, mes_seco, mes_lluvioso_valor, mes_seco_valor,estacionalidad)
        (SELECT estacion_id, fecha, valor, vacios, dias_con_rr, dias_sin_rr,
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
	SELECT r.resultado INTO _resultado FROM resultado r;
    RETURN _resultado;

END;
$BODY$;

