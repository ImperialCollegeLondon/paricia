# Este script crea las funciones necesarias para el modulo validacion.
# creacion de las funcion para mostrar los datos para validar

import os
from django.db import connection
cursor = connection.cursor()

# variables para validaciones
varibles = ["precipitacion", "temperaturaaire", "humedadaire", "velocidadviento", "direccionviento", "humedadsuelo",
            "radiacionsolar", "presionatmosferica", "temperaturaagua", "caudal", "nivelagua"]

# Tipos de datos para inserccion
inserccion_types = """
DROP TYPE IF EXISTS fecha__valor__maximo__minimo__estacion_id;
CREATE TYPE fecha__valor__maximo__minimo__estacion_id AS (fecha TIMESTAMP WITHOUT TIME ZONE, valor NUMERIC, maximo NUMERIC, minimo NUMERIC, estacion_id INT);

DROP TYPE IF EXISTS fecha__valor__estacion_id;
CREATE TYPE fecha__valor__estacion_id AS (fecha TIMESTAMP WITHOUT TIME ZONE, valor NUMERIC, estacion_id INT);

DROP TYPE IF EXISTS fecha__valor;
CREATE TYPE fecha__valor AS (fecha TIMESTAMP WITHOUT TIME ZONE, valor NUMERIC);

DROP TYPE IF EXISTS fecha__valor__maximo__minimo;
CREATE TYPE fecha__valor__maximo__minimo AS (fecha TIMESTAMP WITHOUT TIME ZONE, valor NUMERIC, maximo NUMERIC, minimo NUMERIC);

"""
cursor.execute(inserccion_types)
######################################################################
##  insertar validacion
validacion_type = """
DROP TYPE IF EXISTS validacion;
CREATE type validacion AS (fecha TIMESTAMP, valor NUMERIC, comentario VARCHAR);
"""
cursor.execute(validacion_type)

funcionValidacion = """DROP FUNCTION IF EXISTS insertar_%%variable%%_validacion(bigint, json);
CREATE OR REPLACE FUNCTION insertar_%%variable%%_validacion(_estacion_id bigint, _datos json)
  RETURNS BOOLEAN AS
$BODY$
DECLARE
	curs_datos CURSOR FOR
		SELECT * FROM json_populate_recordset( null::validacion, _datos) t1;

	ultimo_validacion   integer;
	ultimo_valor        numeric;
	id_insertado       validacion_%%variable%%.id%TYPE;
BEGIN
    FOR row_datos in curs_datos LOOP
        ultimo_validacion := NULL;
		SELECT val.validacion, val.valor INTO ultimo_validacion, ultimo_valor
  			FROM validacion_%%variable%% val
  			WHERE val.estacion_id = _estacion_id AND val.fecha = row_datos.fecha
			ORDER BY val.validacion DESC LIMIT 1;

  		IF ultimo_validacion IS NULL THEN
  			ultimo_validacion := 0;
  		ELSE
  			ultimo_validacion := ultimo_validacion + 1;
            IF (row_datos.valor IS NULL) AND (ultimo_valor IS NULL) THEN CONTINUE; END IF;
		    IF row_datos.valor = ultimo_valor THEN CONTINUE; END IF;  			
  		END IF;

		INSERT INTO validacion_%%variable%%(estacion_id, fecha, valor, usado_para_horario, validacion)
			VALUES (_estacion_id, row_datos.fecha, row_datos.valor, FALSE, ultimo_validacion) 
			RETURNING id INTO id_insertado;

		IF row_datos.comentario IS NOT NULL THEN
			INSERT INTO validacion_comentariovalidacion(variable_id, estacion_id, validado_id, comentario)
				VALUES (%%var_id%%, _estacion_id, id_insertado, row_datos.comentario);
		END IF;

    END LOOP;

	RETURN TRUE;
END
$BODY$  LANGUAGE plpgsql
"""

for index, var in enumerate(varibles):
    #print("Variable ",var, "indice ", index+1)
    validacion_sql = funcionValidacion.replace('%%variable%%', var)
    validacion_sql = validacion_sql.replace('%%var_id%%',str(index))
    cursor.execute(validacion_sql)



### funciones de reportes de validadcion
funRepoValida = """DROP FUNCTION IF EXISTS reporte_validacion_%%variable%%(integer,timestamp with time zone,timestamp with time zone);
CREATE OR REPLACE FUNCTION reporte_validacion_%%variable%%(_estacion_id INT, _fecha_inicio TIMESTAMP WITH TIME ZONE, _fecha_fin TIMESTAMP WITH TIME ZONE)
RETURNS TABLE (
	numero_fila BIGINT,
	seleccionado BOOL,
	fecha TIMESTAMP WITH TIME ZONE,
	valor_seleccionado NUMERIC,
	valor NUMERIC,
	variacion_consecutiva NUMERIC,
	comentario VARCHAR,
	class_fila TEXT,
	class_fecha TEXT,
	class_validacion TEXT,
	class_valor TEXT,
	class_variacion_consecutiva TEXT,
	class_stddev_error TEXT
)
AS $$

BEGIN
	RETURN QUERY
	WITH
	estacion AS (SELECT * FROM estacion_estacion est WHERE est.est_id = _estacion_id),
	variable AS (SELECT * FROM variable_variable var WHERE var.var_id = %%var_id%%),
	validacion AS (
		SELECT v.id, v.fecha, 0 AS tipo, v.valor, v.validacion, TRUE AS existe_en_validacion
		FROM validacion_%%variable%% v WHERE v.estacion_id = (SELECT est_id FROM estacion) AND v.fecha >= _fecha_inicio AND v.fecha <= _fecha_fin
	),
	medicion AS (
		SELECT m.id, m.fecha, 1 AS tipo, m.valor, CAST(NULL AS smallint) AS validacion,
			EXISTS(SELECT * FROM validacion v WHERE v.fecha = m.fecha AND v.valor = m.valor) AS existe_en_validacion
		FROM medicion_%%variable%% m WHERE m.estacion_id = (SELECT est_id FROM estacion) AND m.fecha >= _fecha_inicio AND m.fecha <= _fecha_fin
	),
	union_med_val AS (
		SELECT * FROM validacion UNION SELECT * FROM medicion
	),
	fechas0 AS (
		SELECT
			ff.fecha,
			row_number() OVER (ORDER BY ff.fecha ASC) as fecha_grupo,
			EXTRACT(EPOCH FROM ff.fecha - lag(ff.fecha) OVER (ORDER BY ff.fecha ASC))/60  as lapso_tiempo,
			(SELECT fre.fre_valor FROM frecuencia_frecuencia fre
					WHERE fre.var_id_id = (SELECT var_id FROM variable) AND fre.est_id_id = (SELECT est_id FROM estacion) AND fre.fre_fecha_ini < ff.fecha
					ORDER BY fre.fre_fecha_ini DESC LIMIT 1) AS periodo_esperado
		FROM (SELECT DISTINCT(umv.fecha) FROM union_med_val umv) ff ORDER BY fecha ASC
	),
	fechas AS (
		SELECT *,
			CASE WHEN fecha_grupo = 1 THEN 1 ELSE
			CASE WHEN lapso_tiempo < periodo_esperado - 0.13 THEN 0
				 WHEN lapso_tiempo > periodo_esperado + 0.13 THEN 2
				ELSE 1
			END
		END AS fecha_valida
		FROM fechas0
	),
	tabla_base AS (
		SELECT
			row_number() OVER (ORDER BY umv.fecha ASC, umv.tipo ASC, umv.validacion DESC, umv.id DESC) as numero_fila,
			*
		FROM union_med_val umv WHERE NOT (umv.existe_en_validacion = TRUE AND umv.tipo = 1)
	),
	tabla1 AS (
		SELECT *,
			(SELECT fecha_grupo FROM fechas f WHERE f.fecha = tb.fecha) AS fecha_grupo,
			CASE WHEN tb.numero_fila = 1 THEN TRUE ELSE CASE WHEN lag(tb.fecha) OVER (ORDER BY tb.numero_fila ASC) != tb.fecha THEN TRUE ELSE FALSE END END AS seleccionado,
			(SELECT med.id FROM medicion med WHERE med.fecha = tb.fecha ORDER BY id ASC LIMIT 1) AS medicion_id
		FROM tabla_base tb
	),
	tabla2 AS (
		SELECT *,
			(SELECT t1.valor - (SELECT tanterior.valor FROM tabla1 tanterior WHERE tanterior.fecha_grupo = t1.fecha_grupo - 1 AND tanterior.seleccionado IS TRUE) ) AS variacion_consecutiva,
			CASE WHEN t1.seleccionado THEN t1.valor ELSE NULL END AS valor_seleccionado
		FROM tabla1 t1
	),
	estadistica AS (
		SELECT e1.media AS media, e1.desv_est AS desv_est,
		e1.media - (e1.desv_est * (SELECT var_min FROM variable)) AS lim_inf_stddev,
		e1.media + (e1.desv_est * (SELECT var_min FROM variable)) AS lim_sup_stddev
		FROM (
			SELECT AVG(t2.valor) AS media, STDDEV_SAMP(t2.valor) AS desv_est
			FROM tabla2 t2
			WHERE t2.valor IS NOT NULL AND t2.seleccionado IS TRUE
		) e1
	),
	reporte AS (
		SELECT *,
			(SELECT fecha_valida FROM fechas ff WHERE ff.fecha = t2.fecha) AS fecha_error,
			t2.valor > (SELECT var_maximo FROM variable) OR t2.valor < (SELECT var_minimo FROM variable) AS valor_error,
			CASE
				WHEN ABS(t2.variacion_consecutiva) <= (SELECT var_sos FROM variable) THEN 0
				WHEN (ABS(t2.variacion_consecutiva) > (SELECT var_sos FROM variable) AND ABS(t2.variacion_consecutiva) <= (SELECT var_err FROM variable)) THEN 1
				WHEN ABS(t2.variacion_consecutiva) > (SELECT var_sos FROM variable) THEN 2
				ELSE 0
			END AS variacion_nivel,
			t2.valor < (SELECT lim_inf_stddev FROM estadistica ) OR t2.valor > (SELECT lim_sup_stddev FROM estadistica)  AS stddev_error,
			CASE
				WHEN existe_en_validacion THEN
					(SELECT vc.comentario FROM validacion_comentariovalidacion vc WHERE vc.estacion_id = (SELECT est_id FROM estacion) AND vc.variable_id = (SELECT var_id FROM variable) AND vc.validado_id = t2.id)
				ELSE NULL
			END AS comentario
		FROM tabla2 t2
	),
	-- Reporte_con_clases_para_html pudiera ser removido para reducir consumo de memoria RAM
	reporte_con_clases_para_html AS (
		SELECT *,
			CASE
			    WHEN r.seleccionado THEN CAST(fecha_grupo AS text) || ' seleccionado'
			    ELSE CAST(fecha_grupo AS text)  || ' no-seleccionado' END  AS class_fila,
			CASE WHEN fecha_error = 0 THEN 'fecha error' WHEN fecha_error = 1 THEN 'fecha normal' ELSE 'fecha salto' END AS class_fecha,
			CASE WHEN existe_en_validacion THEN 'validacion validado' ELSE 'validacion no-validado' END AS class_validacion,
			CASE WHEN valor_error THEN 'valor error' ELSE 'valor normal' END AS class_valor,
			CASE variacion_nivel WHEN 0 THEN  'var_con normal' WHEN 1 THEN 'var_con sospechoso' WHEN 2 THEN 'var_con error' END AS class_variacion_consecutiva,
			CASE WHEN stddev_error THEN 'stddev error' ELSE 'stddev normal' END AS class_stddev_error
		FROM reporte r
	)
	SELECT rf.numero_fila, rf.seleccionado, rf.fecha, rf.valor_seleccionado, rf.valor, rf.variacion_consecutiva, rf.comentario, rf.class_fila, rf.class_fecha, rf.class_validacion,
		rf.class_valor, rf.class_variacion_consecutiva, rf.class_stddev_error FROM reporte_con_clases_para_html rf;
END; $$
LANGUAGE 'plpgsql';"""

for index, var in enumerate(varibles):
    print("Variable ",var,"indice ",index+1)
    sqlFun = funRepoValida.replace('%%variable%%', var)
    sqlFun = sqlFun.replace('%%var_id%%',str(index+1))
    cursor.execute(sqlFun)



