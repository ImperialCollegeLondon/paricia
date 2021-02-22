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
-- Data for Name: estacion_sistema; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estacion_sistema (id, nombre, imagen) FROM stdin;
1	Alcantarillado	estacion/sistemas/SistAlcantarillado.jpg
2	Centro Occidente	estacion/sistemas/SisOccidente.jpg
3	Menores	estacion/sistemas/SisMenores.jpg
4	Mica Quito Sur	estacion/sistemas/SisMica.jpg
7	Pita - Puengasí	estacion/sistemas/SisPita.jpg
5	Noroccidente	estacion/sistema_imagen/SisNoroccidente.jpg
6	Papallacta	estacion/sistema_imagen/SisPapallacta.jpg
\.


--
-- Name: estacion_sistema_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.estacion_sistema_id_seq', 8, false);


--
-- PostgreSQL database dump complete
--

