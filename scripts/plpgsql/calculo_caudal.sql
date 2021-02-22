-- Esta funcion calcula/recalcula CAUDAL a partir de los datos de NIVEL DE AGUA y la curva de descarga
-- Este cálculo se hace para datos validados y para medicion (crudos)

-- Se calcula SOLO el segmento de tiempo que pertenece esa curva de descarga. El segmento de tiempo viene especificado
--      por la fecha que se da en el parámetro.



-------------------------------------------------------------------
-- Aplica SELECT a una cadena de texto
--      Se creó con el propósito de aplicar las funciones de curva de descarga en la función SQL "CALCULO CAUDAL"

CREATE OR REPLACE FUNCTION evaluar(_s text)
returns numeric as $$
declare i numeric;
begin
    execute format('select %s', _s) into i;
    return i;
end;
$$ language plpgsql;
-----------------------------------------------------------------------



CREATE OR REPLACE FUNCTION calculo_caudal(_estacion_id INT, _fecha TIMESTAMP WITH TIME ZONE) RETURNS VOID
LANGUAGE plpgsql
AS $$
DECLARE
	cursor_curvas CURSOR FOR
		SELECT
		cd.fecha AS fecha_ini, LEAD(cd.fecha) OVER (ORDER BY cd.fecha ASC) AS fecha_fin, cd.funcion AS funcion
		FROM medicion_curvadescarga cd
		WHERE cd.estacion_id = _estacion_id
		ORDER BY cd.fecha ASC;
BEGIN
	FOR curva in cursor_curvas LOOP
		IF _fecha < curva.fecha_ini THEN
			CONTINUE;
		END IF;

		IF curva.fecha_fin IS NOT NULL THEN
			IF _fecha >= curva.fecha_fin THEN
				CONTINUE;
			END IF;
		END IF;


        -- -- -- MEDICION
		-- Eliminando datos anteriores
		DELETE FROM medicion_var10medicion
		WHERE estacion_id = _estacion_id AND fecha >= curva.fecha_ini
			AND (CASE WHEN curva.fecha_fin IS NOT NULL THEN fecha < curva.fecha_fin ELSE TRUE END);

		-- Insertando
		WITH origen AS (
			SELECT *
			FROM medicion_var11medicion m11
			WHERE m11.estacion_id = _estacion_id AND m11.fecha >= curva.fecha_ini
				AND (CASE WHEN curva.fecha_fin IS NOT NULL THEN m11.fecha < curva.fecha_fin ELSE TRUE END)
		),
		calculos AS (
			SELECT oo.fecha,
			(SELECT evaluar(replace(curva.funcion, 'H', CAST(oo.valor AS VarChar) ))) AS valor
			FROM origen oo
		)
		INSERT INTO medicion_var10medicion(estacion_id, fecha, valor)
			SELECT _estacion_id, cc.fecha, cc.valor FROM calculos cc;


        -- -- -- VALIDADOS
		-- Eliminando datos anteriores
		DELETE FROM validacion_var10validado
		WHERE estacion_id = _estacion_id AND fecha >= curva.fecha_ini
			AND (CASE WHEN curva.fecha_fin IS NOT NULL THEN fecha < curva.fecha_fin ELSE TRUE END);

		-- Insertando
		WITH origen AS (
			SELECT *
			FROM validacion_var11validado v11
			WHERE v11.estacion_id = _estacion_id AND v11.fecha >= curva.fecha_ini
				AND (CASE WHEN curva.fecha_fin IS NOT NULL THEN v11.fecha < curva.fecha_fin ELSE TRUE END)
		),
		calculos AS (
			SELECT oo.fecha,
			(SELECT evaluar(replace(curva.funcion, 'H', CAST(oo.valor AS VarChar) ))) AS valor
			FROM origen oo
		)
		INSERT INTO validacion_var10validado(estacion_id, fecha, valor, usado_para_horario, validacion)
			SELECT _estacion_id, cc.fecha, cc.valor, FALSE, 0 FROM calculos cc;


	END LOOP;
END;
$$;



---------------------------

CREATE OR REPLACE FUNCTION public.trigger_calculo_caudal()
    RETURNS trigger
    LANGUAGE 'plpgsql'
AS $BODY$
BEGIN

    IF (TG_OP = 'DELETE') THEN
        PERFORM calculo_caudal(OLD.estacion_id::INT, OLD.fecha::TIMESTAMP WITH TIME ZONE);
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        PERFORM calculo_caudal(NEW.estacion_id::INT, NEW.fecha::TIMESTAMP WITH TIME ZONE);
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        PERFORM calculo_caudal(NEW.estacion_id::INT, NEW.fecha::TIMESTAMP WITH TIME ZONE);
        RETURN NEW;
    END IF;
    RETURN NULL;

END;
$BODY$;


DROP TRIGGER IF EXISTS calculo_caudal ON public.medicion_curvadescarga;

CREATE TRIGGER calculo_caudal
    AFTER INSERT OR UPDATE OR DELETE
    ON public.medicion_curvadescarga
    FOR EACH ROW
    EXECUTE PROCEDURE public.trigger_calculo_caudal();



------------------------------
------------------------------

--CREATE OR REPLACE FUNCTION public.trigger_calculo_caudal_ins_upd()
--    RETURNS trigger
--    LANGUAGE 'plpgsql'
--AS $BODY$
--BEGIN
--    PERFORM calculo_caudal(NEW.estacion_id::INT, NEW.fecha::TIMESTAMP WITH TIME ZONE);
--    RETURN NEW;
--END;
--$BODY$;
--
--
--DROP TRIGGER IF EXISTS calculo_caudal_ins_upd ON public.medicion_curvadescarga;
--
--CREATE TRIGGER calculo_caudal_ins_upd
--    AFTER INSERT OR UPDATE
--    ON public.medicion_curvadescarga
--    FOR EACH ROW
--    EXECUTE PROCEDURE public.trigger_calculo_caudal_ins_upd();
--
--
--
--
--
--CREATE OR REPLACE FUNCTION public.trigger_calculo_caudal_del()
--    RETURNS trigger
--    LANGUAGE 'plpgsql'
--AS $BODY$
--BEGIN
--    PERFORM calculo_caudal(OLD.estacion_id::INT, OLD.fecha::TIMESTAMP WITH TIME ZONE);
--    RETURN NEW;
--END;
--$BODY$;
--
--
--DROP TRIGGER IF EXISTS calculo_caudal_del ON public.medicion_curvadescarga;
--
--CREATE TRIGGER calculo_caudal_del
--    AFTER INSERT OR UPDATE
--    ON public.medicion_curvadescarga
--    FOR EACH ROW
--    EXECUTE PROCEDURE public.trigger_calculo_caudal_del();