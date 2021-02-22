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
-- Data for Name: formato_delimitador; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.formato_delimitador (del_id, del_nombre, del_caracter) FROM stdin;
6	Coma	,
7	Dos Puntos	:
8	Punto y Com	;
1	Tabulador	\\x09
2	Linea	\\x0A
3	Espacio	\\x20
4	Comilla doble	\\x22
5	Comilla Simple	\\x27
9	BackSlash	\\x5C
\.


--
-- Name: formato_delimitador_del_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.formato_delimitador_del_id_seq', 10, false);


--
-- PostgreSQL database dump complete
--

