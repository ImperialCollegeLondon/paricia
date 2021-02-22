--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3 (Ubuntu 12.3-1.pgdg18.04+1)
-- Dumped by pg_dump version 12.3 (Ubuntu 12.3-1.pgdg18.04+1)

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
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: usuario1
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
3	pbkdf2_sha256$180000$fpEay4zBgXjd$4XT/Ioy4j6BfLwprAui+0z/K5276xfzuCVoB/Tx4gLs=	2020-07-23 10:47:57.224428-05	f	adminhidro				f	t	2020-07-21 11:02:26-05
1	pbkdf2_sha256$180000$PMcQpHBF26js$fhHyTBdpXp+8tcsn7ItYk3oZ+IxLD4yQHByWsAuuchQ=	2020-07-27 08:28:54.685948-05	t	admin			admin@paramh2o.aguaquito.gob.ec	t	t	2020-07-21 10:55:13.00124-05
5	pbkdf2_sha256$180000$VKBWIQs7Dn0c$cAY8YEXSEX1wKNpbS4qUerX2zWNgGdUGcANA+nxzcQg=	2020-07-27 10:43:55.132124-05	f	admincalidad				f	t	2020-07-21 11:04:36-05
2	!VkTTWaJeCWtZZzpcj1x82UKDMkyLEGBTM4HYk4sz	\N	f	AnonymousUser				f	t	2020-07-21 10:58:42-05
6	pbkdf2_sha256$180000$gXKSI7c3XV61$Nkndgf6JaA8JVqdA+S+72E0xmOqlVGKNPeGyiGcElaE=	2020-07-27 13:19:55.301444-05	f	teccalidad				f	t	2020-07-21 11:05:04-05
4	pbkdf2_sha256$180000$yMDOyGIqCeQX$X7CmLvPxRP1m+1IcnBWkOPYP9bRfvxlM0FOUZWAe6MI=	2020-07-27 13:48:19.473413-05	f	techidro				f	t	2020-07-21 11:03:40-05
\.


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: usuario1
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 6, true);


--
-- PostgreSQL database dump complete
--

