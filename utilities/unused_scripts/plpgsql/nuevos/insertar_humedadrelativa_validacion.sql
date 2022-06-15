-- FUNCTION: public.insertar_humedadrelativa_validacion(bigint, json)

-- DROP FUNCTION public.insertar_humedadrelativa_validacion(bigint, json);

CREATE OR REPLACE FUNCTION public.insertar_humedadrelativa_validacion(
	_estacion_id bigint,
	_datos json)
    RETURNS boolean
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    
AS $BODY$

DECLARE
	curs_datos CURSOR FOR
		SELECT * FROM json_populate_recordset( null::validacion_pro, _datos) t1;

	id_insertado       validacion_var3validado.id%TYPE;
	valor numeric;
	maximo  numeric;
	minimo numeric;
BEGIN
    FOR row_datos in curs_datos LOOP
        IF row_datos.estado is TRUE THEN
            valor = row_datos.valor;
            IF row_datos.maximo is NULL THEN maximo = row_datos.valor; ELSE maximo = row_datos.maximo; END IF;
            IF row_datos.minimo is NULL THEN minimo = row_datos.valor; ELSE minimo = row_datos.minimo; END IF;
        ELSE
            valor = NULL;
            maximo = NULL;
            minimo = NULL;

        END IF;

        IF row_datos.seleccionado is TRUE THEN
            INSERT INTO validacion_var3validado(estacion_id, fecha, valor, maximo, minimo, usado_para_horario, validacion)
                VALUES (_estacion_id, row_datos.fecha, valor, maximo, minimo, FALSE, 0)
                RETURNING id INTO id_insertado;

            IF row_datos.comentario IS NOT NULL THEN
                INSERT INTO validacion_comentariovalidacion(variable_id, estacion_id, validado_id, comentario)
                    VALUES (3, _estacion_id, id_insertado, row_datos.comentario);
            END IF;
        END IF;

    END LOOP;

	RETURN TRUE;
END

$BODY$;

-- ALTER FUNCTION public.insertar_humedadrelativa_validacion(bigint, json)
--    OWNER TO usuario1;
