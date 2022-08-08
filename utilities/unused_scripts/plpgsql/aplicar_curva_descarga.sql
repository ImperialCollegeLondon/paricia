/*
Functions to

*/


CREATE OR REPLACE FUNCTION curva_descarga() RETURNS trigger
LANGUAGE plpgsql
AS $$
    DECLARE
        curvdesc_id         medicion_curvadescarga.id%TYPE;
        v_funcion           medicion_nivelfuncion.funcion%TYPE;
        resultado           validacion_var10validado.valor%TYPE;
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

        DELETE FROM validacion_var10validado val WHERE val.estacion_id = new.estacion_id
        AND val.fecha >= (new.fecha - interval '30' second) AND val.fecha <= (new.fecha + interval '30' second);

        INSERT INTO public.validacion_var10validado(estacion_id, fecha, valor, usado_para_horario, validacion)
            values(new.estacion_id, new.fecha, resultado, FALSE, 0);
        RETURN NULL;
    END;
$$;



DROP TRIGGER IF EXISTS nivelagua_insert on public.validacion_var11validado;
CREATE TRIGGER nivelagua_insert
    AFTER INSERT ON public.validacion_var11validado
    FOR EACH ROW EXECUTE PROCEDURE public.curva_descarga();



-------------------------------------------------------------------

DROP FUNCTION if exists eval_math(text);
create or replace function eval_math(expression text) returns numeric
as
$body$
declare
  result numeric;
begin

    BEGIN
        EXECUTE 'SELECT ' || expression || ';' INTO result;
        -- ALternativa: execute format('select %s', _s) into i;
        EXCEPTION WHEN OTHERS THEN
                    RETURN NULL;
    END;
    return result;
end;
$body$
language plpgsql