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
-- Data for Name: variable_unidad; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.variable_unidad (uni_id, uni_nombre, uni_sigla) FROM stdin;
1	Kilómetros por Hora	km/h
2	Grados	°
3	Porcentaje	%
4	Centímetros	cm
5	Hecto Pascales	hPa
6	Milímetros	mm
7	KiloWatts por m2	kW/m2
8	Grados Centígrados	°C
9	Metros por Segundo	m/s
10	Metros	m
11	Mega Jouls por m2	MJ/m2
12	Voltios	V
13	Watts por m2	W/m2
14	Metros Cúbicos por Segundo	m3/s
15	Milímetros por Hora	mm/h
16	Potencial Hidrógeno	pH
18	Nephelometric Turbidity Unit	NTU
17	mili Voltio	mV
19	microgramo por Litro	ug/L
20	miligramo por Litro	mg/L
\.


--
-- Name: variable_unidad_uni_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.variable_unidad_uni_id_seq', 21, false);


--
-- PostgreSQL database dump complete
--

