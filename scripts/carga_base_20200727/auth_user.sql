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
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
3	pbkdf2_sha256$100000$QQPPpFt8EL04$2YghQDHxbWhuSHbnFDJuXP3O0zPXQjM7e7H9f60iNj4=	2020-07-24 11:10:42.841924-05	f	admincal				f	t	2019-11-19 12:30:03-05
2	pbkdf2_sha256$100000$1t4DLC5SvLEW$AayTTIejw568Kg1ffN78rNKdpiLJVYxEIZemwf9Inug=	2020-07-24 21:19:48.614291-05	f	tecnico			tecnico@aguaquitoparamh20.com	f	t	2019-01-05 18:25:54-05
6	pbkdf2_sha256$100000$ov7sXo79ZiuC$+/2WO/5sk8cby01F5GxtbGzSsyXAfxvGcpaBChRchsQ=	2020-03-06 11:58:27.310566-05	t	admin_sedc	 	 	 	t	t	2020-03-01 18:01:00-05
4	pbkdf2_sha256$100000$6ByITCeVuBhA$h1DVut9YMCTWexcN8eAHahXbiEwV6bQG2KXjIQQ+x5I=	2019-12-10 01:20:40.630876-05	f	Teccal				f	t	2019-11-19 12:30:30.687853-05
1	pbkdf2_sha256$100000$3XIbb9Tfby81$5qs9AkOF+nMYQ8M3V9eb7+xUDaDa3SyDq7czxF3gYvo=	2020-07-20 09:01:57.000965-05	t	admin			admin@aguaquitoparamh20.com	t	t	2019-01-05 18:25:54-05
\.


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 6, true);


--
-- PostgreSQL database dump complete
--

