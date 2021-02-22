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
-- Data for Name: telemetria_configvisualizar; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.telemetria_configvisualizar (id, umbral_superior, umbral_inferior, estacion_id, variable_id) FROM stdin;
2	\N	\N	60	1
3	\N	\N	63	1
4	\N	\N	64	1
5	\N	\N	70	1
7	\N	\N	73	1
8	\N	\N	74	1
9	\N	\N	82	1
10	\N	\N	85	1
11	\N	\N	88	1
13	\N	\N	95	1
18	\N	\N	2	5
25	\N	\N	5	5
28	\N	\N	6	1
29	\N	\N	6	2
30	\N	\N	6	3
31	\N	\N	6	4
32	\N	\N	6	5
33	\N	\N	6	7
34	\N	\N	6	8
42	\N	\N	8	1
43	\N	\N	8	2
44	\N	\N	8	3
45	\N	\N	8	4
46	\N	\N	8	5
47	\N	\N	8	7
48	\N	\N	8	8
49	\N	\N	10	1
50	\N	\N	10	2
51	\N	\N	10	3
52	\N	\N	10	4
53	\N	\N	10	5
54	\N	\N	10	7
55	\N	\N	10	8
56	\N	\N	13	1
59	\N	\N	13	4
60	\N	\N	13	5
61	\N	\N	13	7
63	\N	\N	65	1
64	\N	\N	79	1
65	\N	\N	96	1
66	\N	\N	97	1
68	\N	\N	78	1
153	\N	\N	19	10
154	\N	\N	41	10
155	\N	\N	51	10
70	\N	\N	56	1
71	\N	\N	99	1
72	\N	\N	67	1
73	\N	\N	76	1
74	\N	\N	61	1
75	\N	\N	57	1
76	\N	\N	68	1
77	\N	\N	112	1
79	\N	\N	114	1
80	\N	\N	113	1
81	\N	\N	59	1
82	\N	\N	75	1
84	\N	\N	92	1
88	\N	\N	71	1
156	\N	\N	52	10
14	4.000000	0.000000	2	1
16	100.000000	35.000000	2	3
17	11.000000	0.000000	2	4
19	1250.000000	0.000000	2	7
157	\N	\N	53	10
20	668.000000	662.000000	2	8
21	4.000000	0.000000	5	1
22	23.000000	6.000000	5	2
23	100.000000	30.000000	5	3
1	4.000000	0.000000	4	1
24	5.000000	0.000000	5	4
26	1250.000000	0.000000	5	7
27	720.000000	711.000000	5	8
158	\N	\N	47	11
62	645.000000	637.000000	13	8
92	\N	\N	4	5
95	\N	\N	73	2
96	\N	\N	73	3
97	\N	\N	73	4
98	\N	\N	73	5
99	\N	\N	73	7
100	\N	\N	73	8
101	\N	\N	74	2
102	\N	\N	74	3
103	\N	\N	74	4
104	\N	\N	74	5
105	\N	\N	74	7
106	\N	\N	74	8
89	18.000000	4.000000	4	2
90	100.000000	35.000000	4	3
91	5.000000	0.000000	4	4
93	1250.000000	0.000000	4	7
94	687.000000	682.000000	4	8
110	\N	\N	111	1
113	\N	\N	41	11
115	\N	\N	51	11
116	\N	\N	51	9
118	\N	\N	52	11
119	\N	\N	52	9
121	\N	\N	53	11
122	\N	\N	53	9
125	\N	\N	7	1
127	\N	\N	7	3
128	\N	\N	7	4
129	\N	\N	7	5
130	\N	\N	7	7
131	\N	\N	7	8
132	\N	\N	659	1
78	4.000000	\N	54	1
133	\N	\N	11	2
134	\N	\N	11	3
135	\N	\N	11	8
136	\N	\N	11	1
137	\N	\N	11	7
139	\N	\N	11	5
140	\N	\N	11	4
142	\N	\N	19	11
143	\N	\N	19	9
144	\N	\N	91	2
145	\N	\N	91	3
146	\N	\N	91	8
147	\N	\N	91	1
148	\N	\N	91	7
150	\N	\N	91	5
151	\N	\N	91	4
159	\N	\N	47	10
160	\N	\N	47	9
161	\N	\N	48	11
162	\N	\N	48	10
164	\N	\N	49	11
165	\N	\N	49	10
166	\N	\N	49	9
15	16.000000	4.000000	2	2
126	28.000000	8.000000	7	2
\.


--
-- Name: telemetria_configvisualizar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.telemetria_configvisualizar_id_seq', 170, true);


--
-- PostgreSQL database dump complete
--

