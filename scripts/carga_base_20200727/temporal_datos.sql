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
-- Data for Name: temporal_datos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.temporal_datos (med_id, var_id, est_id, med_fecha, med_valor, med_maximo, med_minimo, med_estado, horario_generado) FROM stdin;
\.


--
-- Name: temporal_datos_med_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.temporal_datos_med_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

