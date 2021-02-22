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
-- Data for Name: formato_hora; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.formato_hora (hor_id, hor_formato, hor_codigo) FROM stdin;
1	HH:MM:SS AM/PM	%I:%M:%S %p
2	HH:MM:SS 24H	%H:%M:%S
3	HH:MM 24H	%H:%M
\.


--
-- Name: formato_hora_hor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.formato_hora_hor_id_seq', 4, false);


--
-- PostgreSQL database dump complete
--

