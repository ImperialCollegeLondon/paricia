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
-- Data for Name: sensor_marca; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sensor_marca (mar_id, mar_nombre) FROM stdin;
1	Young
2	Texas electronics
3	Davis
4	Weathertronics
5	ISCO
6	Seba
7	Ultrasonica
8	VAISALA
9	Kipp Zonen
10	MET ONE
11	SETRA
12	BISELA
13	Licor
14	Keller
15	Hukseflux
\.


--
-- Name: sensor_marca_mar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sensor_marca_mar_id_seq', 15, true);


--
-- PostgreSQL database dump complete
--

