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
-- Data for Name: datalogger_marca; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.datalogger_marca (mar_id, mar_nombre) FROM stdin;
1	HOBO
2	IOS
3	Lascar electronics
4	Vitel
5	Campbell
6	Vaisala
7	Dipper
8	SEBA
9	(No aplica)
\.


--
-- Name: datalogger_marca_mar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.datalogger_marca_mar_id_seq', 10, false);


--
-- PostgreSQL database dump complete
--

