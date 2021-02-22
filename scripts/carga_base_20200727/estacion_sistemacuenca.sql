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
-- Data for Name: estacion_sistemacuenca; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estacion_sistemacuenca (id, imagen, cuenca_id, sistema_id) FROM stdin;
1		1	1
2		2	1
3		3	1
4		4	1
5		5	2
6		7	2
7		6	2
8		8	2
9		9	3
10		10	3
11		11	3
12		12	4
13		13	5
14		14	5
15		15	5
16		16	5
17		17	5
18		18	6
19		19	6
20		20	6
22		22	6
23		23	6
24		24	6
25		25	7
21		21	6
27	\N	20	5
37	\N	14	7
28	\N	21	5
36	\N	13	7
\.


--
-- Name: estacion_sistemacuenca_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.estacion_sistemacuenca_id_seq', 26, false);


--
-- PostgreSQL database dump complete
--

