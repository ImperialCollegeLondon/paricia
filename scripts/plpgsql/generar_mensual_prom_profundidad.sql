DROP FUNCTION IF EXISTS generar_mensual_var101();
CREATE OR REPLACE FUNCTION generar_mensual_var101()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN

    WITH
    dato AS (
        SELECT id, estacion_id, profundidad, fecha FROM diario_var101diario d
        WHERE d.usado_para_mensual = FALSE LIMIT 1
    ),
    mes_inicio AS (
        SELECT date_trunc('month', (SELECT d.fecha FROM dato d)) AS mes_inicio LIMIT 1
    ),
    mes_fin AS (
        SELECT (SELECT mi.mes_inicio FROM mes_inicio mi) + interval '1 month' AS mes_fin LIMIT 1
    ),
	dias_en_mes AS (
		SELECT extract(days FROM (SELECT mes_fin FROM mes_fin) + interval '- 1 day') AS dias
	),
	bloque AS (
        SELECT id, estacion_id, profundidad, fecha, valor, max_abs, min_abs, vacios
        FROM diario_var101diario d
        WHERE d.estacion_id = (SELECT da.estacion_id FROM dato da)
            AND d.profundidad = (SELECT da.profundidad FROM dato da)
            AND d.fecha >= (SELECT mes_inicio FROM mes_inicio) AND d.fecha < (SELECT mes_fin FROM mes_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT d.profundidad FROM dato d) AS profundidad,
            (SELECT m.mes_inicio FROM mes_inicio m) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
            (SELECT 100.0 - (SUM(100.0-b.vacios)::decimal/(SELECT dias FROM dias_en_mes)) FROM bloque b
			 	WHERE b.vacios IS NOT NULL) AS vacios
    ),
    es_valido AS (
        SELECT
            (fecha IS NOT NULL) AND (vacios >= 0.0) AND (vacios <= 100.0) AS es_valido
        FROM calculo
    ),
    update_mensual AS (
        UPDATE mensual_var101mensual SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            vacios = (SELECT c.vacios FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c)
            AND profundidad = (SELECT c.profundidad FROM calculo c)
            AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_mensual AS (
        INSERT INTO mensual_var101mensual(estacion_id, profundidad, fecha, valor, max_abs, min_abs,
            max_del_prom, min_del_prom, vacios)
        SELECT estacion_id, profundidad, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom,
            vacios FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_mensual)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_MENSUAL AS (
        UPDATE diario_var101diario SET usado_para_mensual = TRUE
        WHERE id = ANY(ARRAY(SELECT b.id FROM bloque b))
        AND (EXISTS (SELECT 1 FROM update_mensual) OR EXISTS (SELECT 1 FROM insert_mensual))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE WHEN EXISTS (SELECT id FROM update_USADO_PARA_MENSUAL) THEN TRUE
				ELSE FALSE  END) AS resultado
    )
	SELECT r.resultado INTO _resultado FROM resultado r;
    RETURN _resultado;

END
$BODY$  LANGUAGE plpgsql;