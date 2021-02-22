--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.15
-- Dumped by pg_dump version 9.6.15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: formato_formato; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.formato_formato (for_id, for_nombre, for_descripcion, for_ubicacion, for_archivo, for_fil_ini, for_fil_cola, for_col_fecha, for_col_hora, for_tipo, for_estado, del_id_id, ext_id_id, fec_id_id, hor_id_id, es_fecha_utc) FROM stdin;
1	HOBO UA	HOBO UA	\N	\N	1	\N	2	2	convencional	t	1	3	5	2	f
29	Vaisala (relleno)	Formato provisional para completar información de las estaciones vaisala	\N	\N	3	0	1	2		t	8	2	5	2	f
3	VAISALA (C12)	VAISALA (C12)	\N	\N	3	\N	1	2	convencional	t	6	2	2	1	f
6	Dipper PT (Sin temperatura)	Dipper PT (Sin temperatura)	\N	\N	2	\N	1	1	convencional	t	1	3	4	2	f
7	HOBO JR5	HOBO JR5	\N	\N	2	\N	1	2	convencional	t	3	1	1	2	f
9	LASCAR (0.1)	LASCAR (0.1)	\N	\N	2	\N	2	2	convencional	t	1	3	4	2	f
10	LASCAR (0.24)	LASCAR (0.24)	\N	\N	2	\N	2	2	convencional	t	1	3	4	2	f
32	YDOC (csv)	Extensión .csv	\N	\N	4	\N	1	2		t	6	2	4	2	f
12	Vitel (Solo precip.)	Vitel (Solo precip.)	\N	\N	13	\N	2	4	convencional	t	3	4	11	3	f
31	CAMPBELL ultrasonico(m)	formato .DAT	\N	\N	5	\N	1	1		t	6	5	3	2	f
17	HOBO JR5 (csv)	HOBO JR5 (csv)	\N	\N	2	\N	1	1		t	6	2	4	3	f
21	VAISALA (precipitación)	VAISALA (precipitación)	\N	\N	3	\N	1	2		t	6	2	2	1	f
22	Seba	Seba (Hidrológicas)	\N	\N	21	7	1	2		t	3	4	12	2	f
8	DAVIS	DAVIS	\N	\N	2	\N	1	2	convencional	t	3	1	1	2	f
23	Vaisala (Sin Precipitación)	Formato vaisala excluyendo el parámetro de precipitación (históricos)	\N	\N	3	0	1	2		t	6	2	2	1	f
24	VAISALA_MODIF	Para carga de c06 y c07 archivos de presi+on atmosférica estan registrados cada minuto por lo que se demora en su validación	\N	\N	3	\N	1	2		t	6	2	2	1	f
4	Dipper PT	Dipper PT	\N	\N	2	\N	1	1	convencional	t	1	3	4	2	f
26	Temperatura General	Temperatura General	\N	\N	1	\N	1	1		t	6	1	3	2	f
27	VAISALA (C13)	VAISALA (C13)	\N	\N	3	\N	1	2		t	6	2	2	1	f
11	Pluvio General	Pluvio General	\N	\N	1	\N	1	1	convencional	t	6	2	4	3	f
34	Vaisala (editado)	Formato editado, se cambia hora UTC a formato local. Extensión .xlsx	\N	\N	3	0	1	1		t	6	3	4	2	f
33	VAISAL (C11-12-13)	Formato csv C11 2011	\N	\N	3	\N	1	2		t	6	2	2	1	f
18	Hidro General	Hidro General	\N	\N	2	\N	1	1		t	6	2	4	3	f
35	Vaisala precipitación	Hora editada	\N	\N	3	0	1	1		t	6	3	1	2	f
2	VAISALA UTC	VAISALA UTC	\N	\N	3	\N	1	2	convencional	t	6	2	2	1	t
36	Precipitación Vaisala UTC	Solo precipitación datalogger vaisala	\N	\N	3	0	1	2		t	6	2	2	1	t
5	SEBA	SEBA	\N	\N	21	6	1	2	convencional	t	3	4	12	2	f
37	Cambell Hidrológica	Nivel y temperatura del agua	\N	\N	5	0	1	1		t	6	5	3	2	f
38	Vaisala Temperatura	Archivo para completar información	\N	\N	2	0	1	1		t	6	3	8	2	t
25	Cambell Climatológicas (1)	Formato de datos climatológicos sin precipitación	\N	\N	5	\N	1	1		t	6	5	3	2	f
39	Humedad vaisala	Archivo para completar vacío de humedad	\N	\N	2	0	1	1		t	6	3	4	2	t
40	Humedad general	Formato general para humedad	\N	\N	2	0	1	1		t	6	3	4	2	f
41	Temperatura C13	Formato .csv vaisala	\N	\N	3	0	1	2		t	6	2	2	1	f
42	Cambell Climatológicas Excel	Formato excel, estaciones Cambell, incluye precipitación. Estación base C14.	\N	\N	5	0	1	1		t	1	3	4	2	f
\.


--
-- Name: formato_formato_for_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.formato_formato_for_id_seq', 42, true);


--
-- PostgreSQL database dump complete
--

