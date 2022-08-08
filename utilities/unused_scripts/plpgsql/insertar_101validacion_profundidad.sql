
DROP FUNCTION IF EXISTS insertar_101validacion(bigint, json);
CREATE OR REPLACE FUNCTION insertar_101validacion(_estacion_id bigint, _datos json)
  RETURNS BOOLEAN AS
$BODY$
DECLARE
	curs_datos CURSOR FOR
		SELECT * FROM json_populate_recordset(null::validacion_profundidad, _datos) t101 ORDER BY t101.fecha;
    row_datos        validacion_profundidad;
	inicio           validacion_profundidad;
	fin              validacion_profundidad;
	id_insertado        validacion_var101validado.id%TYPE;

BEGIN
    -- Obtener fecha de inicio y fin
    OPEN curs_datos;
        FETCH FIRST FROM curs_datos INTO inicio;
        FETCH LAST FROM curs_datos INTO fin;
    CLOSE curs_datos;

    -- Borrar todos los datos validados en el rango de fechas ingresado
    DELETE FROM validacion_var101validado
    WHERE estacion_id = _estacion_id AND profundidad = inicio.profundidad
	AND fecha >= inicio.fecha AND fecha <= fin.fecha;

    -- Iterar por cada nuevo dato para insertar
    FOR row_datos in curs_datos LOOP
		INSERT INTO validacion_var101validado(estacion_id, fecha, profundidad, valor, usado_para_horario)
			VALUES (_estacion_id, row_datos.fecha, row_datos.profundidad, row_datos.valor, FALSE)
			RETURNING id INTO id_insertado;

		IF row_datos.comentario IS NOT NULL THEN
			INSERT INTO validacion_comentariovalidacion(variable_id, estacion_id, validado_id, comentario)
				VALUES (101, _estacion_id, id_insertado, row_datos.comentario);
		END IF;
    END LOOP;

	RETURN TRUE;
END
$BODY$  LANGUAGE plpgsql;