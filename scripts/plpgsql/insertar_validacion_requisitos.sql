/*
Required data types for 'importing' app:
    fecha__valor
    fecha__valor__maximo__minimo
    fecha__xxx__xxx_xxx
    ...

    Those types used in `importacion/functions.py: guardar_datos__temp_a_final()`
        The data to import is passed to PGSQL query as a string and then its formatted
            using the type:  `unnest(%s::fecha__valor__estacion_id[])`


Required data types for 'validation' app:
    validacion
    validacion_profundidad

*/

DROP TYPE IF EXISTS fecha__valor;
CREATE TYPE fecha__valor AS (fecha TIMESTAMP WITHOUT TIME ZONE, valor NUMERIC);

DROP TYPE IF EXISTS fecha__valor__maximo__minimo;
CREATE TYPE fecha__valor__maximo__minimo AS (fecha TIMESTAMP WITHOUT TIME ZONE, valor NUMERIC, maximo NUMERIC, minimo NUMERIC);



DROP TYPE IF EXISTS fecha__valor__estacion_id;
CREATE TYPE fecha__valor__estacion_id AS (fecha TIMESTAMP WITHOUT TIME ZONE, valor NUMERIC, estacion_id INT);

DROP TYPE IF EXISTS fecha__maximo__estacion_id;
CREATE TYPE fecha__maximo__estacion_id AS (fecha TIMESTAMP WITHOUT TIME ZONE, maximo NUMERIC, estacion_id INT);

DROP TYPE IF EXISTS fecha__minimo__estacion_id;
CREATE TYPE fecha__minimo__estacion_id AS (fecha TIMESTAMP WITHOUT TIME ZONE, minimo NUMERIC, estacion_id INT);

DROP TYPE IF EXISTS fecha__valor__maximo__estacion_id;
CREATE TYPE fecha__valor__maximo__estacion_id AS (fecha TIMESTAMP WITHOUT TIME ZONE, valor NUMERIC, maximo NUMERIC, estacion_id INT);

DROP TYPE IF EXISTS fecha__valor__minimo__estacion_id;
CREATE TYPE fecha__valor__minimo__estacion_id AS (fecha TIMESTAMP WITHOUT TIME ZONE, valor NUMERIC, minimo NUMERIC, estacion_id INT);

DROP TYPE IF EXISTS fecha__maximo__minimo__estacion_id;
CREATE TYPE fecha__maximo__minimo__estacion_id AS (fecha TIMESTAMP WITHOUT TIME ZONE, maximo NUMERIC, minimo NUMERIC, estacion_id INT);

DROP TYPE IF EXISTS fecha__valor__maximo__minimo__estacion_id;
CREATE TYPE fecha__valor__maximo__minimo__estacion_id AS (fecha TIMESTAMP WITHOUT TIME ZONE, valor NUMERIC, maximo NUMERIC, minimo NUMERIC, estacion_id INT);




DROP TYPE IF EXISTS validacion;
CREATE type validacion AS (fecha TIMESTAMP, valor NUMERIC, comentario VARCHAR);

DROP TYPE IF EXISTS validacion_profundidad;
CREATE type validacion_profundidad AS (fecha TIMESTAMP, profundidad INTEGER, valor NUMERIC, comentario VARCHAR);
