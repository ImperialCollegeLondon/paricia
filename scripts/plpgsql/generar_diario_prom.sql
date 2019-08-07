-- ---##############################################################
-- ---####  funcion para generar datos diarios de temperaturaaire
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_diario_temperaturaaire();
CREATE OR REPLACE FUNCTION generar_diario_temperaturaaire()
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
        FROM horario_temperaturaaire h
        WHERE h.usado_para_diario = FALSE
        LIMIT 1
    ),
    dia_inicio AS (
        SELECT date_trunc('day', (SELECT d.fecha FROM dato d)) AS dia_inicio LIMIT 1
    ),
    dia_fin AS (
        SELECT (SELECT di.dia_inicio FROM dia_inicio di) + interval '1 day' AS dia_fin LIMIT 1
    ),
	bloque AS (
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones
        FROM horario_temperaturaaire h
        WHERE h.estacion_id = (SELECT d.estacion_id FROM dato d)
            AND h.fecha >= (SELECT dia_inicio FROM dia_inicio) AND h.fecha < (SELECT dia_fin FROM dia_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT dia.dia_inicio FROM dia_inicio dia) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
            (SELECT SUM(b.completo_mediciones)::decimal/24 FROM bloque b) AS completo_mediciones,
            (SELECT COUNT(*)::decimal/24 * 100 FROM bloque b
			 	WHERE b.completo_mediciones >= (SELECT umbral FROM variable) ) AS completo_umbral,
            FALSE AS usado_para_mensual
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_umbral >= 0)
        AS es_valido
        FROM calculo
    ),
    update_diario AS (
        UPDATE diario_temperaturaaire SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c),
            usado_para_mensual = (SELECT c.usado_para_mensual FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_diario AS (
        INSERT INTO diario_temperaturaaire(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual
        FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_diario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_DIARIO AS (
        UPDATE horario_temperaturaaire SET usado_para_diario = TRUE
        WHERE id = ANY(ARRAY(SELECT b.id FROM bloque b))
        AND (EXISTS (SELECT 1 FROM update_diario) OR EXISTS (SELECT 1 FROM insert_diario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE WHEN EXISTS (SELECT id FROM update_USADO_PARA_DIARIO) THEN TRUE
				ELSE FALSE  END) AS resultado
    )
	SELECT r.resultado INTO _resultado FROM resultado r;
    RETURN _resultado;

END
$BODY$  LANGUAGE plpgsql;

-- ---##############################################################
-- ---####  funcion para generar datos diarios de humedadaire
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_diario_humedadaire();
CREATE OR REPLACE FUNCTION generar_diario_humedadaire()
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
        FROM horario_humedadaire h
        WHERE h.usado_para_diario = FALSE
        LIMIT 1
    ),
    dia_inicio AS (
        SELECT date_trunc('day', (SELECT d.fecha FROM dato d)) AS dia_inicio LIMIT 1
    ),
    dia_fin AS (
        SELECT (SELECT di.dia_inicio FROM dia_inicio di) + interval '1 day' AS dia_fin LIMIT 1
    ),
	bloque AS (
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones
        FROM horario_humedadaire h
        WHERE h.estacion_id = (SELECT d.estacion_id FROM dato d)
            AND h.fecha >= (SELECT dia_inicio FROM dia_inicio) AND h.fecha < (SELECT dia_fin FROM dia_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT dia.dia_inicio FROM dia_inicio dia) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
            (SELECT SUM(b.completo_mediciones)::decimal/24 FROM bloque b) AS completo_mediciones,
            (SELECT COUNT(*)::decimal/24 * 100 FROM bloque b
			 	WHERE b.completo_mediciones >= (SELECT umbral FROM variable) ) AS completo_umbral,
            FALSE AS usado_para_mensual
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_umbral >= 0)
        AS es_valido
        FROM calculo
    ),
    update_diario AS (
        UPDATE diario_humedadaire SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c),
            usado_para_mensual = (SELECT c.usado_para_mensual FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_diario AS (
        INSERT INTO diario_humedadaire(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual
        FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_diario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_DIARIO AS (
        UPDATE horario_humedadaire SET usado_para_diario = TRUE
        WHERE id = ANY(ARRAY(SELECT b.id FROM bloque b))
        AND (EXISTS (SELECT 1 FROM update_diario) OR EXISTS (SELECT 1 FROM insert_diario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE WHEN EXISTS (SELECT id FROM update_USADO_PARA_DIARIO) THEN TRUE
				ELSE FALSE  END) AS resultado
    )
	SELECT r.resultado INTO _resultado FROM resultado r;
    RETURN _resultado;

END
$BODY$  LANGUAGE plpgsql;

-- ---##############################################################
-- ---####  funcion para generar datos diarios de velocidadviento
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_diario_velocidadviento();
CREATE OR REPLACE FUNCTION generar_diario_velocidadviento()
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
        FROM horario_velocidadviento h
        WHERE h.usado_para_diario = FALSE
        LIMIT 1
    ),
    dia_inicio AS (
        SELECT date_trunc('day', (SELECT d.fecha FROM dato d)) AS dia_inicio LIMIT 1
    ),
    dia_fin AS (
        SELECT (SELECT di.dia_inicio FROM dia_inicio di) + interval '1 day' AS dia_fin LIMIT 1
    ),
	bloque AS (
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones
        FROM horario_velocidadviento h
        WHERE h.estacion_id = (SELECT d.estacion_id FROM dato d)
            AND h.fecha >= (SELECT dia_inicio FROM dia_inicio) AND h.fecha < (SELECT dia_fin FROM dia_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT dia.dia_inicio FROM dia_inicio dia) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
            (SELECT SUM(b.completo_mediciones)::decimal/24 FROM bloque b) AS completo_mediciones,
            (SELECT COUNT(*)::decimal/24 * 100 FROM bloque b
			 	WHERE b.completo_mediciones >= (SELECT umbral FROM variable) ) AS completo_umbral,
            FALSE AS usado_para_mensual
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_umbral >= 0)
        AS es_valido
        FROM calculo
    ),
    update_diario AS (
        UPDATE diario_velocidadviento SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c),
            usado_para_mensual = (SELECT c.usado_para_mensual FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_diario AS (
        INSERT INTO diario_velocidadviento(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual
        FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_diario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_DIARIO AS (
        UPDATE horario_velocidadviento SET usado_para_diario = TRUE
        WHERE id = ANY(ARRAY(SELECT b.id FROM bloque b))
        AND (EXISTS (SELECT 1 FROM update_diario) OR EXISTS (SELECT 1 FROM insert_diario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE WHEN EXISTS (SELECT id FROM update_USADO_PARA_DIARIO) THEN TRUE
				ELSE FALSE  END) AS resultado
    )
	SELECT r.resultado INTO _resultado FROM resultado r;
    RETURN _resultado;

END
$BODY$  LANGUAGE plpgsql;

-- ---##############################################################
-- ---####  funcion para generar datos diarios de direccionviento
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_diario_direccionviento();
CREATE OR REPLACE FUNCTION generar_diario_direccionviento()
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
        FROM horario_direccionviento h
        WHERE h.usado_para_diario = FALSE
        LIMIT 1
    ),
    dia_inicio AS (
        SELECT date_trunc('day', (SELECT d.fecha FROM dato d)) AS dia_inicio LIMIT 1
    ),
    dia_fin AS (
        SELECT (SELECT di.dia_inicio FROM dia_inicio di) + interval '1 day' AS dia_fin LIMIT 1
    ),
	bloque AS (
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones
        FROM horario_direccionviento h
        WHERE h.estacion_id = (SELECT d.estacion_id FROM dato d)
            AND h.fecha >= (SELECT dia_inicio FROM dia_inicio) AND h.fecha < (SELECT dia_fin FROM dia_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT dia.dia_inicio FROM dia_inicio dia) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
            (SELECT SUM(b.completo_mediciones)::decimal/24 FROM bloque b) AS completo_mediciones,
            (SELECT COUNT(*)::decimal/24 * 100 FROM bloque b
			 	WHERE b.completo_mediciones >= (SELECT umbral FROM variable) ) AS completo_umbral,
            FALSE AS usado_para_mensual
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_umbral >= 0)
        AS es_valido
        FROM calculo
    ),
    update_diario AS (
        UPDATE diario_direccionviento SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c),
            usado_para_mensual = (SELECT c.usado_para_mensual FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_diario AS (
        INSERT INTO diario_direccionviento(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual
        FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_diario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_DIARIO AS (
        UPDATE horario_direccionviento SET usado_para_diario = TRUE
        WHERE id = ANY(ARRAY(SELECT b.id FROM bloque b))
        AND (EXISTS (SELECT 1 FROM update_diario) OR EXISTS (SELECT 1 FROM insert_diario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE WHEN EXISTS (SELECT id FROM update_USADO_PARA_DIARIO) THEN TRUE
				ELSE FALSE  END) AS resultado
    )
	SELECT r.resultado INTO _resultado FROM resultado r;
    RETURN _resultado;

END
$BODY$  LANGUAGE plpgsql;

-- ---##############################################################
-- ---####  funcion para generar datos diarios de humedadsuelo
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_diario_humedadsuelo();
CREATE OR REPLACE FUNCTION generar_diario_humedadsuelo()
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
        FROM horario_humedadsuelo h
        WHERE h.usado_para_diario = FALSE
        LIMIT 1
    ),
    dia_inicio AS (
        SELECT date_trunc('day', (SELECT d.fecha FROM dato d)) AS dia_inicio LIMIT 1
    ),
    dia_fin AS (
        SELECT (SELECT di.dia_inicio FROM dia_inicio di) + interval '1 day' AS dia_fin LIMIT 1
    ),
	bloque AS (
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones
        FROM horario_humedadsuelo h
        WHERE h.estacion_id = (SELECT d.estacion_id FROM dato d)
            AND h.fecha >= (SELECT dia_inicio FROM dia_inicio) AND h.fecha < (SELECT dia_fin FROM dia_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT dia.dia_inicio FROM dia_inicio dia) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
            (SELECT SUM(b.completo_mediciones)::decimal/24 FROM bloque b) AS completo_mediciones,
            (SELECT COUNT(*)::decimal/24 * 100 FROM bloque b
			 	WHERE b.completo_mediciones >= (SELECT umbral FROM variable) ) AS completo_umbral,
            FALSE AS usado_para_mensual
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_umbral >= 0)
        AS es_valido
        FROM calculo
    ),
    update_diario AS (
        UPDATE diario_humedadsuelo SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c),
            usado_para_mensual = (SELECT c.usado_para_mensual FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_diario AS (
        INSERT INTO diario_humedadsuelo(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual
        FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_diario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_DIARIO AS (
        UPDATE horario_humedadsuelo SET usado_para_diario = TRUE
        WHERE id = ANY(ARRAY(SELECT b.id FROM bloque b))
        AND (EXISTS (SELECT 1 FROM update_diario) OR EXISTS (SELECT 1 FROM insert_diario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE WHEN EXISTS (SELECT id FROM update_USADO_PARA_DIARIO) THEN TRUE
				ELSE FALSE  END) AS resultado
    )
	SELECT r.resultado INTO _resultado FROM resultado r;
    RETURN _resultado;

END
$BODY$  LANGUAGE plpgsql;

-- ---##############################################################
-- ---####  funcion para generar datos diarios de radiacionsolar
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_diario_radiacionsolar();
CREATE OR REPLACE FUNCTION generar_diario_radiacionsolar()
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
        FROM horario_radiacionsolar h
        WHERE h.usado_para_diario = FALSE
        LIMIT 1
    ),
    dia_inicio AS (
        SELECT date_trunc('day', (SELECT d.fecha FROM dato d)) AS dia_inicio LIMIT 1
    ),
    dia_fin AS (
        SELECT (SELECT di.dia_inicio FROM dia_inicio di) + interval '1 day' AS dia_fin LIMIT 1
    ),
	bloque AS (
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones
        FROM horario_radiacionsolar h
        WHERE h.estacion_id = (SELECT d.estacion_id FROM dato d)
            AND h.fecha >= (SELECT dia_inicio FROM dia_inicio) AND h.fecha < (SELECT dia_fin FROM dia_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT dia.dia_inicio FROM dia_inicio dia) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
            (SELECT SUM(b.completo_mediciones)::decimal/24 FROM bloque b) AS completo_mediciones,
            (SELECT COUNT(*)::decimal/24 * 100 FROM bloque b
			 	WHERE b.completo_mediciones >= (SELECT umbral FROM variable) ) AS completo_umbral,
            FALSE AS usado_para_mensual
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_umbral >= 0)
        AS es_valido
        FROM calculo
    ),
    update_diario AS (
        UPDATE diario_radiacionsolar SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c),
            usado_para_mensual = (SELECT c.usado_para_mensual FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_diario AS (
        INSERT INTO diario_radiacionsolar(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual
        FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_diario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_DIARIO AS (
        UPDATE horario_radiacionsolar SET usado_para_diario = TRUE
        WHERE id = ANY(ARRAY(SELECT b.id FROM bloque b))
        AND (EXISTS (SELECT 1 FROM update_diario) OR EXISTS (SELECT 1 FROM insert_diario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE WHEN EXISTS (SELECT id FROM update_USADO_PARA_DIARIO) THEN TRUE
				ELSE FALSE  END) AS resultado
    )
	SELECT r.resultado INTO _resultado FROM resultado r;
    RETURN _resultado;

END
$BODY$  LANGUAGE plpgsql;

-- ---##############################################################
-- ---####  funcion para generar datos diarios de presionatmosferica
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_diario_presionatmosferica();
CREATE OR REPLACE FUNCTION generar_diario_presionatmosferica()
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
        FROM horario_presionatmosferica h
        WHERE h.usado_para_diario = FALSE
        LIMIT 1
    ),
    dia_inicio AS (
        SELECT date_trunc('day', (SELECT d.fecha FROM dato d)) AS dia_inicio LIMIT 1
    ),
    dia_fin AS (
        SELECT (SELECT di.dia_inicio FROM dia_inicio di) + interval '1 day' AS dia_fin LIMIT 1
    ),
	bloque AS (
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones
        FROM horario_presionatmosferica h
        WHERE h.estacion_id = (SELECT d.estacion_id FROM dato d)
            AND h.fecha >= (SELECT dia_inicio FROM dia_inicio) AND h.fecha < (SELECT dia_fin FROM dia_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT dia.dia_inicio FROM dia_inicio dia) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
            (SELECT SUM(b.completo_mediciones)::decimal/24 FROM bloque b) AS completo_mediciones,
            (SELECT COUNT(*)::decimal/24 * 100 FROM bloque b
			 	WHERE b.completo_mediciones >= (SELECT umbral FROM variable) ) AS completo_umbral,
            FALSE AS usado_para_mensual
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_umbral >= 0)
        AS es_valido
        FROM calculo
    ),
    update_diario AS (
        UPDATE diario_presionatmosferica SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c),
            usado_para_mensual = (SELECT c.usado_para_mensual FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_diario AS (
        INSERT INTO diario_presionatmosferica(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual
        FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_diario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_DIARIO AS (
        UPDATE horario_presionatmosferica SET usado_para_diario = TRUE
        WHERE id = ANY(ARRAY(SELECT b.id FROM bloque b))
        AND (EXISTS (SELECT 1 FROM update_diario) OR EXISTS (SELECT 1 FROM insert_diario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE WHEN EXISTS (SELECT id FROM update_USADO_PARA_DIARIO) THEN TRUE
				ELSE FALSE  END) AS resultado
    )
	SELECT r.resultado INTO _resultado FROM resultado r;
    RETURN _resultado;

END
$BODY$  LANGUAGE plpgsql;

-- ---##############################################################
-- ---####  funcion para generar datos diarios de temperaturaagua
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_diario_temperaturaagua();
CREATE OR REPLACE FUNCTION generar_diario_temperaturaagua()
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
        FROM horario_temperaturaagua h
        WHERE h.usado_para_diario = FALSE
        LIMIT 1
    ),
    dia_inicio AS (
        SELECT date_trunc('day', (SELECT d.fecha FROM dato d)) AS dia_inicio LIMIT 1
    ),
    dia_fin AS (
        SELECT (SELECT di.dia_inicio FROM dia_inicio di) + interval '1 day' AS dia_fin LIMIT 1
    ),
	bloque AS (
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones
        FROM horario_temperaturaagua h
        WHERE h.estacion_id = (SELECT d.estacion_id FROM dato d)
            AND h.fecha >= (SELECT dia_inicio FROM dia_inicio) AND h.fecha < (SELECT dia_fin FROM dia_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT dia.dia_inicio FROM dia_inicio dia) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
            (SELECT SUM(b.completo_mediciones)::decimal/24 FROM bloque b) AS completo_mediciones,
            (SELECT COUNT(*)::decimal/24 * 100 FROM bloque b
			 	WHERE b.completo_mediciones >= (SELECT umbral FROM variable) ) AS completo_umbral,
            FALSE AS usado_para_mensual
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_umbral >= 0)
        AS es_valido
        FROM calculo
    ),
    update_diario AS (
        UPDATE diario_temperaturaagua SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c),
            usado_para_mensual = (SELECT c.usado_para_mensual FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_diario AS (
        INSERT INTO diario_temperaturaagua(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual
        FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_diario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_DIARIO AS (
        UPDATE horario_temperaturaagua SET usado_para_diario = TRUE
        WHERE id = ANY(ARRAY(SELECT b.id FROM bloque b))
        AND (EXISTS (SELECT 1 FROM update_diario) OR EXISTS (SELECT 1 FROM insert_diario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE WHEN EXISTS (SELECT id FROM update_USADO_PARA_DIARIO) THEN TRUE
				ELSE FALSE  END) AS resultado
    )
	SELECT r.resultado INTO _resultado FROM resultado r;
    RETURN _resultado;

END
$BODY$  LANGUAGE plpgsql;

-- ---##############################################################
-- ---####  funcion para generar datos diarios de caudal
-- ---##############################################################

DROP FUNCTION IF EXISTS generar_diario_caudal();
CREATE OR REPLACE FUNCTION generar_diario_caudal()
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
        FROM horario_caudal h
        WHERE h.usado_para_diario = FALSE
        LIMIT 1
    ),
    dia_inicio AS (
        SELECT date_trunc('day', (SELECT d.fecha FROM dato d)) AS dia_inicio LIMIT 1
    ),
    dia_fin AS (
        SELECT (SELECT di.dia_inicio FROM dia_inicio di) + interval '1 day' AS dia_fin LIMIT 1
    ),
	bloque AS (
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones
        FROM horario_caudal h
        WHERE h.estacion_id = (SELECT d.estacion_id FROM dato d)
            AND h.fecha >= (SELECT dia_inicio FROM dia_inicio) AND h.fecha < (SELECT dia_fin FROM dia_fin)
	),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT dia.dia_inicio FROM dia_inicio dia) AS fecha,
            (SELECT AVG(b.valor) FROM bloque b) AS valor,
			(SELECT MAX(b.max_abs) FROM bloque b) AS max_abs,
			(SELECT MIN(b.min_abs) FROM bloque b) AS min_abs,
			(SELECT MAX(b.valor) FROM bloque b) AS max_del_prom,
			(SELECT MIN(b.valor) FROM bloque b) AS min_del_prom,
            (SELECT SUM(b.completo_mediciones)::decimal/24 FROM bloque b) AS completo_mediciones,
            (SELECT COUNT(*)::decimal/24 * 100 FROM bloque b
			 	WHERE b.completo_mediciones >= (SELECT umbral FROM variable) ) AS completo_umbral,
            FALSE AS usado_para_mensual
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_umbral >= 0)
        AS es_valido
        FROM calculo
    ),
    update_diario AS (
        UPDATE diario_caudal SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
			completo_umbral = (SELECT c.completo_umbral FROM calculo c),
            usado_para_mensual = (SELECT c.usado_para_mensual FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_diario AS (
        INSERT INTO diario_caudal(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom, completo_mediciones, completo_umbral, usado_para_mensual
        FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_diario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_DIARIO AS (
        UPDATE horario_caudal SET usado_para_diario = TRUE
        WHERE id = ANY(ARRAY(SELECT b.id FROM bloque b))
        AND (EXISTS (SELECT 1 FROM update_diario) OR EXISTS (SELECT 1 FROM insert_diario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE WHEN EXISTS (SELECT id FROM update_USADO_PARA_DIARIO) THEN TRUE
				ELSE FALSE  END) AS resultado
    )
	SELECT r.resultado INTO _resultado FROM resultado r;
    RETURN _resultado;

END
$BODY$  LANGUAGE plpgsql;