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
-- Data for Name: formato_clasificacion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.formato_clasificacion (cla_id, cla_valor, cla_maximo, cla_minimo, col_validador_valor, txt_validador_valor, col_validador_maximo, txt_validador_maximo, col_validador_minimo, txt_validador_minimo, acumular, incremental, resolucion, coma_decimal, for_id_id, var_id_id) FROM stdin;
1	4	\N	\N	\N	\N	\N	\N	\N	\N	t	t	0.10	t	1	1
2	4	6	8	3	VALID	5	VALID	7	VALID	f	f	\N	f	2	2
3	10	12	14	9	VALID	11	VALID	13	VALID	f	f	\N	f	2	3
4	16	18	20	15	VALID	17	VALID	19	VALID	f	f	\N	f	2	8
5	22	\N	\N	21	VALID	\N	\N	\N	\N	f	f	\N	f	2	1
6	24	26	28	23	VALID	25	VALID	27	VALID	f	f	\N	f	2	7
7	30	\N	\N	29	VALID	\N	\N	\N	\N	f	f	\N	f	2	22
8	32	34	36	31	VALID	33	VALID	35	VALID	f	f	\N	f	2	5
9	38	\N	\N	37	VALID	\N	\N	\N	\N	f	f	\N	f	2	17
10	40	42	44	39	VALID	41	VALID	43	VALID	f	f	\N	f	2	4
11	46	\N	\N	45	VALID	\N	\N	\N	\N	f	f	\N	f	2	16
12	48	\N	\N	47	VALID	\N	\N	\N	\N	f	f	\N	f	2	12
13	4	6	8	3	VALID	5	VALID	7	VALID	f	f	\N	f	3	3
14	10	12	14	9	VALID	11	VALID	13	VALID	f	f	\N	f	3	7
15	16	18	20	15	VALID	17	VALID	19	VALID	f	f	\N	f	3	2
16	22	\N	\N	21	VALID	\N	\N	\N	\N	f	f	\N	f	3	1
17	24	\N	\N	23	VALID	\N	\N	\N	\N	f	f	\N	f	3	22
18	26	\N	\N	25	VALID	\N	\N	\N	\N	f	f	\N	f	3	5
19	28	\N	\N	27	VALID	\N	\N	\N	\N	f	f	\N	f	3	17
20	30	\N	\N	29	VALID	\N	\N	\N	\N	f	f	\N	f	3	18
21	32	\N	\N	31	VALID	\N	\N	\N	\N	f	f	\N	f	3	19
22	34	36	38	33	VALID	35	VALID	37	VALID	f	f	\N	f	3	4
23	40	\N	\N	39	VALID	\N	\N	\N	\N	f	f	\N	f	3	16
24	42	44	46	41	VALID	43	VALID	45	VALID	f	f	\N	f	3	8
25	2	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	4	11
26	3	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	t	5	11
27	2	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	6	11
28	3	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	6	12
29	3	\N	\N	\N	\N	\N	\N	\N	\N	t	t	1.00	f	7	1
30	3	\N	\N	\N	\N	\N	\N	\N	\N	t	t	1.00	f	8	1
31	3	\N	\N	\N	\N	\N	\N	\N	\N	t	f	0.10	f	9	1
32	3	\N	\N	\N	\N	\N	\N	\N	\N	t	f	0.24	f	10	1
33	2	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	11	1
34	5	\N	\N	\N	\N	\N	\N	\N	\N	f	t	0.10	f	12	1
41	2	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	18	11
43	2	\N	\N	\N	\N	\N	\N	\N	\N	t	t	1.00	f	17	1
45	22	\N	\N	21	VALID	\N	\N	\N	\N	f	f	1.00	f	21	1
46	3	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	t	22	11
47	4	6	8	3	VALID	5	VALID	7	VALID	f	f	\N	f	23	3
48	10	12	14	9	VALID	11	VALID	13	VALID	f	f	\N	f	23	7
49	16	18	20	15	VALID	17	VALID	19	VALID	f	f	\N	f	23	2
50	24	\N	\N	23	VALID	\N	\N	\N	\N	f	f	\N	f	23	22
51	26	\N	\N	25	VALID	\N	\N	\N	\N	f	f	\N	f	23	5
52	28	\N	\N	27	VALID	\N	\N	\N	\N	f	f	\N	f	23	17
53	30	\N	\N	29	VALID	\N	\N	\N	\N	f	f	\N	f	23	18
54	32	\N	\N	31	VALID	\N	\N	\N	\N	f	f	\N	f	23	19
55	34	36	38	33	VALID	35	VALID	37	VALID	f	f	\N	f	23	4
56	40	\N	\N	39	VALID	\N	\N	\N	\N	f	f	\N	f	23	16
57	42	44	46	41	VALID	43	VALID	45	VALID	f	f	\N	f	23	8
61	16	18	20	\N	\N	\N	\N	\N	\N	f	f	\N	f	24	8
71	2	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	t	26	2
76	10	11	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	25	4
77	13	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	25	5
78	15	16	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	25	7
79	21	19	20	\N	\N	\N	\N	\N	\N	f	f	\N	f	25	8
81	4	6	8	\N	\N	\N	\N	\N	\N	f	f	\N	f	27	2
83	10	12	14	\N	\N	\N	\N	\N	\N	f	f	\N	f	27	3
84	40	42	44	\N	\N	\N	\N	\N	\N	f	f	\N	f	27	4
85	32	34	36	\N	\N	\N	\N	\N	\N	f	f	\N	f	27	5
86	24	26	28	\N	\N	\N	\N	\N	\N	f	f	\N	f	27	7
87	16	18	20	\N	\N	\N	\N	\N	\N	f	f	\N	f	27	8
89	46	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	27	16
90	48	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	27	12
91	38	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	27	17
92	30	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	27	22
96	4	6	7	3	VALID	5	VALID	7	VALID	f	f	\N	f	29	2
97	10	12	14	9	VALID	11	VALID	13	VALID	f	f	\N	f	29	3
98	16	18	20	15	VALID	17	VALID	19	VALID	f	f	\N	f	29	8
99	24	26	28	23	VALID	25	VALID	27	VALID	f	f	\N	f	29	7
100	32	34	36	31	VALID	33	VALID	35	VALID	f	f	\N	f	29	5
101	40	42	44	39	VALID	37	VALID	39	VALID	f	f	\N	f	29	4
103	48	\N	\N	47	VALID	\N	\N	\N	\N	f	f	\N	f	29	12
104	22	\N	\N	21	VALID	\N	\N	\N	\N	f	f	\N	f	29	1
111	5	\N	\N	\N	\N	\N	\N	\N	\N	f	f	100.00	f	32	11
112	3	\N	\N	\N	\N	\N	\N	\N	\N	f	f	100.00	f	31	11
121	4	6	8	3	VALID	5	VALID	7	VALID	f	f	1.00	f	33	3
124	24	\N	\N	23	VALID	\N	\N	\N	\N	f	f	1.00	f	33	22
125	26	\N	\N	25	VALID	\N	\N	\N	\N	f	f	1.00	f	33	5
126	28	\N	\N	27	VALID	\N	\N	\N	\N	f	f	1.00	f	33	17
127	34	36	38	33	VALID	35	VALID	37	VALID	f	f	1.00	f	33	4
128	42	44	46	41	VALID	43	VALID	45	VALID	f	f	1.00	f	33	8
130	3	5	7	4	VALID	6	VALID	8	VALID	f	f	1.00	f	34	2
131	9	11	13	10	VALID	12	VALID	14	VALID	f	f	1.00	f	34	3
132	15	17	19	16	VALID	18	VALID	20	VALID	f	f	1.00	f	34	8
133	23	25	27	24	VALID	26	VALID	28	VALID	f	f	1.00	f	34	7
134	31	33	35	32	VALID	34	VALID	36	VALID	f	f	1.00	f	34	5
135	39	41	43	40	VALID	42	VALID	44	VALID	f	f	1.00	f	34	4
136	47	\N	\N	\N	\N	\N	\N	\N	\N	f	f	1.00	f	34	12
137	21	\N	\N	22	VALID	\N	\N	\N	\N	f	f	1.00	f	34	1
138	29	\N	\N	30	VALID	\N	\N	\N	\N	f	f	1.00	f	34	22
140	10	12	14	11	VALID	13	VALID	15	VALID	f	f	1.00	f	33	7
142	23	\N	\N	\N	\N	\N	\N	\N	\N	f	f	1.00	f	25	12
143	5	\N	\N	4	VALID	\N	\N	\N	\N	f	f	\N	f	35	1
144	4	\N	\N	3	VALID	\N	\N	\N	\N	f	f	1.00	f	36	1
145	6	\N	\N	5	VALID	\N	\N	\N	\N	f	f	\N	f	36	12
146	9	11	10	\N	\N	\N	\N	\N	\N	f	f	\N	f	37	9
147	3	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	37	12
148	5	7	6	\N	\N	\N	\N	\N	\N	f	f	\N	f	37	11
149	4	2	3	\N	\N	\N	\N	\N	\N	f	f	\N	f	38	2
151	5	3	4	\N	\N	\N	\N	\N	\N	f	f	\N	f	39	3
152	2	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	40	3
153	16	18	20	17	VALID	19	VALID	21	VALID	f	f	\N	f	41	2
154	4	5	6	\N	\N	\N	\N	\N	\N	f	f	\N	f	42	2
155	8	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	42	3
156	10	11	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	42	4
157	13	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	42	5
158	15	16	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	42	7
159	21	19	20	\N	\N	\N	\N	\N	\N	f	f	\N	f	42	8
161	23	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	42	12
162	21	\N	\N	\N	\N	\N	\N	\N	\N	f	f	\N	f	42	8
\.


--
-- Name: formato_clasificacion_cla_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.formato_clasificacion_cla_id_seq', 162, true);


--
-- PostgreSQL database dump complete
--

