
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
