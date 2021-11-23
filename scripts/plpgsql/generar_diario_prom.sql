DROP FUNCTION IF EXISTS generar_diario_var2();
CREATE OR REPLACE FUNCTION generar_diario_var2()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN

    WITH
    dato AS (
        SELECT id, estacion_id, fecha FROM horario_var2horario h
        WHERE h.usado_para_diario = FALSE LIMIT 1
    ),
    dia_inicio AS (
        SELECT date_trunc('day', (SELECT d.fecha FROM dato d)) AS dia_inicio LIMIT 1
    ),
    dia_fin AS (
        SELECT (SELECT di.dia_inicio FROM dia_inicio di) + interval '1 day' AS dia_fin LIMIT 1
    ),
	bloque AS (
        SELECT id, estacion_id, fecha, valor, max_abs, min_abs, vacios
        FROM horario_var2horario h
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
            (SELECT 100.0 - (SUM(100.0-b.vacios)::decimal/24) FROM bloque b) AS vacios,
            FALSE AS usado_para_mensual
    ),
    es_valido AS (
        SELECT
           (fecha IS NOT NULL) AND (vacios >= 0.0) AND (vacios <= 100.0)
        AS es_valido
        FROM calculo
    ),
    update_diario AS (
        UPDATE diario_var2diario SET
			valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
			max_del_prom = (SELECT c.max_del_prom FROM calculo c),
			min_del_prom = (SELECT c.min_del_prom FROM calculo c),
            vacios = (SELECT c.vacios FROM calculo c),
            usado_para_mensual = (SELECT c.usado_para_mensual FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_diario AS (
        INSERT INTO diario_var2diario(estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom,
            vacios, usado_para_mensual)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, max_del_prom, min_del_prom,
            vacios, usado_para_mensual
        FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_diario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_DIARIO AS (
        UPDATE horario_var2horario SET usado_para_diario = TRUE
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