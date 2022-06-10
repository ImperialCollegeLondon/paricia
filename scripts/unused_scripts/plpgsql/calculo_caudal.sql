-- Esta funcion calcula/recalcula CAUDAL a partir de los datos de NIVEL DE AGUA y la curva de descarga
-- Este cálculo se hace para datos validados y para medicion (crudos)

-- Se calcula SOLO el segmento de tiempo que pertenece esa curva de descarga. El segmento de tiempo viene especificado
--      por la fecha que se da en el parámetro.

-- Importante se debe usar la función "eval_math(txt)" que está definida en "aplicar_curva_descarga.sql"


DROP FUNCTION if exists  calcular_caudal(INT);

CREATE OR REPLACE FUNCTION calcular_caudal(_curvadescarga_id INT) RETURNS VOID
LANGUAGE plpgsql
AS $$
DECLARE
    DECLARE
        _estacion_id   medicion_curvadescarga.estacion_id%TYPE;
        _fecha_ini   medicion_curvadescarga.fecha%TYPE;
        _fecha_fin   medicion_curvadescarga.fecha%TYPE;
        _ultima_funcion medicion_nivelfuncion.funcion%TYPE;
BEGIN

    SELECT cd.estacion_id, cd.fecha INTO _estacion_id, _fecha_ini
        FROM public.medicion_curvadescarga cd WHERE cd.id = _curvadescarga_id;

    -- Límite de fechas
    SELECT cd.fecha, LEAD(fecha) OVER( ORDER by cd.fecha) INTO _fecha_ini, _fecha_fin
        FROM medicion_curvadescarga cd
        WHERE cd.estacion_id = _estacion_id AND cd.fecha >= _fecha_ini ORDER BY cd.fecha;

    -- -- -- MEDICION (CRUDOS)
    -- Eliminando datos anteriores: NIVEL DE AGUA - CRUDOS
    DELETE FROM medicion_var10medicion m10
        WHERE m10.estacion_id = _estacion_id AND m10.fecha >= _fecha_ini
        AND (CASE WHEN _fecha_fin IS NOT NULL THEN m10.fecha < _fecha_fin ELSE TRUE END);

    -- Comprobar si al menos hay una función
    SELECT nv.funcion INTO _ultima_funcion FROM medicion_nivelfuncion nv
        WHERE nv.curvadescarga_id = _curvadescarga_id ORDER BY nv.nivel DESC LIMIT 1;
    IF NOT FOUND THEN RETURN; END IF;


    -- Calculando CAUDAL e insertando datos crudos
    WITH nivelfuncion AS (
	    SELECT  nv.nivel AS nivel, nv.funcion AS funcion FROM medicion_nivelfuncion nv
        WHERE nv.curvadescarga_id = _curvadescarga_id
		UNION
		SELECT 9999 AS nivel, (SELECT _ultima_funcion) AS funcion
		ORDER BY nivel ASC
    ),
    origen AS (
        SELECT *,
        (SELECT nf.funcion FROM nivelfuncion nf WHERE nf.nivel > m11.valor ORDER BY nf.nivel LIMIT 1) AS funcion
        FROM medicion_var11medicion m11
        WHERE m11.estacion_id = _estacion_id AND m11.fecha >= _fecha_ini
            AND (CASE WHEN _fecha_fin IS NOT NULL THEN m11.fecha < _fecha_fin ELSE TRUE END)
    ),
    calculos AS (
        SELECT oo.fecha,
        (SELECT eval_math(replace(oo.funcion, 'H', CAST(oo.valor AS VarChar) ))) AS valor
        FROM origen oo
    )
    INSERT INTO medicion_var10medicion(estacion_id, fecha, valor)
        SELECT _estacion_id, cc.fecha, cc.valor FROM calculos cc;


    -- VALIDADOS
    -- Eliminando datos anteriores: NIVEL DE AGUA - VALIDADOS
    DELETE FROM validacion_var10validado v10
        WHERE v10.estacion_id = _estacion_id AND v10.fecha >= _fecha_ini
        AND (CASE WHEN _fecha_fin IS NOT NULL THEN v10.fecha < _fecha_fin ELSE TRUE END);

    -- Calculando CAUDAL e insertando datos VALIDADOS
    WITH nivelfuncion AS (
	    SELECT  nv.nivel AS nivel, nv.funcion AS funcion FROM medicion_nivelfuncion nv
        WHERE nv.curvadescarga_id = _curvadescarga_id
		UNION
		SELECT 9999 AS nivel, (SELECT _ultima_funcion) AS funcion
		ORDER BY nivel ASC
    ),
    origen AS (
        SELECT *,
        (SELECT nf.funcion FROM nivelfuncion nf WHERE nf.nivel > v11.valor ORDER BY nf.nivel LIMIT 1) AS funcion
        FROM validacion_var11validado v11
        WHERE v11.estacion_id = _estacion_id AND v11.fecha >= _fecha_ini
            AND (CASE WHEN _fecha_fin IS NOT NULL THEN v11.fecha < _fecha_fin ELSE TRUE END)
    ),
    calculos AS (
        SELECT oo.fecha,
        (SELECT eval_math(replace(oo.funcion, 'H', CAST(oo.valor AS VarChar) ))) AS valor
        FROM origen oo
    )
    INSERT INTO validacion_var10validado(estacion_id, fecha, valor, usado_para_horario, validacion)
        SELECT _estacion_id, cc.fecha, cc.valor, False, 0 FROM calculos cc;

END;
$$;


------------------------------
------------------------------
