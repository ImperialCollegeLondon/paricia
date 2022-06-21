-- Type: type_validacion_agua

DROP TYPE IF EXISTS public.type_validacion_agua;
CREATE TYPE public.type_validacion_agua AS
(
	fecha timestamp without time zone,
	nivel numeric,
	caudal numeric,
	estado boolean,
	seleccionado boolean,
	comentario character varying
);

--ALTER TYPE public.type_validacion_agua
--    OWNER TO usuario1;





-- Type: type_validacion_viento

DROP TYPE IF EXISTS public.type_validacion_viento;
CREATE TYPE public.type_validacion_viento AS
(
	fecha timestamp without time zone,
	valor numeric,
	maximo numeric,
	minimo numeric,
	direccion numeric,
	categoria numeric,
	estado boolean,
	seleccionado boolean,
	comentario character varying
);

--ALTER TYPE public.type_validacion_viento
--    OWNER TO usuario1;





-- Type: validacion_acu

DROP TYPE IF EXISTS public.validacion_acu;
CREATE TYPE public.validacion_acu AS
(
	fecha timestamp without time zone,
	valor numeric,
	estado boolean,
	seleccionado boolean,
	comentario character varying
);

--ALTER TYPE public.validacion_acu
--    OWNER TO usuario1;





-- Type: validacion_pro

DROP TYPE IF EXISTS public.validacion_pro;
CREATE TYPE public.validacion_pro AS
(
	fecha timestamp without time zone,
	valor numeric,
	maximo numeric,
	minimo numeric,
	estado boolean,
	seleccionado boolean,
	comentario character varying
);

--ALTER TYPE public.validacion_pro
--    OWNER TO usuario1;