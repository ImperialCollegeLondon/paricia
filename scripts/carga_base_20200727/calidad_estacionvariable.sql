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
-- Data for Name: calidad_estacionvariable; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.calidad_estacionvariable (id, estacion_id, variable_id) FROM stdin;
1	666	101
2	666	102
3	666	103
4	666	104
5	666	105
6	666	106
7	666	107
\.


--
-- Name: calidad_estacionvariable_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.calidad_estacionvariable_id_seq', 7, true);


--
-- PostgreSQL database dump complete
--

