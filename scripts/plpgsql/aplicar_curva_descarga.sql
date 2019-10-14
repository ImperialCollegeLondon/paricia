-- Esta proceso se puede desencadenar luego de la validación

CREATE OR REPLACE FUNCTION curva_descarga() RETURNS trigger
LANGUAGE plpgsql
AS $$
    DECLARE
        v_funcion           medicion_curvadescarga.funcion%TYPE;
        resultado           validacion_var10validado.valor%TYPE;
        ultima_validacion   validacion_var10validado.validacion%TYPE := NULL;
        ultimo_valor        validacion_var10validado.valor%TYPE;
    BEGIN
        SELECT funcion INTO  v_funcion FROM public.medicion_curvadescarga curvadescarga
            WHERE curvadescarga.estacion_id = new.estacion_id  AND curvadescarga.fecha <= new.fecha
            ORDER BY curvadescarga.fecha DESC
            LIMIT 1;
        IF NOT FOUND THEN
            RETURN NULL;
        END IF;
        IF v_funcion IS NULL THEN
            RETURN NULL;
        END IF;
        BEGIN
            EXECUTE 'SELECT ' || replace(v_funcion, 'H', CAST(new.valor AS VarChar) ) || ';' INTO resultado;
            EXCEPTION WHEN OTHERS THEN
                RETURN NULL;
        END;
        IF resultado IS NULL THEN
            RETURN NULL;
        END IF;

        -- Ahora obtener el maximo valor de validacion
		SELECT val.validacion, val.valor INTO ultima_validacion, ultimo_valor
  			FROM validacion_var10validado val
  			WHERE val.estacion_id = new.estacion_id AND val.fecha = new.fecha
			ORDER BY val.validacion DESC LIMIT 1;

  		IF ultima_validacion IS NULL THEN
  			ultima_validacion := 0;
  		ELSE
  			ultima_validacion := ultima_validacion + 1;
  		END IF;

  		IF resultado = ultimo_valor THEN
  		    RETURN NULL;
  		END IF;


        INSERT INTO public.validacion_var10validado
            (estacion_id, fecha, valor, usado_para_horario, validacion)
            values(new.estacion_id, new.fecha, resultado, FALSE, ultima_validacion);
        RETURN NULL;
    END;
$$;



DROP TRIGGER IF EXISTS nivelagua_insert on public.validacion_var11validado;
CREATE TRIGGER nivelagua_insert
    AFTER INSERT ON public.validacion_var11validado
    FOR EACH ROW EXECUTE PROCEDURE public.curva_descarga();