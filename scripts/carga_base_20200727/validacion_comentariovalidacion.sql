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
-- Data for Name: validacion_comentariovalidacion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.validacion_comentariovalidacion (id, variable_id, estacion_id, validado_id, comentario) FROM stdin;
1	1	75	78511967	Salto
2	1	13	80730959	Visita, limpieza del pluviómetro
3	1	658	82123110	Limpieza
4	1	56	82265078	Visita estación
5	1	57	82278086	Visita estación
6	1	89	82854919	Mantenimiento estación
7	1	5	82978086	Visita estación
8	1	6	82982154	Visita
9	1	63	83023895	Visita
10	1	70	83047162	Visita
11	1	74	83059178	Visita
12	1	75	83063532	Visita
13	1	76	83068769	Visita
14	1	79	83088204	Visita
15	1	113	83481192	Visita
16	4	13	617911	valor atipico imposible
17	1	11	83596447	Visita
18	1	111	83726596	Visita
19	1	111	83726671	Visita
20	1	10	83776913	Visita
21	1	6	84175758	Visita estación
22	1	11	84216237	Visita
23	1	60	84286000	Visita
24	1	60	84286002	Visita
25	1	61	84298603	Visita
26	1	65	84368581	Visita
27	1	68	84372960	Visita
28	1	96	84654268	Visita
29	1	113	84749663	Visita
30	1	4	84774970	Visita
31	101	666	700	Validación de prueba
32	102	666	299	Validación prubea
33	101	666	16510	Validación de prueba
34	1	78	86464767	Visita
35	1	78	86464768	Visita
36	1	88	86500391	Visita
37	1	92	86513542	Visita
38	1	95	86531232	Visita
39	1	97	86558584	Visita
40	1	101	87778152	Visita
41	1	91	88885191	VISITA
42	1	76	92220988	Visita
43	1	76	92249010	Visita
44	1	7	93609336	VISITA
45	1	57	94944073	Visita, cambio de pluviómetro
46	1	57	106743585	Visita
\.


--
-- Name: validacion_comentariovalidacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.validacion_comentariovalidacion_id_seq', 46, true);


--
-- PostgreSQL database dump complete
--

