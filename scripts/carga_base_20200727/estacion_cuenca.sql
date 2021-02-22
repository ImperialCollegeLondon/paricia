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
-- Data for Name: estacion_cuenca; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estacion_cuenca (id, nombre, imagen) FROM stdin;
1	Anglo French	estacion/cuencas/AngloFrench.jpg
2	Colegio	estacion/cuencas/Colegio.jpg
3	El Batán	estacion/cuencas/Batan.jpg
4	Machágara	estacion/cuencas/Machangara.jpg
5	El Cinto	estacion/cuencas/Cinto.jpg
6	La Chorrera	estacion/cuencas/Chorrera.jpg
7	Filtros Pichincha	estacion/cuencas/FiltrosPichicha.jpg
8	San Pedro	estacion/cuencas/SanPedro.jpg
9	Guayllabamba Alto	estacion/cuencas/GuayAlto.jpg
10	Guayllabamba Medio	estacion/cuencas/GuayMedio.jpg
11	Santa Clara	
12	Antisana	estacion/cuencas/Antisana.jpg
13	Caicedo	estacion/cuencas/Caicedo.jpg
14	Mindo	estacion/cuencas/Mindo.jpg
15	Pichán	estacion/cuencas/Pichan.jpg
16	Rumihurco	estacion/cuencas/Rumihurco.jpg
17	Rumipamba	estacion/cuencas/Rumipamba.jpg
19	Oyacachi	estacion/cuencas/Oyacachi.jpg
20	Papallacta	estacion/cuencas/Papallacta.jpg
22	Tambo	estacion/cuencas/Tambo.jpg
23	Tamboyacu	estacion/cuencas/Tamboyacu.jpg
25	Pita	estacion/cuencas/Pita.jpg
21	Quijos	estacion/cuencas/Quijos.jpg
24	Valle Vicioso	estacion/cuencas/Valle_Vicioso.jpg
18	Chalpi	estacion/cuenca_imagen/Chalpi.jpg
\.


--
-- Name: estacion_cuenca_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.estacion_cuenca_id_seq', 26, false);


--
-- PostgreSQL database dump complete
--

