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
-- Data for Name: telemetria_alarmaemail; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.telemetria_alarmaemail (id, email) FROM stdin;
1	diego.escobar@aguaquito.gob.ec
2	claudia.encalada@aguaquito.gob.ec
4	teresa.munioz@aguaquito.gob.ec
5	paul.murillo@aguaquito.gob.ec
6	rafael.osorio@aguaquito.gob.ec
\.


--
-- Name: telemetria_alarmaemail_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.telemetria_alarmaemail_id_seq', 7, false);


--
-- PostgreSQL database dump complete
--

