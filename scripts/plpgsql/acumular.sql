-- FUNCTION: public.acumular(integer, timestamp without time zone, timestamp without time zone, integer)

-- DROP FUNCTION public.acumular(integer, timestamp without time zone, timestamp without time zone, integer);

CREATE OR REPLACE FUNCTION public.acumular(
	estacionid integer,
	fecha1 timestamp without time zone,
	fecha2 timestamp without time zone,
	frec integer)
    RETURNS character varying
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    
AS $BODY$
DECLARE
	mensajeret varchar(100) ='vacio';
	maximo NUMERIC; --valor maximo encontrado en la acumulacion
	mxtem NUMERIC; -- valor maximo temporal
	fechaMax timestamp; -- trunca a la fecha maxima de consulta
	fechtem1 timestamp; -- fecha inicial temporal
	fechtem2 timestamp; -- fecha final temporal
	per record;
	frecuen record;
	v_tiempo timestamp with time zone; --variable para medir el timepo de ejecucion
	counta integer;
BEGIN
	
/*Solo se controlaran para frecuencias de  5 10 y 15 minutos para estacioens estaciones automaticas*/
	maximo = 0;
	--fechaMax = fecha1 + ( anios || ' year')::interval;
	fechaMax = fecha1 + interval '1 years';
	raise notice 'fecha máxima permitida para el calculo %', fechaMax;
	if fecha2 > fechaMax then -- controla que la fecha maxima de consultasea un año
		fecha2 = fechaMax - interval '1 years';
		raise notice 'fecha2 nueva %', fecha2;
	end if;
		
	execute 'select count(*) from validacion_var1validado where estacion_id = $1 and fecha >= $2 and fecha <= $3;' into counta using estacionid, fecha1,fecha2;
	if counta > 360 then
		execute 'Select fre_valor, fre_fecha_ini from frecuencia_frecuencia where est_id_id = 1  and var_id_id = 1 
		 and fre_fecha_ini <= $2 order by fre_fecha_ini desc limit 1;' 
		into frecuen using estacionid, fecha2, frec;
		/*compara si las frecuencias dentro del periodo de fechas existen para ejecutar
		sin no es es asi cambiar la frecuencia del periodo de inico y la de fin segun las frecuencias */
		raise notice 'valor de f %',frecuen.fre_valor;
		if frecuen.fre_valor <= frec then	
			if frecuen.fre_valor = 5 and frec = 5 then -- para frecuencias de 5 minutos
				execute 'select max(valor) from validacion_var1validado 
				where estacion_id = $1 and fecha >= $2 and fecha <= $3' into maximo using  estacionid, fecha1,fecha2; 
				execute 'select fecha from validacion_var1validado 
				where estacion_id = $1 and fecha >= $2 and fecha <= $3 and valor = $4 limit 1' into fechaMax using  estacionid, fecha1,fecha2,maximo; 
				raise notice 'maximo para 5 minutos % : %',maximo, fechaMax;
				mensajeret = fechaMax||';'||maximo||';'||'valor maximo cada 5 minutos';
				return mensajeret;
			else -- si la frecunacia es menor a 5 minutos por ejemplo 1 minuto
				fechtem1 = fecha1;
				maximo = -1;
				counta = 0;
				fecha1 = fecha1 + '5 minutes';
				for per in SELECT * FROM generate_series(fecha1, fecha2, '5 minutes')
				loop
					fechtem2 = fechtem1 + (frec||' minutes')::interval;
					execute 'select sum(valor) from validacion_var1validado where estacion_id = $1 and fecha >= $2 and fecha < $3' 
					into mxtem using estacionid, fechtem1, fechtem2;
					if(mxtem > maximo) then
						maximo = mxtem;
						fechaMax = per;
						--raise notice ' %', mxtem;
						--raise notice 'select max(valor) from validacion_var1validado where estacion_id = % and fecha >= % and fecha < %',estacionid, fechtem1, fechtem2;
					end if;
					--raise notice ' %', mxtem;
					--raise notice 'select sum(valor) from validacion_var1validado where estacion_id = % and fecha >= % and fecha < %',estacionid, fechtem1, fechtem2;
					fechtem1 = per ;
					--EXIT WHEN counta > 200;
					--counta = counta + 1;
				end loop;
				raise notice 'maximo para % minutos % : %',frec,maximo, fechaMax;
				mensajeret = fechaMax||';'||maximo||';'||'valor maximo cada '||frec||' minutos';
				return mensajeret;
			end if;	

		else
			raise notice 'null;-10;No existe una frecuencia para  % minutos', frec;
			mensajeret = 'null;-10;No existe una frecuencia para '||frec||' minutos';
			return mensajeret;
		end if;
	else 
		raise notice 'null;-10;No existen datos, frecunecia % minutos', frec;
		mensajeret = 'null;-10;No existen datos, frecunecia '||frec||' minutos';
		return mensajeret;
	end if;
	
END;
$BODY$;

-- ALTER FUNCTION public.acumular(integer, timestamp without time zone, timestamp without time zone, integer)
--    OWNER TO usuario1;
