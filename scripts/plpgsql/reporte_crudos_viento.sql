DROP FUNCTION IF EXISTS   public.reporte_crudos_viento(integer, timestamp with time zone, timestamp with time zone, numeric, numeric);


CREATE OR REPLACE FUNCTION public.reporte_crudos_viento(
	_estacion_id integer,
	_fecha_inicio timestamp with time zone,
	_fecha_fin timestamp with time zone,
	_var_maximo numeric,
	_var_minimo numeric)
    RETURNS TABLE(id bigint, fecha timestamp with time zone, valor numeric, maximo numeric, minimo numeric,
    direccion numeric, categoria numeric,
    estado boolean, seleccionado boolean,
    comentario character varying)
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE
    ROWS 1000
AS $BODY$

BEGIN
	RETURN QUERY
	
    WITH
	estacion AS (SELECT * FROM estacion_estacion est WHERE est.est_id = _estacion_id),
	variable AS (SELECT * FROM variable_variable var WHERE var.var_id = 4),
	--Seleccionar los datos de la tabla validados
    validacion AS (
        SELECT v.id, v.fecha, v.valor, v.maximo, v.minimo, v.direccion, v.categoria
        FROM validacion_viento v WHERE v.estacion_id = (SELECT est_id FROM estacion)
        AND date_trunc('day',v.fecha) >= _fecha_inicio AND date_trunc('day',v.fecha) <= _fecha_fin
    ),
    --Seleccionar los datos de la tabla medicion
    medicion AS (
        SELECT m_vvi.id, m_vvi.fecha,CASE WHEN m_vvi.valor = 'NaN' THEN NULL ELSE m_vvi.valor END,
        CASE WHEN m_vvi.maximo = 'NaN' THEN NULL ELSE m_vvi.maximo END,
        CASE WHEN m_vvi.minimo = 'NaN' THEN NULL ELSE m_vvi.minimo END,
        CASE WHEN m_dvi.valor = 'NaN' THEN NULL ELSE m_dvi.valor END as direccion,
        CASE WHEN m_dvi.valor IS NULL OR m_dvi.valor = 'NaN'::numeric THEN NULL ELSE
            CASE WHEN m_dvi.valor<= 22.5 OR m_dvi.valor> 337.5 THEN 1 ELSE
                CASE WHEN m_dvi.valor> 22.5 AND m_dvi.valor<= 67.5 THEN 2 ELSE
                    CASE WHEN m_dvi.valor> 67.5 AND m_dvi.valor<= 112.5 THEN 3 ELSE
                        CASE WHEN m_dvi.valor> 112.5 AND m_dvi.valor<= 157.5 THEN 4 ELSE
                            CASE WHEN m_dvi.valor> 157.5 AND m_dvi.valor<= 202.5 THEN 5 ELSE
                                CASE WHEN m_dvi.valor> 202.5 AND m_dvi.valor<= 247.5 THEN 6 ELSE
                                    CASE WHEN m_dvi.valor> 247.5 AND m_dvi.valor<= 292.5 THEN 7 ELSE
                                        CASE WHEN m_dvi.valor> 292.5 AND m_dvi.valor<= 337.5 THEN 8 ELSE NULL END
                                    END
                                END
                            END
                        END
                    END
                END
            END
        END AS categoria,

        EXISTS(SELECT * FROM validacion v WHERE v.fecha = m_vvi.fecha) AS existe_en_validacion

        FROM medicion_var4medicion m_vvi, medicion_var5medicion m_dvi
        WHERE m_vvi.estacion_id = (SELECT est_id FROM estacion)
        AND m_vvi.fecha = m_dvi.fecha and m_vvi.estacion_id = m_dvi.estacion_id
        AND date_trunc('day',m_vvi.fecha) >= _fecha_inicio AND date_trunc('day',m_vvi.fecha) <= _fecha_fin
        ORDER BY m_vvi.fecha


    ),
	tabla_base AS (
		SELECT
			m.fecha, m.valor, m.maximo, m.minimo, m.direccion, m.categoria

		FROM medicion m WHERE m.existe_en_validacion = FALSE
		GROUP BY m.fecha, m.valor, m.maximo, m.minimo, m.direccion, m.categoria
		HAVING COUNT(*)=1
	),
	reporte AS (
		SELECT row_number() OVER (ORDER BY ts.fecha ASC) as id, ts.fecha,
			CASE WHEN ts.valor> _var_maximo OR ts.valor < _var_minimo THEN NULL ELSE ts.valor END AS valor,
			CASE WHEN ts.maximo> _var_maximo OR ts.maximo < _var_minimo THEN NULL ELSE ts.maximo END AS maximo,
			CASE WHEN ts.minimo> _var_maximo OR ts.minimo < _var_minimo THEN NULL ELSE ts.minimo END AS minimo,
			ts.direccion, ts.categoria::numeric,
		    CASE WHEN ts.valor IS NULL OR ts.direccion IS NULL THEN FALSE ELSE TRUE END as estado,
		    TRUE as seleccionado, NULL::character varying as comentario
		FROM tabla_base ts
	)

	SELECT * FROM reporte order by fecha;


END;
$BODY$;

ALTER FUNCTION public.reporte_validacion_viento(integer, timestamp with time zone, timestamp with time zone, numeric, numeric)
    OWNER TO usuario1;
