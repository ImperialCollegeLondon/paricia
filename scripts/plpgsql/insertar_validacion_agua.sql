-- FUNCTION: public.insertar_agua_validacion(bigint, json)

--DROP FUNCTION public.insertar_agua_validacion(bigint, json);

CREATE OR REPLACE FUNCTION public.insertar_agua_validacion(
	_estacion_id bigint,
	_datos json)
    RETURNS boolean
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE
AS $BODY$

DECLARE
	curs_datos CURSOR FOR
		SELECT * FROM json_populate_recordset( null::type_validacion_agua, _datos) t1;

	id_insertado_agua       validacion_agua.id%TYPE;
	nivel numeric;
	caudal numeric;
BEGIN
    FOR row_datos in curs_datos LOOP
        IF row_datos.estado is TRUE THEN
            nivel = row_datos.nivel;
            caudal = row_datos.caudal;

        ELSE
            nivel = NULL;
            caudal = NULL;

        END IF;
        IF row_datos.seleccionado is TRUE THEN

            INSERT INTO validacion_agua(estacion_id, fecha, nivel, caudal, usado_para_horario)
                VALUES (_estacion_id, row_datos.fecha, nivel, caudal,  FALSE)
                RETURNING id INTO id_insertado_agua;

            IF row_datos.comentario IS NOT NULL THEN
                INSERT INTO validacion_comentariovalidacion(variable_id, estacion_id, validado_id, comentario)
                    VALUES (11, _estacion_id, id_insertado_agua, row_datos.comentario);
            END IF;

        END IF;

    END LOOP;

	RETURN TRUE;
END

$BODY$;

ALTER FUNCTION public.insertar_agua_validacion(bigint, json)
    OWNER TO usuario1;
