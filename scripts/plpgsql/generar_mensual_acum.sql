DROP FUNCTION IF EXISTS generar_mensual_precipitacion();
CREATE OR REPLACE FUNCTION generar_mensual_precipitacion()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN

    WITH
	variable AS (
		SELECT umbral_completo AS umbral FROM variable_variable v WHERE var_id = 1 LIMIT 1
	),
    dato AS (
        SELECT * FROM diario_precipitacion d
        WHERE d.usado_para_mensual = FALSE
        LIMIT 1
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
        SELECT * FROM diario_precipitacion d
        WHERE d.estacion_id = (SELECT da.estacion_id FROM dato da)
            AND d.fecha >= (SELECT mes_inicio FROM mes_inicio) AND d.fecha < (SELECT mes_fin FROM mes_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT m.mes_inicio FROM mes_inicio m) AS fecha,
            (SELECT SUM(b.valor) FROM bloque b WHERE b.valor IS NOT NULL) AS valor,
            (SELECT SUM(b.completo_mediciones)::decimal/(SELECT dias FROM dias_en_mes) FROM bloque b
			 	WHERE b.completo_mediciones IS NOT NULL) AS completo_mediciones,
            (SELECT COUNT(*)::decimal/(SELECT dias FROM dias_en_mes) * 100 FROM bloque b
			 	WHERE b.completo_umbral >= (SELECT umbral FROM variable) ) AS completo_umbral
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_umbral >= 0)
        AS es_valido
        FROM calculo
    ),
    update_mensual AS (
        UPDATE mensual_precipitacion SET
			valor = (SELECT c.valor FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_mensual AS (
        INSERT INTO mensual_precipitacion(estacion_id, fecha, valor, completo_mediciones, completo_umbral)
        SELECT estacion_id, fecha, valor, completo_mediciones, completo_umbral FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_mensual)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_MENSUAL AS (
        UPDATE diario_precipitacion SET usado_para_mensual = TRUE
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