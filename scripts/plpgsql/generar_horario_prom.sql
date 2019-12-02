-- funcion para temperatura del aire

DROP FUNCTION IF EXISTS generar_horario_temperaturaaire();
CREATE OR REPLACE FUNCTION generar_horario_temperaturaaire()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN
    WITH
    dato AS (
        SELECT id, estacion_id, fecha FROM validacion_temperaturaaire v
        WHERE v.usado_para_horario = FALSE
        LIMIT 1
    ),
    hora_inicio AS (
        SELECT date_trunc('hour', (SELECT d.fecha FROM dato d)) AS hora_inicio
    ),
    hora_fin AS (
        SELECT (SELECT hi.hora_inicio FROM hora_inicio hi) + interval '1 hour' AS hora_fin
    ),
    numero_datos_esperado AS (
        SELECT CAST(60/f.fre_valor AS INT) ndatos
        FROM frecuencia_frecuencia f
        WHERE f.est_id_id = (SELECT d.estacion_id FROM dato d) AND f.var_id_id = 2
            AND f.fre_fecha_ini <= (SELECT d.fecha FROM dato d)
            AND (f.fre_fecha_fin >= (SELECT d.fecha FROM dato d) OR f.fre_fecha_fin IS NULL)
        ORDER BY f.fre_fecha_ini DESC LIMIT 1
    ),
    validados AS(
        SELECT id, estacion_id, fecha, valor, validacion FROM validacion_temperaturaaire v
        WHERE estacion_id = (SELECT d.estacion_id FROM dato d)
            AND fecha >= (SELECT hora_inicio FROM hora_inicio) AND fecha < (SELECT hora_fin FROM hora_fin)
    ),
    seleccionados AS (
        SELECT v.fecha, v.valor FROM (
            SELECT fecha, MAX(validacion) AS validacion FROM validados v GROUP BY fecha
        ) AS tbl_max
        INNER JOIN validados v
        ON v.fecha = tbl_max.fecha AND v.validacion = tbl_max.validacion
    ),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT h.hora_inicio FROM hora_inicio h) AS fecha,
            (SELECT AVG(valor) FROM seleccionados s) AS valor,
			(SELECT MAX(valor) FROM seleccionados s) AS max_abs,
			(SELECT MIN(valor) FROM seleccionados s) AS min_abs,
            (SELECT COUNT(s.valor)::decimal/(SELECT nde.ndatos FROM numero_datos_esperado nde) * 100
                FROM seleccionados s WHERE s.valor IS NOT NULL) AS completo_mediciones,
            FALSE AS usado_para_diario
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_mediciones >= 0)
        AS es_valido
        FROM calculo
    ),
    update_horario AS (
        UPDATE horario_temperaturaaire SET
            valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
            usado_para_diario = (SELECT c.usado_para_diario FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_horario AS (
        INSERT INTO horario_temperaturaaire(estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_horario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_HORARIO_validados AS (
        UPDATE validacion_temperaturaaire SET usado_para_horario = TRUE
        WHERE id = ANY(ARRAY(SELECT vs.id FROM validados vs))
        AND (EXISTS (SELECT 1 FROM update_horario) OR EXISTS (SELECT 1 FROM insert_horario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE
            WHEN EXISTS (SELECT id FROM update_USADO_PARA_HORARIO_validados) THEN TRUE
            ELSE FALSE
            END) AS resultado
    )
    SELECT r.resultado INTO _resultado FROM resultado r;
    return _resultado;
END
$BODY$  LANGUAGE plpgsql;

--******************************
-- funcion para humedadaire
DROP FUNCTION IF EXISTS generar_horario_humedadaire();
CREATE OR REPLACE FUNCTION generar_horario_humedadaire()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN
    WITH
    dato AS (
        SELECT id, estacion_id, fecha FROM validacion_humedadaire v
        WHERE v.usado_para_horario = FALSE
        LIMIT 1
    ),
    hora_inicio AS (
        SELECT date_trunc('hour', (SELECT d.fecha FROM dato d)) AS hora_inicio
    ),
    hora_fin AS (
        SELECT (SELECT hi.hora_inicio FROM hora_inicio hi) + interval '1 hour' AS hora_fin
    ),
    numero_datos_esperado AS (
        SELECT CAST(60/f.fre_valor AS INT) ndatos
        FROM frecuencia_frecuencia f
        WHERE f.est_id_id = (SELECT d.estacion_id FROM dato d) AND f.var_id_id = 3
            AND f.fre_fecha_ini <= (SELECT d.fecha FROM dato d)
            AND (f.fre_fecha_fin >= (SELECT d.fecha FROM dato d) OR f.fre_fecha_fin IS NULL)
        ORDER BY f.fre_fecha_ini DESC LIMIT 1
    ),
    validados AS(
        SELECT id, estacion_id, fecha, valor, validacion FROM validacion_humedadaire v
        WHERE estacion_id = (SELECT d.estacion_id FROM dato d)
            AND fecha >= (SELECT hora_inicio FROM hora_inicio) AND fecha < (SELECT hora_fin FROM hora_fin)
    ),
    seleccionados AS (
        SELECT v.fecha, v.valor FROM (
            SELECT fecha, MAX(validacion) AS validacion FROM validados v GROUP BY fecha
        ) AS tbl_max
        INNER JOIN validados v
        ON v.fecha = tbl_max.fecha AND v.validacion = tbl_max.validacion
    ),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT h.hora_inicio FROM hora_inicio h) AS fecha,
            (SELECT AVG(valor) FROM seleccionados s) AS valor,
			(SELECT MAX(valor) FROM seleccionados s) AS max_abs,
			(SELECT MIN(valor) FROM seleccionados s) AS min_abs,
            (SELECT COUNT(s.valor)::decimal/(SELECT nde.ndatos FROM numero_datos_esperado nde) * 100
                FROM seleccionados s WHERE s.valor IS NOT NULL) AS completo_mediciones,
            FALSE AS usado_para_diario
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_mediciones >= 0)
        AS es_valido
        FROM calculo
    ),
    update_horario AS (
        UPDATE horario_humedadaire SET
            valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
            usado_para_diario = (SELECT c.usado_para_diario FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_horario AS (
        INSERT INTO horario_humedadaire(estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_horario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_HORARIO_validados AS (
        UPDATE validacion_humedadaire SET usado_para_horario = TRUE
        WHERE id = ANY(ARRAY(SELECT vs.id FROM validados vs))
        AND (EXISTS (SELECT 1 FROM update_horario) OR EXISTS (SELECT 1 FROM insert_horario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE
            WHEN EXISTS (SELECT id FROM update_USADO_PARA_HORARIO_validados) THEN TRUE
            ELSE FALSE
            END) AS resultado
    )
    SELECT r.resultado INTO _resultado FROM resultado r;
    return _resultado;
END
$BODY$  LANGUAGE plpgsql;

----**********************************
---- funcion para Velocidad del Viento

DROP FUNCTION IF EXISTS generar_horario_velocidadviento();
CREATE OR REPLACE FUNCTION generar_horario_velocidadviento()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN
    WITH
    dato AS (
        SELECT id, estacion_id, fecha FROM validacion_velocidadviento v
        WHERE v.usado_para_horario = FALSE
        LIMIT 1
    ),
    hora_inicio AS (
        SELECT date_trunc('hour', (SELECT d.fecha FROM dato d)) AS hora_inicio
    ),
    hora_fin AS (
        SELECT (SELECT hi.hora_inicio FROM hora_inicio hi) + interval '1 hour' AS hora_fin
    ),
    numero_datos_esperado AS (
        SELECT CAST(60/f.fre_valor AS INT) ndatos
        FROM frecuencia_frecuencia f
        WHERE f.est_id_id = (SELECT d.estacion_id FROM dato d) AND f.var_id_id = 4
            AND f.fre_fecha_ini <= (SELECT d.fecha FROM dato d)
            AND (f.fre_fecha_fin >= (SELECT d.fecha FROM dato d) OR f.fre_fecha_fin IS NULL)
        ORDER BY f.fre_fecha_ini DESC LIMIT 1
    ),
    validados AS(
        SELECT id, estacion_id, fecha, valor, validacion FROM validacion_velocidadviento v
        WHERE estacion_id = (SELECT d.estacion_id FROM dato d)
            AND fecha >= (SELECT hora_inicio FROM hora_inicio) AND fecha < (SELECT hora_fin FROM hora_fin)
    ),
    seleccionados AS (
        SELECT v.fecha, v.valor FROM (
            SELECT fecha, MAX(validacion) AS validacion FROM validados v GROUP BY fecha
        ) AS tbl_max
        INNER JOIN validados v
        ON v.fecha = tbl_max.fecha AND v.validacion = tbl_max.validacion
    ),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT h.hora_inicio FROM hora_inicio h) AS fecha,
            (SELECT AVG(valor) FROM seleccionados s) AS valor,
			(SELECT MAX(valor) FROM seleccionados s) AS max_abs,
			(SELECT MIN(valor) FROM seleccionados s) AS min_abs,
            (SELECT COUNT(s.valor)::decimal/(SELECT nde.ndatos FROM numero_datos_esperado nde) * 100
                FROM seleccionados s WHERE s.valor IS NOT NULL) AS completo_mediciones,
            FALSE AS usado_para_diario
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_mediciones >= 0)
        AS es_valido
        FROM calculo
    ),
    update_horario AS (
        UPDATE horario_velocidadviento SET
            valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
            usado_para_diario = (SELECT c.usado_para_diario FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_horario AS (
        INSERT INTO horario_velocidadviento(estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_horario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_HORARIO_validados AS (
        UPDATE validacion_velocidadviento SET usado_para_horario = TRUE
        WHERE id = ANY(ARRAY(SELECT vs.id FROM validados vs))
        AND (EXISTS (SELECT 1 FROM update_horario) OR EXISTS (SELECT 1 FROM insert_horario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE
            WHEN EXISTS (SELECT id FROM update_USADO_PARA_HORARIO_validados) THEN TRUE
            ELSE FALSE
            END) AS resultado
    )
    SELECT r.resultado INTO _resultado FROM resultado r;
    return _resultado;
END
$BODY$  LANGUAGE plpgsql;

-- *****************************
---  funcion para Direccion del Viento

DROP FUNCTION IF EXISTS generar_horario_direccionviento();
CREATE OR REPLACE FUNCTION generar_horario_direccionviento()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN
    WITH
    dato AS (
        SELECT id, estacion_id, fecha FROM validacion_direccionviento v
        WHERE v.usado_para_horario = FALSE
        LIMIT 1
    ),
    hora_inicio AS (
        SELECT date_trunc('hour', (SELECT d.fecha FROM dato d)) AS hora_inicio
    ),
    hora_fin AS (
        SELECT (SELECT hi.hora_inicio FROM hora_inicio hi) + interval '1 hour' AS hora_fin
    ),
    numero_datos_esperado AS (
        SELECT CAST(60/f.fre_valor AS INT) ndatos
        FROM frecuencia_frecuencia f
        WHERE f.est_id_id = (SELECT d.estacion_id FROM dato d) AND f.var_id_id = 5
            AND f.fre_fecha_ini <= (SELECT d.fecha FROM dato d)
            AND (f.fre_fecha_fin >= (SELECT d.fecha FROM dato d) OR f.fre_fecha_fin IS NULL)
        ORDER BY f.fre_fecha_ini DESC LIMIT 1
    ),
    validados AS(
        SELECT id, estacion_id, fecha, valor, validacion FROM validacion_direccionviento v
        WHERE estacion_id = (SELECT d.estacion_id FROM dato d)
            AND fecha >= (SELECT hora_inicio FROM hora_inicio) AND fecha < (SELECT hora_fin FROM hora_fin)
    ),
    seleccionados AS (
        SELECT v.fecha, v.valor FROM (
            SELECT fecha, MAX(validacion) AS validacion FROM validados v GROUP BY fecha
        ) AS tbl_max
        INNER JOIN validados v
        ON v.fecha = tbl_max.fecha AND v.validacion = tbl_max.validacion
    ),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT h.hora_inicio FROM hora_inicio h) AS fecha,
            (SELECT AVG(valor) FROM seleccionados s) AS valor,
			(SELECT MAX(valor) FROM seleccionados s) AS max_abs,
			(SELECT MIN(valor) FROM seleccionados s) AS min_abs,
            (SELECT COUNT(s.valor)::decimal/(SELECT nde.ndatos FROM numero_datos_esperado nde) * 100
                FROM seleccionados s WHERE s.valor IS NOT NULL) AS completo_mediciones,
            FALSE AS usado_para_diario
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_mediciones >= 0)
        AS es_valido
        FROM calculo
    ),
    update_horario AS (
        UPDATE horario_direccionviento SET
            valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
            usado_para_diario = (SELECT c.usado_para_diario FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_horario AS (
        INSERT INTO horario_direccionviento(estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_horario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_HORARIO_validados AS (
        UPDATE validacion_direccionviento SET usado_para_horario = TRUE
        WHERE id = ANY(ARRAY(SELECT vs.id FROM validados vs))
        AND (EXISTS (SELECT 1 FROM update_horario) OR EXISTS (SELECT 1 FROM insert_horario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE
            WHEN EXISTS (SELECT id FROM update_USADO_PARA_HORARIO_validados) THEN TRUE
            ELSE FALSE
            END) AS resultado
    )
    SELECT r.resultado INTO _resultado FROM resultado r;
    return _resultado;
END
$BODY$  LANGUAGE plpgsql;

-- ******************************************************* -- -
-- funcion para humedadsuelo

DROP FUNCTION IF EXISTS generar_horario_humedadsuelo();
CREATE OR REPLACE FUNCTION generar_horario_humedadsuelo()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN
    WITH
    dato AS (
        SELECT id, estacion_id, fecha FROM validacion_humedadsuelo v
        WHERE v.usado_para_horario = FALSE
        LIMIT 1
    ),
    hora_inicio AS (
        SELECT date_trunc('hour', (SELECT d.fecha FROM dato d)) AS hora_inicio
    ),
    hora_fin AS (
        SELECT (SELECT hi.hora_inicio FROM hora_inicio hi) + interval '1 hour' AS hora_fin
    ),
    numero_datos_esperado AS (
        SELECT CAST(60/f.fre_valor AS INT) ndatos
        FROM frecuencia_frecuencia f
        WHERE f.est_id_id = (SELECT d.estacion_id FROM dato d) AND f.var_id_id = 6
            AND f.fre_fecha_ini <= (SELECT d.fecha FROM dato d)
            AND (f.fre_fecha_fin >= (SELECT d.fecha FROM dato d) OR f.fre_fecha_fin IS NULL)
        ORDER BY f.fre_fecha_ini DESC LIMIT 1
    ),
    validados AS(
        SELECT id, estacion_id, fecha, valor, validacion FROM validacion_humedadsuelo v
        WHERE estacion_id = (SELECT d.estacion_id FROM dato d)
            AND fecha >= (SELECT hora_inicio FROM hora_inicio) AND fecha < (SELECT hora_fin FROM hora_fin)
    ),
    seleccionados AS (
        SELECT v.fecha, v.valor FROM (
            SELECT fecha, MAX(validacion) AS validacion FROM validados v GROUP BY fecha
        ) AS tbl_max
        INNER JOIN validados v
        ON v.fecha = tbl_max.fecha AND v.validacion = tbl_max.validacion
    ),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT h.hora_inicio FROM hora_inicio h) AS fecha,
            (SELECT AVG(valor) FROM seleccionados s) AS valor,
			(SELECT MAX(valor) FROM seleccionados s) AS max_abs,
			(SELECT MIN(valor) FROM seleccionados s) AS min_abs,
            (SELECT COUNT(s.valor)::decimal/(SELECT nde.ndatos FROM numero_datos_esperado nde) * 100
                FROM seleccionados s WHERE s.valor IS NOT NULL) AS completo_mediciones,
            FALSE AS usado_para_diario
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_mediciones >= 0)
        AS es_valido
        FROM calculo
    ),
    update_horario AS (
        UPDATE horario_humedadsuelo SET
            valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
            usado_para_diario = (SELECT c.usado_para_diario FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_horario AS (
        INSERT INTO horario_humedadsuelo(estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_horario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_HORARIO_validados AS (
        UPDATE validacion_humedadsuelo SET usado_para_horario = TRUE
        WHERE id = ANY(ARRAY(SELECT vs.id FROM validados vs))
        AND (EXISTS (SELECT 1 FROM update_horario) OR EXISTS (SELECT 1 FROM insert_horario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE
            WHEN EXISTS (SELECT id FROM update_USADO_PARA_HORARIO_validados) THEN TRUE
            ELSE FALSE
            END) AS resultado
    )
    SELECT r.resultado INTO _resultado FROM resultado r;
    return _resultado;
END
$BODY$  LANGUAGE plpgsql;

-- ******************************************************* -- -
-- funcion para radiacionsolar

DROP FUNCTION IF EXISTS generar_horario_radiacionsolar();
CREATE OR REPLACE FUNCTION generar_horario_radiacionsolar()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN
    WITH
    dato AS (
        SELECT id, estacion_id, fecha FROM validacion_radiacionsolar v
        WHERE v.usado_para_horario = FALSE
        LIMIT 1
    ),
    hora_inicio AS (
        SELECT date_trunc('hour', (SELECT d.fecha FROM dato d)) AS hora_inicio
    ),
    hora_fin AS (
        SELECT (SELECT hi.hora_inicio FROM hora_inicio hi) + interval '1 hour' AS hora_fin
    ),
    numero_datos_esperado AS (
        SELECT CAST(60/f.fre_valor AS INT) ndatos
        FROM frecuencia_frecuencia f
        WHERE f.est_id_id = (SELECT d.estacion_id FROM dato d) AND f.var_id_id = 7
            AND f.fre_fecha_ini <= (SELECT d.fecha FROM dato d)
            AND (f.fre_fecha_fin >= (SELECT d.fecha FROM dato d) OR f.fre_fecha_fin IS NULL)
        ORDER BY f.fre_fecha_ini DESC LIMIT 1
    ),
    validados AS(
        SELECT id, estacion_id, fecha, valor, validacion FROM validacion_radiacionsolar v
        WHERE estacion_id = (SELECT d.estacion_id FROM dato d)
            AND fecha >= (SELECT hora_inicio FROM hora_inicio) AND fecha < (SELECT hora_fin FROM hora_fin)
    ),
    seleccionados AS (
        SELECT v.fecha, v.valor FROM (
            SELECT fecha, MAX(validacion) AS validacion FROM validados v GROUP BY fecha
        ) AS tbl_max
        INNER JOIN validados v
        ON v.fecha = tbl_max.fecha AND v.validacion = tbl_max.validacion
    ),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT h.hora_inicio FROM hora_inicio h) AS fecha,
            (SELECT AVG(valor) FROM seleccionados s) AS valor,
			(SELECT MAX(valor) FROM seleccionados s) AS max_abs,
			(SELECT MIN(valor) FROM seleccionados s) AS min_abs,
            (SELECT COUNT(s.valor)::decimal/(SELECT nde.ndatos FROM numero_datos_esperado nde) * 100
                FROM seleccionados s WHERE s.valor IS NOT NULL) AS completo_mediciones,
            FALSE AS usado_para_diario
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_mediciones >= 0)
        AS es_valido
        FROM calculo
    ),
    update_horario AS (
        UPDATE horario_radiacionsolar SET
            valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
            usado_para_diario = (SELECT c.usado_para_diario FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_horario AS (
        INSERT INTO horario_radiacionsolar(estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_horario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_HORARIO_validados AS (
        UPDATE validacion_radiacionsolar SET usado_para_horario = TRUE
        WHERE id = ANY(ARRAY(SELECT vs.id FROM validados vs))
        AND (EXISTS (SELECT 1 FROM update_horario) OR EXISTS (SELECT 1 FROM insert_horario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE
            WHEN EXISTS (SELECT id FROM update_USADO_PARA_HORARIO_validados) THEN TRUE
            ELSE FALSE
            END) AS resultado
    )
    SELECT r.resultado INTO _resultado FROM resultado r;
    return _resultado;
END
$BODY$  LANGUAGE plpgsql;

-- ******************************************************* -- -
-- funcion para presionatmosferica

DROP FUNCTION IF EXISTS generar_horario_presionatmosferica();
CREATE OR REPLACE FUNCTION generar_horario_presionatmosferica()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN
    WITH
    dato AS (
        SELECT id, estacion_id, fecha FROM validacion_presionatmosferica v
        WHERE v.usado_para_horario = FALSE
        LIMIT 1
    ),
    hora_inicio AS (
        SELECT date_trunc('hour', (SELECT d.fecha FROM dato d)) AS hora_inicio
    ),
    hora_fin AS (
        SELECT (SELECT hi.hora_inicio FROM hora_inicio hi) + interval '1 hour' AS hora_fin
    ),
    numero_datos_esperado AS (
        SELECT CAST(60/f.fre_valor AS INT) ndatos
        FROM frecuencia_frecuencia f
        WHERE f.est_id_id = (SELECT d.estacion_id FROM dato d) AND f.var_id_id = 8
            AND f.fre_fecha_ini <= (SELECT d.fecha FROM dato d)
            AND (f.fre_fecha_fin >= (SELECT d.fecha FROM dato d) OR f.fre_fecha_fin IS NULL)
        ORDER BY f.fre_fecha_ini DESC LIMIT 1
    ),
    validados AS(
        SELECT id, estacion_id, fecha, valor, validacion FROM validacion_presionatmosferica v
        WHERE estacion_id = (SELECT d.estacion_id FROM dato d)
            AND fecha >= (SELECT hora_inicio FROM hora_inicio) AND fecha < (SELECT hora_fin FROM hora_fin)
    ),
    seleccionados AS (
        SELECT v.fecha, v.valor FROM (
            SELECT fecha, MAX(validacion) AS validacion FROM validados v GROUP BY fecha
        ) AS tbl_max
        INNER JOIN validados v
        ON v.fecha = tbl_max.fecha AND v.validacion = tbl_max.validacion
    ),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT h.hora_inicio FROM hora_inicio h) AS fecha,
            (SELECT AVG(valor) FROM seleccionados s) AS valor,
			(SELECT MAX(valor) FROM seleccionados s) AS max_abs,
			(SELECT MIN(valor) FROM seleccionados s) AS min_abs,
            (SELECT COUNT(s.valor)::decimal/(SELECT nde.ndatos FROM numero_datos_esperado nde) * 100
                FROM seleccionados s WHERE s.valor IS NOT NULL) AS completo_mediciones,
            FALSE AS usado_para_diario
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_mediciones >= 0)
        AS es_valido
        FROM calculo
    ),
    update_horario AS (
        UPDATE horario_presionatmosferica SET
            valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
            usado_para_diario = (SELECT c.usado_para_diario FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_horario AS (
        INSERT INTO horario_presionatmosferica(estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_horario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_HORARIO_validados AS (
        UPDATE validacion_presionatmosferica SET usado_para_horario = TRUE
        WHERE id = ANY(ARRAY(SELECT vs.id FROM validados vs))
        AND (EXISTS (SELECT 1 FROM update_horario) OR EXISTS (SELECT 1 FROM insert_horario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE
            WHEN EXISTS (SELECT id FROM update_USADO_PARA_HORARIO_validados) THEN TRUE
            ELSE FALSE
            END) AS resultado
    )
    SELECT r.resultado INTO _resultado FROM resultado r;
    return _resultado;
END
$BODY$  LANGUAGE plpgsql;

-- ******************************************************* -- -
-- funcion para temperaturaagua

DROP FUNCTION IF EXISTS generar_horario_temperaturaagua();
CREATE OR REPLACE FUNCTION generar_horario_temperaturaagua()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN
    WITH
    dato AS (
        SELECT id, estacion_id, fecha FROM validacion_temperaturaagua v
        WHERE v.usado_para_horario = FALSE
        LIMIT 1
    ),
    hora_inicio AS (
        SELECT date_trunc('hour', (SELECT d.fecha FROM dato d)) AS hora_inicio
    ),
    hora_fin AS (
        SELECT (SELECT hi.hora_inicio FROM hora_inicio hi) + interval '1 hour' AS hora_fin
    ),
    numero_datos_esperado AS (
        SELECT CAST(60/f.fre_valor AS INT) ndatos
        FROM frecuencia_frecuencia f
        WHERE f.est_id_id = (SELECT d.estacion_id FROM dato d) AND f.var_id_id = 9
            AND f.fre_fecha_ini <= (SELECT d.fecha FROM dato d)
            AND (f.fre_fecha_fin >= (SELECT d.fecha FROM dato d) OR f.fre_fecha_fin IS NULL)
        ORDER BY f.fre_fecha_ini DESC LIMIT 1
    ),
    validados AS(
        SELECT id, estacion_id, fecha, valor, validacion FROM validacion_temperaturaagua v
        WHERE estacion_id = (SELECT d.estacion_id FROM dato d)
            AND fecha >= (SELECT hora_inicio FROM hora_inicio) AND fecha < (SELECT hora_fin FROM hora_fin)
    ),
    seleccionados AS (
        SELECT v.fecha, v.valor FROM (
            SELECT fecha, MAX(validacion) AS validacion FROM validados v GROUP BY fecha
        ) AS tbl_max
        INNER JOIN validados v
        ON v.fecha = tbl_max.fecha AND v.validacion = tbl_max.validacion
    ),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT h.hora_inicio FROM hora_inicio h) AS fecha,
            (SELECT AVG(valor) FROM seleccionados s) AS valor,
			(SELECT MAX(valor) FROM seleccionados s) AS max_abs,
			(SELECT MIN(valor) FROM seleccionados s) AS min_abs,
            (SELECT COUNT(s.valor)::decimal/(SELECT nde.ndatos FROM numero_datos_esperado nde) * 100
                FROM seleccionados s WHERE s.valor IS NOT NULL) AS completo_mediciones,
            FALSE AS usado_para_diario
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_mediciones >= 0)
        AS es_valido
        FROM calculo
    ),
    update_horario AS (
        UPDATE horario_temperaturaagua SET
            valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
            usado_para_diario = (SELECT c.usado_para_diario FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_horario AS (
        INSERT INTO horario_temperaturaagua(estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_horario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_HORARIO_validados AS (
        UPDATE validacion_temperaturaagua SET usado_para_horario = TRUE
        WHERE id = ANY(ARRAY(SELECT vs.id FROM validados vs))
        AND (EXISTS (SELECT 1 FROM update_horario) OR EXISTS (SELECT 1 FROM insert_horario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE
            WHEN EXISTS (SELECT id FROM update_USADO_PARA_HORARIO_validados) THEN TRUE
            ELSE FALSE
            END) AS resultado
    )
    SELECT r.resultado INTO _resultado FROM resultado r;
    return _resultado;
END
$BODY$  LANGUAGE plpgsql;


-- ******************************************************* -- -
-- funcion para caudal

DROP FUNCTION IF EXISTS generar_horario_caudal();
CREATE OR REPLACE FUNCTION generar_horario_caudal()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN
    WITH
    dato AS (
        SELECT id, estacion_id, fecha FROM validacion_caudal v
        WHERE v.usado_para_horario = FALSE
        LIMIT 1
    ),
    hora_inicio AS (
        SELECT date_trunc('hour', (SELECT d.fecha FROM dato d)) AS hora_inicio
    ),
    hora_fin AS (
        SELECT (SELECT hi.hora_inicio FROM hora_inicio hi) + interval '1 hour' AS hora_fin
    ),
    numero_datos_esperado AS (
        SELECT CAST(60/f.fre_valor AS INT) ndatos
        FROM frecuencia_frecuencia f
        WHERE f.est_id_id = (SELECT d.estacion_id FROM dato d) AND f.var_id_id = 10
            AND f.fre_fecha_ini <= (SELECT d.fecha FROM dato d)
            AND (f.fre_fecha_fin >= (SELECT d.fecha FROM dato d) OR f.fre_fecha_fin IS NULL)
        ORDER BY f.fre_fecha_ini DESC LIMIT 1
    ),
    validados AS(
        SELECT id, estacion_id, fecha, valor, validacion FROM validacion_caudal v
        WHERE estacion_id = (SELECT d.estacion_id FROM dato d)
            AND fecha >= (SELECT hora_inicio FROM hora_inicio) AND fecha < (SELECT hora_fin FROM hora_fin)
    ),
    seleccionados AS (
        SELECT v.fecha, v.valor FROM (
            SELECT fecha, MAX(validacion) AS validacion FROM validados v GROUP BY fecha
        ) AS tbl_max
        INNER JOIN validados v
        ON v.fecha = tbl_max.fecha AND v.validacion = tbl_max.validacion
    ),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT h.hora_inicio FROM hora_inicio h) AS fecha,
            (SELECT AVG(valor) FROM seleccionados s) AS valor,
			(SELECT MAX(valor) FROM seleccionados s) AS max_abs,
			(SELECT MIN(valor) FROM seleccionados s) AS min_abs,
            (SELECT COUNT(s.valor)::decimal/(SELECT nde.ndatos FROM numero_datos_esperado nde) * 100
                FROM seleccionados s WHERE s.valor IS NOT NULL) AS completo_mediciones,
            FALSE AS usado_para_diario
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_mediciones >= 0)
        AS es_valido
        FROM calculo
    ),
    update_horario AS (
        UPDATE horario_caudal SET
            valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
            usado_para_diario = (SELECT c.usado_para_diario FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_horario AS (
        INSERT INTO horario_caudal(estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_horario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_HORARIO_validados AS (
        UPDATE validacion_caudal SET usado_para_horario = TRUE
        WHERE id = ANY(ARRAY(SELECT vs.id FROM validados vs))
        AND (EXISTS (SELECT 1 FROM update_horario) OR EXISTS (SELECT 1 FROM insert_horario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE
            WHEN EXISTS (SELECT id FROM update_USADO_PARA_HORARIO_validados) THEN TRUE
            ELSE FALSE
            END) AS resultado
    )
    SELECT r.resultado INTO _resultado FROM resultado r;
    return _resultado;
END
$BODY$  LANGUAGE plpgsql;


-- ******************************************************* -- -
-- funcion para Nivel de agua

DROP FUNCTION IF EXISTS generar_horario_nivelagua();
CREATE OR REPLACE FUNCTION generar_horario_nivelagua()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN
    WITH
    dato AS (
        SELECT id, estacion_id, fecha FROM validacion_nivelagua v
        WHERE v.usado_para_horario = FALSE
        LIMIT 1
    ),
    hora_inicio AS (
        SELECT date_trunc('hour', (SELECT d.fecha FROM dato d)) AS hora_inicio
    ),
    hora_fin AS (
        SELECT (SELECT hi.hora_inicio FROM hora_inicio hi) + interval '1 hour' AS hora_fin
    ),
    numero_datos_esperado AS (
        SELECT CAST(60/f.fre_valor AS INT) ndatos
        FROM frecuencia_frecuencia f
        WHERE f.est_id_id = (SELECT d.estacion_id FROM dato d) AND f.var_id_id = 10
            AND f.fre_fecha_ini <= (SELECT d.fecha FROM dato d)
            AND (f.fre_fecha_fin >= (SELECT d.fecha FROM dato d) OR f.fre_fecha_fin IS NULL)
        ORDER BY f.fre_fecha_ini DESC LIMIT 1
    ),
    validados AS(
        SELECT id, estacion_id, fecha, valor, validacion FROM validacion_nivelagua v
        WHERE estacion_id = (SELECT d.estacion_id FROM dato d)
            AND fecha >= (SELECT hora_inicio FROM hora_inicio) AND fecha < (SELECT hora_fin FROM hora_fin)
    ),
    seleccionados AS (
        SELECT v.fecha, v.valor FROM (
            SELECT fecha, MAX(validacion) AS validacion FROM validados v GROUP BY fecha
        ) AS tbl_max
        INNER JOIN validados v
        ON v.fecha = tbl_max.fecha AND v.validacion = tbl_max.validacion
    ),
    calculo AS (
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT h.hora_inicio FROM hora_inicio h) AS fecha,
            (SELECT AVG(valor) FROM seleccionados s) AS valor,
			(SELECT MAX(valor) FROM seleccionados s) AS max_abs,
			(SELECT MIN(valor) FROM seleccionados s) AS min_abs,
            (SELECT COUNT(s.valor)::decimal/(SELECT nde.ndatos FROM numero_datos_esperado nde) * 100
                FROM seleccionados s WHERE s.valor IS NOT NULL) AS completo_mediciones,
            FALSE AS usado_para_diario
    ),
    es_valido AS (
        SELECT
        (estacion_id IS NOT NULL) AND (fecha IS NOT NULL) AND (completo_mediciones >= 0)
        AS es_valido
        FROM calculo
    ),
    update_horario AS (
        UPDATE horario_nivelagua SET
            valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
            usado_para_diario = (SELECT c.usado_para_diario FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_horario AS (
        INSERT INTO horario_nivelagua(estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, completo_mediciones, usado_para_diario FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_horario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_HORARIO_validados AS (
        UPDATE validacion_nivelagua SET usado_para_horario = TRUE
        WHERE id = ANY(ARRAY(SELECT vs.id FROM validados vs))
        AND (EXISTS (SELECT 1 FROM update_horario) OR EXISTS (SELECT 1 FROM insert_horario))
        RETURNING *
    ),
    resultado AS (
        SELECT (CASE
            WHEN EXISTS (SELECT id FROM update_USADO_PARA_HORARIO_validados) THEN TRUE
            ELSE FALSE
            END) AS resultado
    )
    SELECT r.resultado INTO _resultado FROM resultado r;
    return _resultado;
END
$BODY$  LANGUAGE plpgsql;
