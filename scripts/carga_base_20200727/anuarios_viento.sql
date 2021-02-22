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
-- Data for Name: anuarios_viento; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.anuarios_viento (vie_id, vie_periodo, vie_mes, "vie_vel_N", "vie_por_N", "vie_vel_NE", "vie_por_NE", "vie_vel_E", "vie_por_E", "vie_vel_SE", "vie_por_SE", "vie_vel_S", "vie_por_S", "vie_vel_SO", "vie_por_SO", "vie_vel_O", "vie_por_O", "vie_vel_NO", "vie_por_NO", vie_calma, vie_obs, vie_vel_max, vie_vel_dir, vie_vel_med, est_id_id) FROM stdin;
\.


--
-- Name: anuarios_viento_vie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.anuarios_viento_vie_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

