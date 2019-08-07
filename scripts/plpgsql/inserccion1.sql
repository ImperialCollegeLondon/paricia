
DROP FUNCTION IF EXISTS insertar_%%var_id%%validacion(bigint, json);
CREATE OR REPLACE FUNCTION insertar_%%var_id%%validacion(_estacion_id bigint, _datos json)
  RETURNS BOOLEAN AS
$BODY$
DECLARE
	curs_datos CURSOR FOR
		SELECT * FROM json_populate_recordset( null::validacion, _datos) t1;

	ultimo_validacion   integer;
	ultimo_valor        numeric;
	id_insertado       validacion_var%%var_id%%validado.id%TYPE;
BEGIN
    FOR row_datos in curs_datos LOOP
        ultimo_validacion := NULL;
		SELECT val.validacion, val.valor INTO ultimo_validacion, ultimo_valor
  			FROM validacion_var%%var_id%%validado val
  			WHERE val.estacion_id = _estacion_id AND val.fecha = row_datos.fecha
			ORDER BY val.validacion DESC LIMIT 1;

  		IF ultimo_validacion IS NULL THEN
  			ultimo_validacion := 0;
  		ELSE
  			ultimo_validacion := ultimo_validacion + 1;
            IF (row_datos.valor IS NULL) AND (ultimo_valor IS NULL) THEN CONTINUE; END IF;
		    IF row_datos.valor = ultimo_valor THEN CONTINUE; END IF;
  		END IF;

		INSERT INTO validacion_var%%var_id%%validado(estacion_id, fecha, valor, usado_para_horario, validacion)
			VALUES (_estacion_id, row_datos.fecha, row_datos.valor, FALSE, ultimo_validacion)
			RETURNING id INTO id_insertado;

		IF row_datos.comentario IS NOT NULL THEN
			INSERT INTO validacion_comentariovalidacion(variable_id, estacion_id, validado_id, comentario)
				VALUES (%%var_id%%, _estacion_id, id_insertado, row_datos.comentario);
		END IF;

    END LOOP;

	RETURN TRUE;
END
$BODY$  LANGUAGE plpgsql