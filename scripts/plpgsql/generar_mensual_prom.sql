-- ---##############################################################
-- ---####  funcion para generar datos mensuales de temperaturaaire
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_mensual_temperaturaaire();
CREATE OR REPLACE FUNCTION generar_mensual_temperaturaaire()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN

    WITH
	variable AS (
		SELECT umbral_completo AS umbral FROM variable_variable v WHERE var_id = 2 LIMIT 1
	),
    dato AS (
        SELECT id, estacion_id, fecha
        FROM diario_temperaturaaire d
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
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, completo_umbral
        FROM diario_temperaturaaire d
        WHERE d.estacion_id = (SELECT da.estacion_id FROM dato da)
            AND d.fecha >= (SELECT mes_inicio FROM mes_inicio) AND d.fecha < (SELECT mes_fin FROM mes_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT m.mes_inicio FROM mes_inicio m) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
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
        UPDATE mensual_temperaturaaire SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_mensual AS (
        INSERT INTO mensual_temperaturaaire(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_mensual)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_MENSUAL AS (
        UPDATE diario_temperaturaaire SET usado_para_mensual = TRUE
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

-- ---##############################################################
-- ---####  funcion para generar datos mensuales de humedadaire
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_mensual_humedadaire();
CREATE OR REPLACE FUNCTION generar_mensual_humedadaire()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN

    WITH
	variable AS (
		SELECT umbral_completo AS umbral FROM variable_variable v WHERE var_id = 3 LIMIT 1
	),
    dato AS (
        SELECT id, estacion_id, fecha
        FROM diario_humedadaire d
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
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, completo_umbral
        FROM diario_humedadaire d
        WHERE d.estacion_id = (SELECT da.estacion_id FROM dato da)
            AND d.fecha >= (SELECT mes_inicio FROM mes_inicio) AND d.fecha < (SELECT mes_fin FROM mes_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT m.mes_inicio FROM mes_inicio m) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
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
        UPDATE mensual_humedadaire SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_mensual AS (
        INSERT INTO mensual_humedadaire(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_mensual)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_MENSUAL AS (
        UPDATE diario_humedadaire SET usado_para_mensual = TRUE
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

-- ---##############################################################
-- ---####  funcion para generar datos mensuales de velocidadviento
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_mensual_velocidadviento();
CREATE OR REPLACE FUNCTION generar_mensual_velocidadviento()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN

    WITH
	variable AS (
		SELECT umbral_completo AS umbral FROM variable_variable v WHERE var_id = 4 LIMIT 1
	),
    dato AS (
        SELECT id, estacion_id, fecha
        FROM diario_velocidadviento d
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
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, completo_umbral
        FROM diario_velocidadviento d
        WHERE d.estacion_id = (SELECT da.estacion_id FROM dato da)
            AND d.fecha >= (SELECT mes_inicio FROM mes_inicio) AND d.fecha < (SELECT mes_fin FROM mes_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT m.mes_inicio FROM mes_inicio m) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
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
        UPDATE mensual_velocidadviento SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_mensual AS (
        INSERT INTO mensual_velocidadviento(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_mensual)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_MENSUAL AS (
        UPDATE diario_velocidadviento SET usado_para_mensual = TRUE
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

-- ---##############################################################
-- ---####  funcion para generar datos mensuales de direccionviento
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_mensual_direccionviento();
CREATE OR REPLACE FUNCTION generar_mensual_direccionviento()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN

    WITH
	variable AS (
		SELECT umbral_completo AS umbral FROM variable_variable v WHERE var_id = 5 LIMIT 1
	),
    dato AS (
        SELECT id, estacion_id, fecha
        FROM diario_direccionviento d
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
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, completo_umbral
        FROM diario_direccionviento d
        WHERE d.estacion_id = (SELECT da.estacion_id FROM dato da)
            AND d.fecha >= (SELECT mes_inicio FROM mes_inicio) AND d.fecha < (SELECT mes_fin FROM mes_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT m.mes_inicio FROM mes_inicio m) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
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
        UPDATE mensual_direccionviento SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_mensual AS (
        INSERT INTO mensual_direccionviento(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_mensual)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_MENSUAL AS (
        UPDATE diario_direccionviento SET usado_para_mensual = TRUE
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

-- ---##############################################################
-- ---####  funcion para generar datos mensuales de humedadsuelo
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_mensual_humedadsuelo();
CREATE OR REPLACE FUNCTION generar_mensual_humedadsuelo()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN

    WITH
	variable AS (
		SELECT umbral_completo AS umbral FROM variable_variable v WHERE var_id = 6 LIMIT 1
	),
    dato AS (
        SELECT id, estacion_id, fecha
        FROM diario_humedadsuelo d
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
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, completo_umbral
        FROM diario_humedadsuelo d
        WHERE d.estacion_id = (SELECT da.estacion_id FROM dato da)
            AND d.fecha >= (SELECT mes_inicio FROM mes_inicio) AND d.fecha < (SELECT mes_fin FROM mes_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT m.mes_inicio FROM mes_inicio m) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
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
        UPDATE mensual_humedadsuelo SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_mensual AS (
        INSERT INTO mensual_humedadsuelo(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_mensual)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_MENSUAL AS (
        UPDATE diario_humedadsuelo SET usado_para_mensual = TRUE
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

-- ---##############################################################
-- ---####  funcion para generar datos mensuales de radiacionsolar
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_mensual_radiacionsolar();
CREATE OR REPLACE FUNCTION generar_mensual_radiacionsolar()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN

    WITH
	variable AS (
		SELECT umbral_completo AS umbral FROM variable_variable v WHERE var_id = 7 LIMIT 1
	),
    dato AS (
        SELECT id, estacion_id, fecha
        FROM diario_radiacionsolar d
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
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, completo_umbral
        FROM diario_radiacionsolar d
        WHERE d.estacion_id = (SELECT da.estacion_id FROM dato da)
            AND d.fecha >= (SELECT mes_inicio FROM mes_inicio) AND d.fecha < (SELECT mes_fin FROM mes_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT m.mes_inicio FROM mes_inicio m) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
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
        UPDATE mensual_radiacionsolar SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_mensual AS (
        INSERT INTO mensual_radiacionsolar(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_mensual)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_MENSUAL AS (
        UPDATE diario_radiacionsolar SET usado_para_mensual = TRUE
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

-- ---##############################################################
-- ---####  funcion para generar datos mensuales de presionatmosferica
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_mensual_presionatmosferica();
CREATE OR REPLACE FUNCTION generar_mensual_presionatmosferica()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN

    WITH
	variable AS (
		SELECT umbral_completo AS umbral FROM variable_variable v WHERE var_id = 8 LIMIT 1
	),
    dato AS (
        SELECT id, estacion_id, fecha
        FROM diario_presionatmosferica d
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
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, completo_umbral
        FROM diario_presionatmosferica d
        WHERE d.estacion_id = (SELECT da.estacion_id FROM dato da)
            AND d.fecha >= (SELECT mes_inicio FROM mes_inicio) AND d.fecha < (SELECT mes_fin FROM mes_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT m.mes_inicio FROM mes_inicio m) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
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
        UPDATE mensual_presionatmosferica SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_mensual AS (
        INSERT INTO mensual_presionatmosferica(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_mensual)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_MENSUAL AS (
        UPDATE diario_presionatmosferica SET usado_para_mensual = TRUE
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

-- ---##############################################################
-- ---####  funcion para generar datos mensuales de temperaturaagua
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_mensual_temperaturaagua();
CREATE OR REPLACE FUNCTION generar_mensual_temperaturaagua()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN

    WITH
	variable AS (
		SELECT umbral_completo AS umbral FROM variable_variable v WHERE var_id = 9 LIMIT 1
	),
    dato AS (
        SELECT id, estacion_id, fecha
        FROM diario_temperaturaagua d
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
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, completo_umbral
        FROM diario_temperaturaagua d
        WHERE d.estacion_id = (SELECT da.estacion_id FROM dato da)
            AND d.fecha >= (SELECT mes_inicio FROM mes_inicio) AND d.fecha < (SELECT mes_fin FROM mes_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT m.mes_inicio FROM mes_inicio m) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
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
        UPDATE mensual_temperaturaagua SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_mensual AS (
        INSERT INTO mensual_temperaturaagua(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_mensual)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_MENSUAL AS (
        UPDATE diario_temperaturaagua SET usado_para_mensual = TRUE
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

-- ---##############################################################
-- ---####  funcion para generar datos mensuales de caudal
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_mensual_caudal();
CREATE OR REPLACE FUNCTION generar_mensual_caudal()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN

    WITH
	variable AS (
		SELECT umbral_completo AS umbral FROM variable_variable v WHERE var_id = 10 LIMIT 1
	),
    dato AS (
        SELECT id, estacion_id, fecha
        FROM diario_caudal d
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
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, completo_umbral
        FROM diario_caudal d
        WHERE d.estacion_id = (SELECT da.estacion_id FROM dato da)
            AND d.fecha >= (SELECT mes_inicio FROM mes_inicio) AND d.fecha < (SELECT mes_fin FROM mes_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT m.mes_inicio FROM mes_inicio m) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
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
        UPDATE mensual_caudal SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_mensual AS (
        INSERT INTO mensual_caudal(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_mensual)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_MENSUAL AS (
        UPDATE diario_caudal SET usado_para_mensual = TRUE
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


-- ---##############################################################
-- ---####  funcion para generar datos mensuales de caudal
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_mensual_nivelagua();
CREATE OR REPLACE FUNCTION generar_mensual_nivelagua()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN

    WITH
	variable AS (
		SELECT umbral_completo AS umbral FROM variable_variable v WHERE var_id = 10 LIMIT 1
	),
    dato AS (
        SELECT id, estacion_id, fecha
        FROM diario_nivelagua d
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
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, completo_umbral
        FROM diario_nivelagua d
        WHERE d.estacion_id = (SELECT da.estacion_id FROM dato da)
            AND d.fecha >= (SELECT mes_inicio FROM mes_inicio) AND d.fecha < (SELECT mes_fin FROM mes_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT m.mes_inicio FROM mes_inicio m) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
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
        UPDATE mensual_nivelagua SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_mensual AS (
        INSERT INTO mensual_nivelagua(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_mensual)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_MENSUAL AS (
        UPDATE diario_nivelagua SET usado_para_mensual = TRUE
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