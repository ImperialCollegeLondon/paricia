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
-- Data for Name: instalacion_instalacion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.instalacion_instalacion (ins_id, ins_fecha_ini, ins_fecha_fin, ins_en_uso, ins_observacion, dat_id_id, est_id_id) FROM stdin;
1	2018-01-01	\N	t		1	1
8	2018-01-01	\N	t		8	10
10	2018-01-01	\N	t		10	12
11	2018-01-01	\N	t		11	13
14	2018-01-01	\N	t		14	23
15	2018-01-01	\N	t		15	25
18	2018-01-01	\N	t		18	32
19	2018-01-01	\N	t		19	33
21	2018-01-01	\N	t		21	41
22	2018-01-01	\N	t		22	43
23	2018-01-01	\N	t		23	44
24	2018-01-01	\N	t		24	46
26	2018-01-01	\N	t		26	48
29	2018-01-01	\N	t		29	56
35	2018-01-01	\N	t		35	63
40	2018-01-01	\N	t		40	70
41	2018-01-01	\N	t		41	71
46	2018-01-01	\N	t		46	77
47	2018-01-01	\N	t		47	78
48	2018-01-01	\N	t		48	79
49	2018-01-01	\N	t		49	82
50	2018-01-01	\N	t		50	85
51	2018-01-01	\N	t		51	86
52	2018-01-01	\N	t		52	87
54	2018-01-01	\N	t		54	89
55	2018-01-01	\N	t		55	90
56	2018-01-01	\N	t		56	91
59	2018-01-01	\N	t		59	94
60	2018-01-01	\N	t		60	95
62	2018-01-01	\N	t		62	97
63	2018-01-01	\N	t		63	98
69	2018-01-01	\N	t		69	105
70	2018-01-01	\N	t		70	106
71	2018-01-01	\N	t		71	107
72	2018-01-01	\N	t		72	108
75	2018-01-01	\N	t		75	111
43	2018-01-01	\N	t		35	74
44	2018-01-01	\N	t		67	75
45	2018-01-01	\N	t		66	76
3	2018-01-01	\N	t		16	4
4	2018-01-01	\N	t		2	5
5	2018-01-01	\N	t		4	6
7	2018-01-01	\N	t		5	8
9	2018-01-01	\N	t		61	11
53	2018-01-01	\N	t		53	88
2	2018-01-01	\N	t		80	2
6	2018-01-01	\N	t		81	7
28	2018-01-01	\N	t		56	54
57	2018-01-01	\N	t		29	92
30	2018-01-01	\N	t		39	57
31	2018-01-01	\N	t		44	59
32	2018-01-01	\N	t		42	60
33	2018-01-01	\N	t		30	61
34	2018-01-01	\N	t		1	62
58	2018-01-01	\N	t		68	93
36	2018-01-01	\N	t		40	64
37	2018-01-01	\N	t		34	65
38	2018-01-01	\N	t		31	67
39	2018-01-01	\N	t		28	68
42	2018-01-01	\N	t		36	73
61	2018-01-01	\N	t		69	96
64	2018-01-01	\N	t		38	99
65	2018-01-01	\N	t		83	101
66	2018-01-01	\N	t		59	102
67	2018-01-01	\N	t		65	103
68	2018-01-01	\N	t		84	104
73	2018-01-01	\N	t		71	109
74	2018-01-01	\N	t		33	110
76	2018-01-01	\N	t		58	112
77	2018-01-01	\N	t		37	113
78	2018-01-01	\N	t		57	114
79	2018-01-01	\N	t		85	115
80	2018-12-13	\N	t		54	658
12	2018-01-01	\N	t		86	19
13	2018-01-01	\N	t		87	20
16	2018-01-01	\N	t		88	29
17	2018-01-01	\N	t		27	30
20	2018-01-01	\N	t		89	36
25	2018-01-01	\N	t		26	47
27	2018-01-01	\N	t		25	49
81	2018-01-11	\N	t		90	51
82	2018-01-11	\N	t		91	52
83	2018-01-11	\N	t		92	53
84	2018-01-11	\N	t		93	47
85	2018-01-11	\N	t		94	48
86	2018-01-11	\N	t		95	29
87	2018-01-11	\N	t		96	30
88	2018-01-11	\N	t		97	19
89	2018-01-11	\N	t		98	91
90	2018-01-11	\N	t		99	94
91	2018-01-11	\N	t		100	1
92	2018-01-11	\N	t		101	11
93	2019-05-09	\N	t		102	4
94	2019-05-09	\N	t		103	74
95	2019-05-09	\N	t		104	73
96	2019-05-09	\N	t		105	101
97	2019-05-09	\N	t		106	4
98	2019-05-09	\N	t		107	74
99	2019-05-09	\N	t		108	73
100	2019-05-09	\N	t		109	101
\.


--
-- Name: instalacion_instalacion_ins_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.instalacion_instalacion_ins_id_seq', 100, true);


--
-- PostgreSQL database dump complete
--

