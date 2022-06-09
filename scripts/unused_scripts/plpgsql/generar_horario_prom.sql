DROP FUNCTION IF EXISTS generar_horario_var2();
CREATE OR REPLACE FUNCTION generar_horario_var2()
  RETURNS boolean AS
$BODY$
DECLARE _resultado boolean;
BEGIN
    WITH
    dato AS (
        SELECT id, estacion_id, fecha FROM validacion_var2validado v
        WHERE v.usado_para_horario = FALSE LIMIT 1
    ),
    hora_inicio AS (
        -- Calcula la hora inicial que deberá tener el bloque
        SELECT date_trunc('hour', (SELECT d.fecha FROM dato d)) AS hora_inicio
    ),
    hora_fin AS (
        -- Calcula la hora final que deberá tener el bloque
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
        -- selecciona el bloque de datos validados
        SELECT id, estacion_id, fecha, valor FROM validacion_var2validado v
        WHERE estacion_id = (SELECT d.estacion_id FROM dato d)
            AND fecha >= (SELECT hora_inicio FROM hora_inicio) AND fecha < (SELECT hora_fin FROM hora_fin)
    ),
    calculo AS (
        -- Calcula el promedio del valor de todo el bloque de validados
        SELECT
            (SELECT d.estacion_id FROM dato d) AS estacion_id,
            (SELECT h.hora_inicio FROM hora_inicio h) AS fecha,
            (SELECT AVG(v.valor) FROM validados v) AS valor,
			(SELECT MAX(v.valor) FROM validados v) AS max_abs,
			(SELECT MIN(v.valor) FROM validados v) AS min_abs,
            (SELECT 100.0 - (COUNT(v.valor)::decimal/(SELECT nde.ndatos FROM numero_datos_esperado nde) * 100)
                FROM validados v WHERE v.valor IS NOT NULL) AS vacios,
            FALSE AS usado_para_diario
    ),
    es_valido AS (
        SELECT
            (fecha IS NOT NULL) AND (vacios <= 100.0) AND (vacios >= 0.0)
        AS es_valido
        FROM calculo
    ),
    update_horario AS (
        -- Primera opción es actualizar el dato horario en caso de que ya hubiese existido
        UPDATE horario_var2horario SET
            valor = (SELECT c.valor FROM calculo c),
			max_abs = (SELECT c.max_abs FROM calculo c),
			min_abs = (SELECT c.min_abs FROM calculo c),
            vacios = (SELECT c.vacios FROM calculo c),
            usado_para_diario = (SELECT c.usado_para_diario FROM calculo c)
        WHERE estacion_id = (SELECT c.estacion_id FROM calculo c) AND fecha = (SELECT c.fecha FROM calculo c)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    insert_horario AS (
        -- En caso de que no haya existido el dato horario, entonces se lo inserta
        INSERT INTO horario_var2horario(estacion_id, fecha, valor, max_abs, min_abs, vacios, usado_para_diario)
        SELECT estacion_id, fecha, valor, max_abs, min_abs, vacios, usado_para_diario FROM calculo
        WHERE NOT EXISTS (SELECT 1 FROM update_horario)
        AND (SELECT es_valido FROM es_valido)
        RETURNING *
    ),
    update_USADO_PARA_HORARIO_validados AS (
        -- Se actualiza el campo USADO_PARA_HORARIO de los validados
        UPDATE validacion_var2validado SET usado_para_horario = TRUE
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

