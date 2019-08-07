DROP FUNCTION IF EXISTS generar_horario_precipitacion();
CREATE OR REPLACE FUNCTION generar_horario_precipitacion()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN
    WITH
    dato AS (
        SELECT * FROM validacion_precipitacion v
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
        WHERE f.est_id_id = (SELECT d.estacion_id FROM dato d) AND f.var_id_id = 1
            AND f.fre_fecha_ini <= (SELECT d.fecha FROM dato d)
            AND (f.fre_fecha_fin >= (SELECT d.fecha FROM dato d) OR f.fre_fecha_fin IS NULL)
        ORDER BY f.fre_fecha_ini DESC LIMIT 1
    ),
    validados AS(
        SELECT * FROM validacion_precipitacion v
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
            (SELECT SUM(valor) FROM seleccionados s WHERE s.valor IS NOT NULL) AS valor,
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
        UPDATE horario_precipitacion SET
            valor = (SELECT c.valor FROM calculo c),
            completo_mediciones = (SELECT c.completo_mediciones FROM calculo c),
            usado_para_diario = (SELECT c.usado_para_diario FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_horario AS (
        INSERT INTO horario_precipitacion(estacion_id, fecha, valor, completo_mediciones, usado_para_diario)
        SELECT estacion_id, fecha, valor, completo_mediciones, usado_para_diario FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_horario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_HORARIO_validados AS (
        UPDATE validacion_precipitacion SET usado_para_horario = TRUE
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

