CREATE OR REPLACE FUNCTION curva_descarga() RETURNS trigger

LANGUAGE plpgsql
AS $$
    DECLARE

        v_funcion   medicion_curvadescarga.funcion%TYPE;
        resultado   medicion_nivelagua.valor%TYPE;

    BEGIN
        SELECT funcion INTO  v_funcion
        FROM public.medicion_curvadescarga curvadescarga
        WHERE curvadescarga.estacion_id = new.estacion
        AND curvadescarga.fecha <= new.fecha
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

        INSERT INTO public.medicion_caudal(estacion, fecha, valor)
                values(new.estacion, new.fecha, resultado);
            RETURN NULL;
    END;
$$;

DROP TRIGGER IF EXISTS caudal_insert on public.medicion_nivelagua;
CREATE TRIGGER caudal_insert
    AFTER INSERT ON public.medicion_nivelagua
    FOR EACH ROW EXECUTE PROCEDURE public.curva_descarga();