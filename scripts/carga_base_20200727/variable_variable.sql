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
-- Data for Name: variable_variable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.variable_variable (var_id, var_codigo, var_nombre, var_maximo, var_minimo, var_sos, var_err, var_min, var_estado, es_acumulada, reporte_automatico, umbral_completo, uni_id_id) FROM stdin;
1	pre	Precipitación	13.00	0.00	3.50	4.00	3.00	t	t	t	80.0	6
2	tai	Temperatura ambiente	28.00	-5.00	2.00	3.00	3.00	t	f	t	70.0	8
3	hai	Humedad relativa	100.00	0.00	10.00	20.00	3.00	t	f	t	70.0	3
4	vvi	Velocidad de viento	15.00	0.00	5.00	10.00	3.00	t	f	t	70.0	9
5	dvi	Dirección de viento	360.00	0.00	361.00	370.00	3.00	t	f	t	70.0	2
6	hsu	Humedad de suelo	100.00	0.00	100.00	100.00	3.00	f	f	f	70.0	3
7	rad	Radiación solar	1353.00	0.00	700.00	800.00	3.00	t	f	t	70.0	13
8	pat	Presion atmosférica	740.00	630.00	0.12	0.22	3.00	t	f	t	70.0	5
9	tag	Temperatura de agua	17.00	0.00	2.00	3.00	3.00	t	f	t	70.0	8
10	cau	Caudal	8.00	0.00	2.00	3.00	3.00	t	f	t	70.0	14
11	nag	Nivel de agua	250.00	0.00	15.00	20.00	3.00	t	f	t	70.0	4
12	vol	Voltaje de batería	15.00	12.00	100.00	100.00	3.00	t	f	f	70.0	12
13	caf	Caudal de aforo	8.00	0.00	100.00	100.00	3.00	t	f	f	70.0	14
14	nre	Nivel de regleta	300.00	0.00	100.00	100.00	3.00	t	f	f	\N	4
15	dvr	Dirección de viento ráfaga	360.00	0.00	100.00	100.00	3.00	t	t	f	\N	2
16	rvi	Recorrido de viento	17.00	0.00	100.00	100.00	3.00	t	f	f	\N	10
17	gustdir	GustDir	1.00	0.00	100.00	100.00	3.00	f	f	f	\N	1
18	gusth	GustH	1.00	0.00	100.00	100.00	3.00	f	f	f	\N	1
19	gustm	GustM	1.00	0.00	100.00	100.00	3.00	f	f	f	\N	1
20	tsu	Temperatura de suelo	20.00	-3.00	100.00	100.00	3.00	f	f	f	70.0	8
21	rin	Radiacion indirecta	1.00	0.00	100.00	100.00	3.00	f	f	f	70.0	13
22	radsum	Radiacion solar suma	6000.00	0.00	35000.00	40000.00	3.00	t	t	f	\N	13
101	T° Agua	Temperatura agua	99.00	0.00	\N	\N	\N	t	f	t	70.0	8
102	pH	pH	14.00	0.00	\N	\N	\N	t	f	t	70.0	16
103	ORP	Potencial REDOX	2000.00	0.00	\N	\N	\N	t	f	t	70.0	17
104	Turp.	Turbidez	10000.00	0.00	\N	\N	\N	t	f	t	70.0	18
105	chl.	Clorofila	100.00	0.00	\N	\N	\N	t	f	t	70.0	19
106	HDO	Oxígeno disuelto	14.00	0.00	\N	\N	\N	t	f	t	70.0	20
107	HDO%	Porcentaje de Oxígeno disuelto	100.00	0.00	\N	\N	\N	t	f	t	70.0	3
\.


--
-- Name: variable_variable_var_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.variable_variable_var_id_seq', 108, false);


--
-- PostgreSQL database dump complete
--

