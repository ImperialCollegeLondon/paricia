-- FUNCTION: public.insertar_precipitacion_validacion(bigint, json)

--DROP FUNCTION public.insertar_viento_validacion(bigint, json);

CREATE OR REPLACE FUNCTION public.insertar_viento_validacion(
	_estacion_id bigint,
	_datos json)
    RETURNS boolean
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE
AS $BODY$

DECLARE
	curs_datos CURSOR FOR
		SELECT * FROM json_populate_recordset( null::type_validacion_viento, _datos) t1;

	id_insertado_viento       validacion_viento.id%TYPE;
	valor numeric;
	maximo  numeric;
	minimo numeric;
	direccion numeric;
	categoria numeric;
BEGIN
    FOR row_datos in curs_datos LOOP
        IF row_datos.estado is TRUE THEN
            valor = row_datos.valor;
            IF row_datos.maximo is NULL THEN maximo = row_datos.valor; ELSE maximo = row_datos.maximo; END IF;
            IF row_datos.minimo is NULL THEN minimo = row_datos.valor; ELSE minimo = row_datos.minimo; END IF;
            direccion = row_datos.direccion;
            categoria = row_datos.categoria;

        ELSE
            valor = NULL;
            maximo = NULL;
            minimo = NULL;
            direccion = NULL;
            categoria = NULL;

        END IF;
        IF row_datos.seleccionado is TRUE THEN

            INSERT INTO validacion_viento(estacion_id, fecha, valor, maximo, minimo, direccion, categoria, usado_para_horario)
                VALUES (_estacion_id, row_datos.fecha, valor, maximo, minimo, direccion, categoria, FALSE)
                RETURNING id INTO id_insertado_viento;

            INSERT INTO validacion_var5validado(estacion_id, fecha, valor, usado_para_horario, validacion, maximo, minimo)
			VALUES (_estacion_id, row_datos.fecha, direccion, FALSE, 0, maximo, minimo);

            INSERT INTO validacion_var4validado(estacion_id, fecha, valor, usado_para_horario, validacion, maximo, minimo)
			VALUES (_estacion_id, row_datos.fecha, valor, FALSE, 0, maximo, minimo);
            
            IF row_datos.comentario IS NOT NULL THEN
                INSERT INTO validacion_comentariovalidacion(variable_id, estacion_id, validado_id, comentario)
                    VALUES (4, _estacion_id, id_insertado_viento, row_datos.comentario);

            END IF;

        END IF;

    END LOOP;

	RETURN TRUE;
END

$BODY$;

--ALTER FUNCTION public.insertar_viento_validacion(bigint, json)
--    OWNER TO usuario1;
