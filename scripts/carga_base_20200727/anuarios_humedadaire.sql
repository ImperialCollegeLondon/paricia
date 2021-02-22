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
-- Data for Name: anuarios_humedadaire; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.anuarios_humedadaire (hai_id, hai_periodo, hai_mes, hai_maximo, hai_maximo_dia, hai_minimo, hai_minimo_dia, hai_promedio, est_id_id) FROM stdin;
\.


--
-- Name: anuarios_humedadaire_hai_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.anuarios_humedadaire_hai_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

