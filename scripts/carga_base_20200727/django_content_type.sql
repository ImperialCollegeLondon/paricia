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
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	horario	var16horario
2	horario	var21horario
3	horario	var7horario
4	horario	var5horario
5	horario	var12horario
6	horario	var19horario
7	horario	var22horario
8	horario	var6horario
9	horario	var14horario
10	horario	var9horario
11	horario	var13horario
12	horario	var2horario
13	horario	var4horario
14	horario	var11horario
15	horario	var20horario
16	horario	var8horario
17	horario	var23horario
18	horario	var24horario
19	horario	var18horario
20	horario	var1horario
21	horario	var15horario
22	horario	var17horario
23	horario	var3horario
24	horario	var10horario
25	diario	var3diario
26	diario	var7diario
27	diario	var13diario
28	diario	var9diario
29	diario	var21diario
30	diario	var12diario
31	diario	var22diario
32	diario	var11diario
33	diario	var16diario
34	diario	var17diario
35	diario	var24diario
36	diario	var14diario
37	diario	var2diario
38	diario	var1diario
39	diario	var8diario
40	diario	var20diario
41	diario	var18diario
42	diario	var6diario
43	diario	var10diario
44	diario	var19diario
45	diario	var23diario
46	diario	var5diario
47	diario	var15diario
48	diario	var4diario
49	mensual	var23mensual
50	mensual	var22mensual
51	mensual	var21mensual
52	mensual	var12mensual
53	mensual	var13mensual
54	mensual	var19mensual
55	mensual	var8mensual
56	mensual	var14mensual
57	mensual	var11mensual
58	mensual	var20mensual
59	mensual	var18mensual
60	mensual	var16mensual
61	mensual	var6mensual
62	mensual	var7mensual
63	mensual	var9mensual
64	mensual	var17mensual
65	mensual	var5mensual
66	mensual	var15mensual
67	mensual	var2mensual
68	mensual	var24mensual
69	mensual	var1mensual
70	mensual	var4mensual
71	mensual	var3mensual
72	mensual	var10mensual
73	variable	curvadescarga
74	variable	control
75	variable	unidad
76	variable	variable
77	formato	fecha
78	formato	hora
79	formato	formato
80	formato	clasificacion
81	formato	extension
82	formato	delimitador
83	formato	asociacion
84	datalogger	datalogger
85	datalogger	marca
86	sensor	tipo
87	sensor	sensor
88	sensor	marca
89	estacion	estacion
90	estacion	provincia
91	estacion	tipo
92	estacion	sistema
93	estacion	cuenca
94	estacion	sistemacuenca
95	medicion	var20medicion
96	medicion	var6medicion
97	medicion	var1medicion
98	medicion	var8medicion
99	medicion	medicion
100	medicion	var5medicion
101	medicion	var18medicion
102	medicion	var19medicion
103	medicion	var10medicion
104	medicion	var16medicion
105	medicion	var17medicion
106	medicion	reportevalidacion
107	medicion	var24medicion
108	medicion	var2medicion
109	medicion	cursordbclima
110	medicion	var7medicion
111	medicion	var11medicion
112	medicion	var23medicion
113	medicion	var15medicion
114	medicion	var22medicion
115	medicion	var12medicion
116	medicion	var14medicion
117	medicion	cursoremaaphidro
118	medicion	var13medicion
119	medicion	curvadescarga
120	medicion	var21medicion
121	medicion	var4medicion
122	medicion	var9medicion
123	medicion	var3medicion
124	medicion	caudalviaestacion
125	vacios	vacios
126	vacios	consulta
127	frecuencia	frecuencia
128	importacion	importaciontemp
129	importacion	importacion
130	validacion	var24validado
131	validacion	var19validado
132	validacion	var14validado
133	validacion	var13validado
134	validacion	validacion
135	validacion	var10validado
136	validacion	var16validado
137	validacion	var11validado
138	validacion	var21validado
139	validacion	var1validado
140	validacion	var2validado
141	validacion	var3validado
142	validacion	var15validado
143	validacion	var5validado
144	validacion	var4validado
145	validacion	var8validado
146	validacion	var20validado
147	validacion	comentariovalidacion
148	validacion	var7validado
149	validacion	var12validado
150	validacion	var17validado
151	validacion	var18validado
152	validacion	var23validado
153	validacion	consulta
154	validacion	var9validado
155	validacion	var22validado
156	validacion	var6validado
157	temporal	datos
158	anuarios	radiacionmaxima
159	anuarios	temperaturaaire
160	anuarios	radiacionsolar
161	anuarios	temperaturaagua
162	anuarios	radiacionminima
163	anuarios	caudal
164	anuarios	presionatmosferica
165	anuarios	humedadsuelo
166	anuarios	viento
167	anuarios	precipitacion
168	anuarios	nivelagua
169	anuarios	humedadaire
170	instalacion	instalacion
171	bitacora	bitacora
172	cruce	cruce
173	registro	logmedicion
174	reportes	consultagenericafecha
175	reportes	consultagenericafechahora
176	admin	logentry
177	auth	permission
178	auth	user
179	auth	group
180	contenttypes	contenttype
181	sessions	session
182	telemetria	configvisualizar
183	medicion	vientopolar
184	telemetria	alarmaestado
186	telemetria	alarmatipoestado
187	telemetria	alarmaemail
185	telemetria	variable
188	telemetria	televariables
189	horario	var30horario
190	horario	var29horario
191	horario	var27horario
192	horario	var25horario
193	horario	var28horario
194	horario	var31horario
195	horario	var26horario
196	diario	var27diario
197	diario	var29diario
198	diario	var28diario
199	diario	var25diario
200	diario	var31diario
201	diario	var26diario
202	diario	var30diario
203	mensual	var30mensual
204	mensual	var28mensual
205	mensual	var26mensual
206	mensual	var27mensual
207	mensual	var29mensual
208	mensual	var31mensual
209	mensual	var25mensual
210	medicion	var30medicion
211	medicion	var27medicion
212	medicion	var25medicion
213	medicion	var29medicion
214	medicion	var31medicion
215	medicion	var28medicion
216	medicion	var26medicion
217	validacion	var25validado
218	validacion	var28validado
219	validacion	var30validado
220	validacion	var31validado
221	validacion	var29validado
222	validacion	var27validado
223	validacion	var26validado
224	horario	var106horario
225	horario	var107horario
226	horario	var102horario
227	horario	var104horario
228	horario	var103horario
229	horario	var101horario
230	horario	var105horario
231	diario	var102diario
232	diario	var106diario
233	diario	var104diario
234	diario	var107diario
235	diario	var101diario
236	diario	var105diario
237	diario	var103diario
238	mensual	var107mensual
239	mensual	var106mensual
240	mensual	var101mensual
241	mensual	var105mensual
242	mensual	var103mensual
243	mensual	var102mensual
244	mensual	var104mensual
245	medicion	var103medicion
246	medicion	var105medicion
247	medicion	var106medicion
248	medicion	var101medicion
249	medicion	var104medicion
250	medicion	var107medicion
251	medicion	var102medicion
252	validacion	var103validado
253	validacion	var106validado
254	validacion	var107validado
255	validacion	var101validado
256	validacion	var105validado
257	validacion	var102validado
258	validacion	var104validado
259	calidad	estacionvariable
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 259, true);


--
-- PostgreSQL database dump complete
--

