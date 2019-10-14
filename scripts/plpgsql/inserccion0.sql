
DROP TYPE IF EXISTS fecha__valor;
CREATE TYPE fecha__valor AS (fecha TIMESTAMP WITHOUT TIME ZONE, valor NUMERIC);

DROP TYPE IF EXISTS fecha__valor__maximo__minimo;
CREATE TYPE fecha__valor__maximo__minimo AS (fecha TIMESTAMP WITHOUT TIME ZONE, valor NUMERIC, maximo NUMERIC, minimo NUMERIC);




DROP TYPE IF EXISTS validacion;
CREATE type validacion AS (fecha TIMESTAMP, valor NUMERIC, comentario VARCHAR);


