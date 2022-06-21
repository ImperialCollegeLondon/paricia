/*
Required data types for 'importing' app:
    date__value
    date__value__maximum__minimum
    date__xxx__xxx_xxx
    ...

    Those types used in `importacion/functions.py: guardar_datos__temp_a_final()`
        The data to import is passed to PGSQL query as a string and then its formatted
            using the type:  `unnest(%s::date__value__station_id[])`


Required data types for 'validation' app (NOTE: NOT IMPLEMENTED YET):
    validacion
    validacion_profundidad

*/

DROP TYPE IF EXISTS date__value;
CREATE TYPE date__value AS (date TIMESTAMP WITHOUT TIME ZONE, value NUMERIC);

DROP TYPE IF EXISTS date__value__maximum__minimum;
CREATE TYPE date__value__maximum__minimum AS (date TIMESTAMP WITHOUT TIME ZONE, value NUMERIC, maximum NUMERIC, minimum NUMERIC);



DROP TYPE IF EXISTS date__value__station_id;
CREATE TYPE date__value__station_id AS (date TIMESTAMP WITHOUT TIME ZONE, value NUMERIC, station_id INT);

DROP TYPE IF EXISTS date__maximum__station_id;
CREATE TYPE date__maximum__station_id AS (date TIMESTAMP WITHOUT TIME ZONE, maximum NUMERIC, station_id INT);

DROP TYPE IF EXISTS date__minimum__station_id;
CREATE TYPE date__minimum__station_id AS (date TIMESTAMP WITHOUT TIME ZONE, minimum NUMERIC, station_id INT);

DROP TYPE IF EXISTS date__value__maximum__station_id;
CREATE TYPE date__value__maximum__station_id AS (date TIMESTAMP WITHOUT TIME ZONE, value NUMERIC, maximum NUMERIC, station_id INT);

DROP TYPE IF EXISTS date__value__minimum__station_id;
CREATE TYPE date__value__minimum__station_id AS (date TIMESTAMP WITHOUT TIME ZONE, value NUMERIC, minimum NUMERIC, station_id INT);

DROP TYPE IF EXISTS date__maximum__minimum__station_id;
CREATE TYPE date__maximum__minimum__station_id AS (date TIMESTAMP WITHOUT TIME ZONE, maximum NUMERIC, minimum NUMERIC, station_id INT);

DROP TYPE IF EXISTS date__value__maximum__minimum__station_id;
CREATE TYPE date__value__maximum__minimum__station_id AS (date TIMESTAMP WITHOUT TIME ZONE, value NUMERIC, maximum NUMERIC, minimum NUMERIC, station_id INT);




DROP TYPE IF EXISTS validacion;
CREATE type validacion AS (date TIMESTAMP, value NUMERIC, comentario VARCHAR);

DROP TYPE IF EXISTS validacion_profundidad;
CREATE type validacion_profundidad AS (date TIMESTAMP, profundidad INTEGER, value NUMERIC, comentario VARCHAR);
