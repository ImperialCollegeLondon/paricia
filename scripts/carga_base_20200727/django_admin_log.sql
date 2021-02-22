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
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2019-01-06 17:37:25.451851-05	1	admin	2	[{"changed": {"fields": ["password"]}}]	178	1
2	2019-01-06 17:37:48.056783-05	2	tecnico	2	[{"changed": {"fields": ["password"]}}]	178	1
3	2019-01-11 17:03:24.563746-05	1	admin	2	[{"changed": {"fields": ["password"]}}]	178	1
4	2019-01-11 17:04:27.211858-05	2	tecnico	2	[{"changed": {"fields": ["password"]}}]	178	1
5	2019-07-23 14:19:48.344192-05	1	admin	2	[{"changed": {"fields": ["password"]}}]	178	1
6	2019-07-23 14:20:34.954835-05	1	admin	2	[]	178	1
7	2019-07-23 14:21:58.168624-05	2	tecnico	2	[{"changed": {"fields": ["password"]}}]	178	1
8	2019-07-23 14:22:02.317943-05	2	tecnico	2	[]	178	1
9	2019-11-19 12:30:03.743161-05	3	admincal	1	[{"added": {}}]	178	1
10	2019-11-19 12:30:15.097476-05	3	admincal	2	[]	178	1
11	2019-11-19 12:30:30.795728-05	4	Teccal	1	[{"added": {}}]	178	1
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 11, true);


--
-- PostgreSQL database dump complete
--

