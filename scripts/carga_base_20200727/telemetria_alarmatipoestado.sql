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
-- Data for Name: telemetria_alarmatipoestado; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.telemetria_alarmatipoestado (id, nombre, descripcion) FROM stdin;
1	NORMAL	La transmisión es contínua.
2	EXPECTANTE	No ha existido transmisión en mas de 1 hora pero aún no excede el período de tolerancia.
3	FALLO	Se considera transmisión fallida. Execedió el período de tolerancia.
\.


--
-- Name: telemetria_alarmatipoestado_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.telemetria_alarmatipoestado_id_seq', 4, false);


--
-- PostgreSQL database dump complete
--

