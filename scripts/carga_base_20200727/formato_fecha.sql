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
-- Data for Name: formato_fecha; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.formato_fecha (fec_id, fec_formato, fec_codigo) FROM stdin;
1	DD/MM/YY	%d/%m/%y
2	MM/DD/YY	%m/%d/%y
3	YYYY-MM-DD	%Y-%m-%d
4	DD/MM/YYYY	%d/%m/%Y
5	MM/DD/YYYY	%m/%d/%Y
6	DD-BB-YY	%d-%b-%y
7	YYYY-DD-MM	%Y-%d-%m
8	DD-MM-YYYY	%d-%m-%Y
9	YY-DD-MM	%y-%m-%d
10	YY-MM-DD	%y-%m-%d
11	YYYY DOY	%Y %j
12	DD.MM.YYYY	%d.%m.%Y
\.


--
-- Name: formato_fecha_fec_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.formato_fecha_fec_id_seq', 13, false);


--
-- PostgreSQL database dump complete
--

