-- FUNCTION: public.insertar_precipitacion_validacion(bigint, json)

DROP FUNCTION IF EXISTS  public.insertar_precipitacion_validacion(bigint, json);

CREATE OR REPLACE FUNCTION public.insertar_precipitacion_validacion(
	_estacion_id bigint,
	_datos json)
    RETURNS boolean
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE
AS $BODY$

DECLARE
	curs_datos CURSOR FOR
		SELECT * FROM json_populate_recordset( null::validacion_acu, _datos) t1;

	id_insertado       validacion_var1validado.id%TYPE;
	valor numeric;
BEGIN
    FOR row_datos in curs_datos LOOP
        IF row_datos.estado is TRUE THEN valor = row_datos.valor; ELSE valor = NULL; END IF;

        IF row_datos.seleccionado is TRUE THEN
            INSERT INTO validacion_var1validado(estacion_id, fecha, valor, usado_para_horario)
                VALUES (_estacion_id, row_datos.fecha, valor, FALSE)
                RETURNING id INTO id_insertado;

            IF row_datos.comentario IS NOT NULL THEN
                INSERT INTO validacion_comentariovalidacion(variable_id, estacion_id, validado_id, comentario)
                    VALUES (1, _estacion_id, id_insertado, row_datos.comentario);
		    END IF;
		END IF;

    END LOOP;

	RETURN TRUE;
END

$BODY$;

--ALTER FUNCTION public.insertar_precipitacion_validacion(bigint, json)
--    OWNER TO usuario1;
