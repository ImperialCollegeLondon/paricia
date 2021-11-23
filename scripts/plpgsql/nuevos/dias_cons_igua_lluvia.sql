-- FUNCTION: public.dias_cons_igua_lluvia(integer, date, date, numeric)

-- DROP FUNCTION public.dias_cons_igua_lluvia(integer, date, date, numeric);

CREATE OR REPLACE FUNCTION public.dias_cons_igua_lluvia(
	estacionid integer,
	fecha1 date,
	fecha2 date,
	valorc numeric)
    RETURNS integer
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    
AS $BODY$
DECLARE
	datos RECORD;
	con_e_cer integer; --contador de valores de cero
	con_e_cer_tmp integer; --caontador de ceros temporal
	mes_ver integer; -- verifica que existan los meses completos
BEGIN
	con_e_cer = 0;
	con_e_cer_tmp = 0;
	execute 'select count(mp.estacion_id) from public.mensual_var1mensual mp 
	where mp.estacion_id = $1 and mp.fecha >= $2 and mp.fecha <= $3 and mp.valor IS NOT NULL 
	group by mp.estacion_id' into mes_ver using estacionid, fecha1, fecha2;
	if mes_ver < 11 then
		return null;
	else
		for datos in select * from public.diario_var1diario dp where dp.estacion_id = estacionid 
		and dp.fecha >= fecha1 and dp.fecha<= fecha2 and dp.valor IS NOT NULL order by fecha asc loop
			IF datos.valor = valorc THEN
				con_e_cer = con_e_cer +1;
			ELSE 
				IF con_e_cer >= con_e_cer_tmp  THEN --COMPRUEBA QUE EL CONTEO SE MAYOR
					con_e_cer_tmp = con_e_cer;
				END IF;
				con_e_cer = 0;			
			END IF;
			--RAISE NOTICE 'dias sin lluvia %, dias con lluvia %',con_e_cer , con_gt_cer;
		end loop;	
		IF con_e_cer > 0 and con_e_cer >= con_e_cer_tmp THEN
			con_e_cer_tmp := con_e_cer;
		END IF;
	END IF;
	
	return con_e_cer_tmp ;
END;
$BODY$;

-- ALTER FUNCTION public.dias_cons_igua_lluvia(integer, date, date, numeric)
--    OWNER TO usuario1;
