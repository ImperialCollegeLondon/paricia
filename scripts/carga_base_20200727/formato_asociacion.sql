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
-- Data for Name: formato_asociacion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.formato_asociacion (aso_id, est_id_id, for_id_id) FROM stdin;
1	1	1
2	2	2
3	4	11
4	5	2
5	6	2
6	7	2
7	8	2
8	10	2
9	11	1
10	12	3
11	13	2
12	17	4
13	19	4
14	21	5
15	23	4
16	24	4
17	25	4
18	32	5
19	33	4
20	34	5
21	41	6
22	43	4
23	44	4
24	54	1
25	56	7
26	57	1
27	59	1
28	61	1
29	62	1
30	65	1
31	67	1
32	68	1
33	76	7
34	77	8
35	77	9
36	78	8
37	78	9
38	79	1
39	86	8
40	86	9
41	86	10
42	87	12
43	87	9
44	89	1
45	91	9
46	91	8
47	92	1
48	93	1
49	94	1
50	96	1
51	97	1
52	98	1
53	99	1
54	101	1
55	102	1
56	103	1
57	104	1
58	105	1
59	106	1
60	107	1
61	108	1
62	109	1
63	110	1
64	111	1
65	112	1
66	113	1
67	114	1
68	115	9
70	56	1
75	76	17
76	19	18
77	76	1
81	75	1
82	20	18
83	32	18
84	41	18
85	23	18
86	25	18
87	43	22
88	87	1
89	25	5
90	21	18
91	30	18
93	34	18
94	36	18
95	112	11
96	114	11
97	658	9
98	659	9
99	11	23
100	77	1
101	7	24
102	6	24
103	115	1
104	658	1
105	46	22
108	1	26
109	4	26
110	13	27
111	1	25
112	2	26
113	3	26
115	6	26
116	56	11
117	7	26
118	71	1
119	86	1
120	659	1
123	10	29
124	91	1
125	20	4
127	50	4
131	663	4
132	664	4
135	90	1
137	36	4
139	94	25
140	91	25
134	48	32
133	50	31
141	11	33
142	12	33
143	101	34
144	13	33
145	2	34
147	5	34
148	6	34
149	8	34
150	10	34
151	13	34
152	74	34
153	73	34
154	13	1
155	79	35
156	101	2
157	76	36
158	19	37
159	34	4
160	36	5
162	47	37
164	5	38
126	51	\N
129	53	\N
130	52	\N
136	29	\N
138	30	\N
163	49	\N
165	11	25
166	5	39
167	12	40
168	13	41
170	13	40
172	94	42
173	73	2
\.


--
-- Name: formato_asociacion_aso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.formato_asociacion_aso_id_seq', 173, true);


--
-- PostgreSQL database dump complete
--

