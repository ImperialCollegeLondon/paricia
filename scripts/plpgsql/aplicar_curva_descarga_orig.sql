-- Esta proceso se puede desencadenar luego de la validación

CREATE OR REPLACE FUNCTION curva_descarga() RETURNS trigger
LANGUAGE plpgsql
AS $$
    DECLARE
        v_funcion   medicion_curvadescarga.funcion%TYPE;
        resultado   validacion_var10validado.valor%TYPE;
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
        INSERT INTO public.validacion_var10validado
            (estacion_id, fecha, valor, usado_para_horario, validacion)
            values(new.estacion_id, new.fecha, resultado, new.usado_para_horario, new.validacion);
        RETURN NULL;
    END;
$$;



DROP TRIGGER IF EXISTS nivelagua_insert on public.validacion_var11validado;
CREATE TRIGGER nivelagua_insert
    AFTER INSERT ON public.validacion_var11validado
    FOR EACH ROW EXECUTE PROCEDURE public.curva_descarga();