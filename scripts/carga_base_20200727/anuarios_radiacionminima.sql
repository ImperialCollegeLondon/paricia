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
-- Data for Name: anuarios_radiacionminima; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.anuarios_radiacionminima (rad_id, rad_periodo, rad_mes, rad_5, rad_6, rad_7, rad_8, rad_9, rad_10, rad_11, rad_12, rad_13, rad_14, rad_15, rad_16, rad_17, rad_18, rad_max, rad_hora, est_id_id) FROM stdin;
\.


--
-- Name: anuarios_radiacionminima_rad_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.anuarios_radiacionminima_rad_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

