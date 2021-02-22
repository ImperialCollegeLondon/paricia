--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3 (Ubuntu 12.3-1.pgdg18.04+1)
-- Dumped by pg_dump version 12.3 (Ubuntu 12.3-1.pgdg18.04+1)

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
-- Data for Name: frecuencia_usuariotipofrecuencia; Type: TABLE DATA; Schema: public; Owner: usuario1
--

COPY public.frecuencia_usuariotipofrecuencia (id, tipofrecuencia_id, usuario_id) FROM stdin;
1	1	5
2	2	5
3	3	5
4	4	5
5	5	5
6	1	3
7	2	3
8	3	3
9	4	3
10	5	3
11	2	2
12	3	2
13	4	2
14	5	2
15	2	6
16	3	6
17	4	6
18	5	6
19	2	4
20	3	4
21	4	4
22	5	4
\.


--
-- Name: frecuencia_usuariotipofrecuencia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: usuario1
--

SELECT pg_catalog.setval('public.frecuencia_usuariotipofrecuencia_id_seq', 22, true);


--
-- PostgreSQL database dump complete
--

