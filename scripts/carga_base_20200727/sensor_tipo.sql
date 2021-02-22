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
-- Data for Name: sensor_tipo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sensor_tipo (tip_id, tip_nombre) FROM stdin;
1	Pluviómetro
2	Sonda Piezométrico
3	Sonda Ultrasónico
4	Sensor de viento
5	Humedad y Temperatura
6	Presión Barométrica
7	Radiación Solar
8	Dirección del viento
9	Velocidad del viento
\.


--
-- Name: sensor_tipo_tip_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sensor_tipo_tip_id_seq', 10, false);


--
-- PostgreSQL database dump complete
--

