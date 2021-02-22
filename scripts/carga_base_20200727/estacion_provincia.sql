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
-- Data for Name: estacion_provincia; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estacion_provincia (id, nombre) FROM stdin;
1	Azuay
2	Bolívar
3	Cañar
4	Carchi
5	Chimborazo
6	Cotopaxi
7	Imbabura
8	Loja
9	Pichincha
10	Tungurahua
11	El Oro
12	Esmeraldas
13	Guayas
14	Los Ríos
15	Manabí
16	Santo Domingo de los Tsáchilas
17	Santa Elena
18	Morona Santiago
19	Napo
20	Orellana
21	Pastaza
22	Sucumbíos
23	Zamora Chinchipe
24	Galápagos
\.


--
-- Name: estacion_provincia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.estacion_provincia_id_seq', 25, false);


--
-- PostgreSQL database dump complete
--

