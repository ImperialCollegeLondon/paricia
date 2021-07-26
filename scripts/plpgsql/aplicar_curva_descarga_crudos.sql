-- Esta funcion es para desencadenarse luego de inserccion a datos crudos

CREATE OR REPLACE FUNCTION curva_descarga_crudos() RETURNS trigger
LANGUAGE plpgsql
AS $$
    DECLARE
        curvdesc_id    medicion_curvadescarga.id%TYPE;
        v_funcion           medicion_nivelfuncion.funcion%TYPE;
        resultado           medicion_var10medicion.valor%TYPE;
        _ultima_funcion     medicion_nivelfuncion.funcion%TYPE;
    BEGIN
        -- Buscar curva de descarga para la estacíon y fecha correspondiente al dato
        SELECT id INTO curvdesc_id FROM public.medicion_curvadescarga cd
            WHERE cd.estacion_id = new.estacion_id  AND cd.fecha <= new.fecha
            ORDER BY cd.fecha DESC
            LIMIT 1;
        IF NOT FOUND THEN RETURN NULL; END IF;

        -- Verifica que al menos tenga una función, caso contrario sale
        SELECT nv.funcion INTO _ultima_funcion FROM medicion_nivelfuncion nv
            WHERE nv.curvadescarga_id = curvdesc_id ORDER BY nv.nivel DESC LIMIT 1;
        IF NOT FOUND THEN RETURN NULL; END IF;

        -- Seleccionar la función que corresponda al intervalo de nivel
        SELECT funcion INTO v_funcion from public.medicion_nivelfuncion nf
            WHERE nf.curvadescarga_id = curvdesc_id AND nf.nivel > new.valor
            ORDER BY nf.nivel ASC
            LIMIT 1;
        -- Si no está dentro de algún intervalo, entonces, por diseño tomar la última función
        IF NOT FOUND THEN
            SELECT funcion INTO v_funcion from public.medicion_nivelfuncion nf
                WHERE nf.curvadescarga_id = curvdesc_id
                ORDER BY nf.nivel DESC
                LIMIT 1;
        END IF;


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