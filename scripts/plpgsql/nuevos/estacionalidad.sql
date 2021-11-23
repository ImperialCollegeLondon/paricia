-- FUNCTION: public.estacionalidad(integer, date, date)

-- DROP FUNCTION public.estacionalidad(integer, date, date);

CREATE OR REPLACE FUNCTION public.estacionalidad(
	estacionid integer,
	fecha1 date,
	fecha2 date)
    RETURNS numeric
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    
AS $BODY$
DECLARE
	sum1 decimal;
	div1 decimal;
	sum2 decimal;
	SI decimal;
	INDX decimal; --valor del indice de estacionalidad
BEGIN
	sum2 :=0;
	SI :=0;
	execute 'select count(mp.estacion_id),sum(mp.valor) as sum1 from public.mensual_var1mensual mp 
	where mp.estacion_id = $1
			and mp.fecha >= $2 and mp.fecha <= $3 and mp.valor IS NOT NULL group by mp.estacion_id' 
			into SI,sum1 using estacionid, fecha1, fecha2;
	/*sum1 := (select count(mp.estacion_id),sum(mp.valor) as sum1 from public.mensual_var1mensual mp where mp.estacion_id = estacionid
			and mp.fecha >= fecha1 and mp.fecha <= fecha2 and mp.valor IS NOT NULL group by mp.estacion_id );*/
	raise notice 'valor de sum1 = % , SI= %', sum1, SI;
	if sum1 = 0 or SI < 11 then
		return null;
	end if;
	
	div1 := sum1/12;
	sum2 := (select SUM(ABS(mp.valor - div1)) as sum2 from public.mensual_var1mensual mp where mp.estacion_id = estacionid
			and mp.fecha >= fecha1 and mp.fecha <= fecha2 and mp.valor IS NOT NULL group by mp.estacion_id );
	--raise notice 'valor de sum1 = % , div1 = %, sum2 = %', sum1, div1 ,sum2;
	SI := sum2/sum1;
	INDX := SI*6/11;
	--raise notice 'valor de SI = % , INDX = %', SI, INDX;
	RETURN INDX;
END;
$BODY$;

-- ALTER FUNCTION public.estacionalidad(integer, date, date)
--    OWNER TO usuario1;
