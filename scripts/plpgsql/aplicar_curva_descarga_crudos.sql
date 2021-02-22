-- Esta funcion es para desencadenarse luego de inserccion a datos crudos

CREATE OR REPLACE FUNCTION curva_descarga_crudos() RETURNS trigger
LANGUAGE plpgsql
AS $$
    DECLARE
        v_funcion           medicion_curvadescarga.funcion%TYPE;
        resultado           medicion_var10medicion.valor%TYPE;
    BEGIN
        SELECT funcion INTO  v_funcion FROM public.medicion_curvadescarga curvadescarga
            WHERE curvadescarga.estacion_id = new.estacion_id  AND curvadescarga.fecha <= new.fecha
            ORDER BY curvadescarga.fecha DESC
            LIMIT 1;

        IF NOT FOUND THEN RETURN NULL; END IF;

        IF v_funcion IS NULL THEN RETURN NULL; END IF;

        BEGIN
            EXECUTE 'SELECT ' || replace(v_funcion, 'H', CAST(new.valor AS VarChar) ) || ';' INTO resultado;
            EXCEPTION WHEN OTHERS THEN
                RETURN NULL;
        END;

        IF resultado IS NULL THEN RETURN NULL; END IF;

        DELETE FROM medicion_var10medicion med WHERE med.estacion_id = new.estacion_id
        AND med.fecha >= (new.fecha - interval '30' second) AND med.fecha <= (new.fecha + interval '30' second);

        INSERT INTO public.medicion_var10medicion(estacion_id, fecha, valor)
            values(new.estacion_id, new.fecha, resultado);
        RETURN NULL;
    END;
$$;



DROP TRIGGER IF EXISTS nivelagua_insert_crudos on public.medicion_var11medicion;
CREATE TRIGGER nivelagua_insert_crudos
    AFTER INSERT ON public.medicion_var11medicion
    FOR EACH ROW EXECUTE PROCEDURE public.curva_descarga_crudos();