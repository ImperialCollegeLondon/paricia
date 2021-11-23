DROP FUNCTION IF EXISTS  public.reporte_validacion_diario_viento(integer, timestamp with time zone, timestamp with time zone, numeric, numeric);
CREATE OR REPLACE FUNCTION public.reporte_validacion_diario_viento(
	_estacion_id integer,
	_fecha_inicio timestamp with time zone,
	_fecha_fin timestamp with time zone,
	_var_maximo numeric,
	_var_minimo numeric)
    RETURNS TABLE(id bigint, fecha timestamp with time zone, fecha_error numeric, fecha_numero numeric,
    	valor numeric, maximo numeric, minimo numeric, direccion numeric, categoria numeric,
    	porcentaje numeric, porcentaje_error boolean,
        valor_error boolean, maximo_error boolean, minimo_error boolean,
        valor_numero numeric, maximo_numero numeric, minimo_numero numeric, estado boolean, validado boolean)
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
    /*validacion AS (
        SELECT v_vvi.id, v_vvi.fecha, 0 AS tipo, v_vvi.valor, v_vvi.maximo, v_vvi.minimo,
        v_dvi.valor as direccion,
        TRUE AS existe_en_validacion, FALSE as valor_vacio
        FROM validacion_velocidadviento v_vvi, validacion_direccionviento v_dvi WHERE v_vvi.estacion_id = (SELECT est_id FROM estacion)
        AND v_vvi.fecha >= _fecha_inicio AND v_vvi.fecha <= _fecha_fin AND v_vvi.fecha = v_dvi.fecha AND v_dvi.estacion_id = v_vvi.estacion_id
    ),*/

    validacion AS (
        SELECT v_vvi.id, v_vvi.fecha, 0 AS tipo, v_vvi.valor, v_vvi.maximo, v_vvi.minimo,
        v_vvi.direccion as direccion,
        TRUE AS existe_en_validacion, FALSE as valor_vacio
        FROM validacion_viento v_vvi WHERE v_vvi.estacion_id = (SELECT est_id FROM estacion)
        AND v_vvi.fecha >= _fecha_inicio AND v_vvi.fecha <= _fecha_fin
    ),
    --Seleccionar los datos de la tabla medicion
    medicion AS (
        SELECT m_vvi.id, m_vvi.fecha, 1 AS tipo, CASE WHEN m_vvi.valor = 'NaN' THEN NULL ELSE m_vvi.valor END AS valor ,
        CASE WHEN m_vvi.maximo = 'NaN' THEN NULL ELSE m_vvi.maximo END AS maximo , CASE WHEN m_vvi.minimo = 'NaN' THEN NULL ELSE m_vvi.minimo END AS minimo ,
        CASE WHEN m_dvi.valor = 'NaN' THEN NULL ELSE m_dvi.valor END AS direccion,

            EXISTS(SELECT * FROM validacion v_vvi WHERE v_vvi.fecha = m_vvi.fecha AND v_vvi.valor = m_vvi.valor) AS existe_en_validacion,
            EXISTS(SELECT * FROM validacion v_vvi WHERE v_vvi.fecha = m_vvi.fecha) AS valor_vacio
        FROM medicion_var4medicion m_vvi, medicion_var5medicion m_dvi WHERE m_vvi.estacion_id = (SELECT est_id FROM estacion)
        AND m_vvi.fecha >= _fecha_inicio AND m_vvi.fecha <= _fecha_fin AND m_vvi.fecha = m_dvi.fecha AND m_dvi.estacion_id = m_vvi.estacion_id
        AND NOT (m_vvi.valor IS NULL OR m_vvi.valor = 'NaN'::numeric) AND NOT (m_dvi.valor IS NULL OR m_vvi.valor = 'NAN'::numeric)
        AND NOT (m_dvi.valor IS NULL OR m_dvi.valor = 'NaN'::numeric)
    ),
	--unir las tablas medicion y validacion en una tabla
    union_med_val AS (
        SELECT * FROM validacion UNION SELECT * FROM medicion
    ),
    --Seleccionar una serie unica de los validados y los crudos
    tabla_base AS (
        SELECT
            --row_number() OVER (ORDER BY umv.fecha ASC, umv.tipo ASC, umv.id DESC) as numero_fila,
            *,
        CASE WHEN umv.direccion<= 22.5 OR umv.direccion> 337.5 THEN 1 ELSE
            CASE WHEN umv.direccion> 22.5 AND umv.direccion<= 67.5 THEN 2 ELSE
                CASE WHEN umv.direccion> 67.5 AND umv.direccion<= 112.5 THEN 3 ELSE
                    CASE WHEN umv.direccion> 112.5 AND umv.direccion<= 157.5 THEN 4 ELSE
                        CASE WHEN umv.direccion> 157.5 AND umv.direccion<= 202.5 THEN 5 ELSE
                            CASE WHEN umv.direccion> 202.5 AND umv.direccion<= 247.5 THEN 6 ELSE
                                CASE WHEN umv.direccion> 247.5 AND umv.direccion<= 292.5 THEN 7 ELSE
                                    CASE WHEN umv.direccion> 292.5 AND umv.direccion<= 337.5 THEN 8 ELSE NULL END
                                END
                            END
                        END
                    END
                END
            END
        END AS categoria
        FROM union_med_val umv WHERE NOT (umv.existe_en_validacion = TRUE AND umv.tipo = 1 OR umv.valor_vacio = TRUE)
    ),
    -- valores duplicados por cada fecha
    tabla_duplicados AS (

        SELECT tb.fecha, date_trunc('day',tb.fecha) as dia, COUNT(*) AS num_duplicados
        FROM tabla_base tb
        GROUP BY tb.fecha
        HAVING COUNT(*) > 1
        ORDER BY tb.fecha
    ),
    -- acumular los datos a diario
    tabla_acumulada AS (
        SELECT date_trunc('day',tb.fecha) as dia, tb.categoria, COUNT(tb.valor) numero_datos,
        ROUND(AVG(tb.valor),2) as valor, ROUND(MAX(tb.maximo),2) as maximo, ROUND(MIN(tb.minimo),2) as minimo, ROUND(AVG(tb.direccion),2) as direccion,
        bool_and(tb.existe_en_validacion) as existe_en_validacion
        FROM tabla_base tb GROUP BY dia, tb.categoria ORDER by dia, tb.categoria
    ),
    -- Numero de datos esperados por d?a
    tabla_datos_esperados AS (
        SELECT ta.dia, SUM(ta.numero_datos) as numero_datos,
        (SELECT CAST(1440/f.fre_valor AS INT) ndatos FROM frecuencia_frecuencia f WHERE f.fre_valor <= 60
            and f.est_id_id = (SELECT e.est_id FROM estacion e) AND f.var_id_id = (SELECT var_id FROM variable)
            AND f.fre_fecha_ini <= ta.dia
            AND (f.fre_fecha_fin >= ta.dia OR f.fre_fecha_fin IS NULL)
        ORDER BY f.fre_fecha_ini DESC LIMIT 1) as numero_datos_esperado
        FROM tabla_acumulada ta GROUP BY ta.dia ORDER by ta.dia
    ),
    tabla_calculo AS (
        SELECT tde.dia, tde.numero_datos, tde.numero_datos_esperado,
        ROUND((tde.numero_datos::decimal/tde.numero_datos_esperado)*100,2) as porcentaje,
        CASE WHEN ROUND((tde.numero_datos::decimal/tde.numero_datos_esperado)*100,2) < (SELECT umbral_completo FROM variable)
        OR ROUND((tde.numero_datos::decimal/tde.numero_datos_esperado)*100,2) > 100
        THEN TRUE ELSE FALSE END AS porcentaje_error
        FROM tabla_datos_esperados tde
    ),
    tabla_valores_sos AS (
        SELECT ta.dia,
            (SELECT COUNT(tb.valor) nsvalor FROM tabla_base tb WHERE date(tb.fecha) = ta.dia
                AND (tb.valor>_var_maximo OR tb.valor < _var_minimo )
            )::numeric as numero_valor_sospechoso,
            (SELECT COUNT(tb.maximo) nsvalor FROM tabla_base tb WHERE date(tb.fecha) = ta.dia
                AND (tb.maximo>_var_maximo OR tb.maximo < _var_minimo )
            )::numeric as numero_maximo_sospechoso,
            (SELECT COUNT(tb.minimo) nsvalor FROM tabla_base tb WHERE date(tb.fecha) = ta.dia
                AND (tb.minimo>_var_maximo OR tb.minimo < _var_minimo )
            )::numeric as numero_minimo_sospechoso
        FROM tabla_calculo ta ORDER BY ta.dia
    ),
    -- revision de lapsos de tiempo entre fechas
    lapsos_dias AS (
        SELECT
            ff.dia,
            row_number() OVER (ORDER BY ff.dia ASC) as fecha_grupo,
            EXTRACT(EPOCH FROM ff.dia - lag(ff.dia) OVER (ORDER BY ff.dia ASC))/86400 as lapso_tiempo
        FROM (SELECT tc.dia FROM tabla_calculo tc) ff ORDER BY dia ASC
    ),
    error_lapsos AS (
        SELECT *,
            CASE WHEN fecha_grupo = 1 THEN 1 ELSE
            CASE WHEN lapso_tiempo < 1 THEN 0
                 WHEN lapso_tiempo > 1 THEN 3
                 WHEN LEAD (lapso_tiempo) OVER (ORDER BY ld.dia) > 1 THEN 2
                ELSE 1
            END
        END AS fecha_valida
        FROM lapsos_dias ld
    ),
    reporte AS (
        SELECT
        row_number() OVER (ORDER BY ta.dia ASC) as id,
        ta.dia, (SELECT el.fecha_valida FROM error_lapsos el WHERE el.dia = ta.dia)::numeric as dia_error,
        (SELECT SUM(td.num_duplicados) FROM tabla_duplicados td WHERE td.dia = ta.dia)::numeric as fecha_numero,
        ta.valor::numeric as valor, ta.maximo::numeric as maximo, ta.minimo::numeric as minimo,
        ta.direccion as direccion, ta.categoria::numeric as cagegoria,
        (SELECT tc.porcentaje FROM tabla_calculo tc WHERE tc.dia = ta.dia) as porcentaje,
        (SELECT tc.porcentaje_error FROM tabla_calculo tc WHERE tc.dia = ta.dia) as porcentaje_error,
        --ta.valor > _var_maximo OR ta.valor < _var_minimo AS valor_error,
        --ta.maximo > _var_maximo OR ta.maximo < _var_minimo AS maximo_error,
        --ta.minimo > _var_maximo OR ta.minimo < _var_minimo AS minimo_error,
        CASE WHEN (SELECT tvs.numero_valor_sospechoso FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia)> 0 THEN true ELSE false END as valor_error,
        CASE WHEN (SELECT tvs.numero_maximo_sospechoso FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia)> 0 THEN true ELSE false END as valor_error,
        CASE WHEN (SELECT tvs.numero_minimo_sospechoso FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia)> 0 THEN true ELSE false END as valor_error,
        (SELECT tvs.numero_valor_sospechoso FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia) as valor_numero,
        (SELECT tvs.numero_maximo_sospechoso FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia) as maximo_numero,
        (SELECT tvs.numero_minimo_sospechoso FROM tabla_valores_sos tvs WHERE tvs.dia = ta.dia) as minimo_numero,


        TRUE as estado,
        ta.existe_en_validacion as validado
        FROM tabla_acumulada ta

    )
    SELECT * FROM reporte;

END;
$BODY$;

--ALTER FUNCTION public.reporte_validacion_diario_viento(integer, timestamp with time zone, timestamp with time zone, numeric, numeric)
--    OWNER TO usuario1;