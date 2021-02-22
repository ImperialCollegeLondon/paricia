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
-- Data for Name: frecuencia_tipofrecuencia; Type: TABLE DATA; Schema: public; Owner: usuario1
--

COPY public.frecuencia_tipofrecuencia (id, nombre) FROM stdin;
1	Subhorario crudo
2	Subhorario validado
3	Horario
4	Diario
5	Mensual
\.


--
-- Name: frecuencia_tipofrecuencia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: usuario1
--

SELECT pg_catalog.setval('public.frecuencia_tipofrecuencia_id_seq', 5, true);


--
-- PostgreSQL database dump complete
--

