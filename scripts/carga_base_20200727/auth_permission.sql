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
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add var16 horario	1	add_var16horario
2	Can change var16 horario	1	change_var16horario
3	Can delete var16 horario	1	delete_var16horario
4	Can add var21 horario	2	add_var21horario
5	Can change var21 horario	2	change_var21horario
6	Can delete var21 horario	2	delete_var21horario
7	Can add var7 horario	3	add_var7horario
8	Can change var7 horario	3	change_var7horario
9	Can delete var7 horario	3	delete_var7horario
10	Can add var5 horario	4	add_var5horario
11	Can change var5 horario	4	change_var5horario
12	Can delete var5 horario	4	delete_var5horario
13	Can add var12 horario	5	add_var12horario
14	Can change var12 horario	5	change_var12horario
15	Can delete var12 horario	5	delete_var12horario
16	Can add var19 horario	6	add_var19horario
17	Can change var19 horario	6	change_var19horario
18	Can delete var19 horario	6	delete_var19horario
19	Can add var22 horario	7	add_var22horario
20	Can change var22 horario	7	change_var22horario
21	Can delete var22 horario	7	delete_var22horario
22	Can add var6 horario	8	add_var6horario
23	Can change var6 horario	8	change_var6horario
24	Can delete var6 horario	8	delete_var6horario
25	Can add var14 horario	9	add_var14horario
26	Can change var14 horario	9	change_var14horario
27	Can delete var14 horario	9	delete_var14horario
28	Can add var9 horario	10	add_var9horario
29	Can change var9 horario	10	change_var9horario
30	Can delete var9 horario	10	delete_var9horario
31	Can add var13 horario	11	add_var13horario
32	Can change var13 horario	11	change_var13horario
33	Can delete var13 horario	11	delete_var13horario
34	Can add var2 horario	12	add_var2horario
35	Can change var2 horario	12	change_var2horario
36	Can delete var2 horario	12	delete_var2horario
37	Can add var4 horario	13	add_var4horario
38	Can change var4 horario	13	change_var4horario
39	Can delete var4 horario	13	delete_var4horario
40	Can add var11 horario	14	add_var11horario
41	Can change var11 horario	14	change_var11horario
42	Can delete var11 horario	14	delete_var11horario
43	Can add var20 horario	15	add_var20horario
44	Can change var20 horario	15	change_var20horario
45	Can delete var20 horario	15	delete_var20horario
46	Can add var8 horario	16	add_var8horario
47	Can change var8 horario	16	change_var8horario
48	Can delete var8 horario	16	delete_var8horario
49	Can add var23 horario	17	add_var23horario
50	Can change var23 horario	17	change_var23horario
51	Can delete var23 horario	17	delete_var23horario
52	Can add var24 horario	18	add_var24horario
53	Can change var24 horario	18	change_var24horario
54	Can delete var24 horario	18	delete_var24horario
55	Can add var18 horario	19	add_var18horario
56	Can change var18 horario	19	change_var18horario
57	Can delete var18 horario	19	delete_var18horario
58	Can add var1 horario	20	add_var1horario
59	Can change var1 horario	20	change_var1horario
60	Can delete var1 horario	20	delete_var1horario
61	Can add var15 horario	21	add_var15horario
62	Can change var15 horario	21	change_var15horario
63	Can delete var15 horario	21	delete_var15horario
64	Can add var17 horario	22	add_var17horario
65	Can change var17 horario	22	change_var17horario
66	Can delete var17 horario	22	delete_var17horario
67	Can add var3 horario	23	add_var3horario
68	Can change var3 horario	23	change_var3horario
69	Can delete var3 horario	23	delete_var3horario
70	Can add var10 horario	24	add_var10horario
71	Can change var10 horario	24	change_var10horario
72	Can delete var10 horario	24	delete_var10horario
73	Can add var3 diario	25	add_var3diario
74	Can change var3 diario	25	change_var3diario
75	Can delete var3 diario	25	delete_var3diario
76	Can add var7 diario	26	add_var7diario
77	Can change var7 diario	26	change_var7diario
78	Can delete var7 diario	26	delete_var7diario
79	Can add var13 diario	27	add_var13diario
80	Can change var13 diario	27	change_var13diario
81	Can delete var13 diario	27	delete_var13diario
82	Can add var9 diario	28	add_var9diario
83	Can change var9 diario	28	change_var9diario
84	Can delete var9 diario	28	delete_var9diario
85	Can add var21 diario	29	add_var21diario
86	Can change var21 diario	29	change_var21diario
87	Can delete var21 diario	29	delete_var21diario
88	Can add var12 diario	30	add_var12diario
89	Can change var12 diario	30	change_var12diario
90	Can delete var12 diario	30	delete_var12diario
91	Can add var22 diario	31	add_var22diario
92	Can change var22 diario	31	change_var22diario
93	Can delete var22 diario	31	delete_var22diario
94	Can add var11 diario	32	add_var11diario
95	Can change var11 diario	32	change_var11diario
96	Can delete var11 diario	32	delete_var11diario
97	Can add var16 diario	33	add_var16diario
98	Can change var16 diario	33	change_var16diario
99	Can delete var16 diario	33	delete_var16diario
100	Can add var17 diario	34	add_var17diario
101	Can change var17 diario	34	change_var17diario
102	Can delete var17 diario	34	delete_var17diario
103	Can add var24 diario	35	add_var24diario
104	Can change var24 diario	35	change_var24diario
105	Can delete var24 diario	35	delete_var24diario
106	Can add var14 diario	36	add_var14diario
107	Can change var14 diario	36	change_var14diario
108	Can delete var14 diario	36	delete_var14diario
109	Can add var2 diario	37	add_var2diario
110	Can change var2 diario	37	change_var2diario
111	Can delete var2 diario	37	delete_var2diario
112	Can add var1 diario	38	add_var1diario
113	Can change var1 diario	38	change_var1diario
114	Can delete var1 diario	38	delete_var1diario
115	Can add var8 diario	39	add_var8diario
116	Can change var8 diario	39	change_var8diario
117	Can delete var8 diario	39	delete_var8diario
118	Can add var20 diario	40	add_var20diario
119	Can change var20 diario	40	change_var20diario
120	Can delete var20 diario	40	delete_var20diario
121	Can add var18 diario	41	add_var18diario
122	Can change var18 diario	41	change_var18diario
123	Can delete var18 diario	41	delete_var18diario
124	Can add var6 diario	42	add_var6diario
125	Can change var6 diario	42	change_var6diario
126	Can delete var6 diario	42	delete_var6diario
127	Can add var10 diario	43	add_var10diario
128	Can change var10 diario	43	change_var10diario
129	Can delete var10 diario	43	delete_var10diario
130	Can add var19 diario	44	add_var19diario
131	Can change var19 diario	44	change_var19diario
132	Can delete var19 diario	44	delete_var19diario
133	Can add var23 diario	45	add_var23diario
134	Can change var23 diario	45	change_var23diario
135	Can delete var23 diario	45	delete_var23diario
136	Can add var5 diario	46	add_var5diario
137	Can change var5 diario	46	change_var5diario
138	Can delete var5 diario	46	delete_var5diario
139	Can add var15 diario	47	add_var15diario
140	Can change var15 diario	47	change_var15diario
141	Can delete var15 diario	47	delete_var15diario
142	Can add var4 diario	48	add_var4diario
143	Can change var4 diario	48	change_var4diario
144	Can delete var4 diario	48	delete_var4diario
145	Can add var23 mensual	49	add_var23mensual
146	Can change var23 mensual	49	change_var23mensual
147	Can delete var23 mensual	49	delete_var23mensual
148	Can add var22 mensual	50	add_var22mensual
149	Can change var22 mensual	50	change_var22mensual
150	Can delete var22 mensual	50	delete_var22mensual
151	Can add var21 mensual	51	add_var21mensual
152	Can change var21 mensual	51	change_var21mensual
153	Can delete var21 mensual	51	delete_var21mensual
154	Can add var12 mensual	52	add_var12mensual
155	Can change var12 mensual	52	change_var12mensual
156	Can delete var12 mensual	52	delete_var12mensual
157	Can add var13 mensual	53	add_var13mensual
158	Can change var13 mensual	53	change_var13mensual
159	Can delete var13 mensual	53	delete_var13mensual
160	Can add var19 mensual	54	add_var19mensual
161	Can change var19 mensual	54	change_var19mensual
162	Can delete var19 mensual	54	delete_var19mensual
163	Can add var8 mensual	55	add_var8mensual
164	Can change var8 mensual	55	change_var8mensual
165	Can delete var8 mensual	55	delete_var8mensual
166	Can add var14 mensual	56	add_var14mensual
167	Can change var14 mensual	56	change_var14mensual
168	Can delete var14 mensual	56	delete_var14mensual
169	Can add var11 mensual	57	add_var11mensual
170	Can change var11 mensual	57	change_var11mensual
171	Can delete var11 mensual	57	delete_var11mensual
172	Can add var20 mensual	58	add_var20mensual
173	Can change var20 mensual	58	change_var20mensual
174	Can delete var20 mensual	58	delete_var20mensual
175	Can add var18 mensual	59	add_var18mensual
176	Can change var18 mensual	59	change_var18mensual
177	Can delete var18 mensual	59	delete_var18mensual
178	Can add var16 mensual	60	add_var16mensual
179	Can change var16 mensual	60	change_var16mensual
180	Can delete var16 mensual	60	delete_var16mensual
181	Can add var6 mensual	61	add_var6mensual
182	Can change var6 mensual	61	change_var6mensual
183	Can delete var6 mensual	61	delete_var6mensual
184	Can add var7 mensual	62	add_var7mensual
185	Can change var7 mensual	62	change_var7mensual
186	Can delete var7 mensual	62	delete_var7mensual
187	Can add var9 mensual	63	add_var9mensual
188	Can change var9 mensual	63	change_var9mensual
189	Can delete var9 mensual	63	delete_var9mensual
190	Can add var17 mensual	64	add_var17mensual
191	Can change var17 mensual	64	change_var17mensual
192	Can delete var17 mensual	64	delete_var17mensual
193	Can add var5 mensual	65	add_var5mensual
194	Can change var5 mensual	65	change_var5mensual
195	Can delete var5 mensual	65	delete_var5mensual
196	Can add var15 mensual	66	add_var15mensual
197	Can change var15 mensual	66	change_var15mensual
198	Can delete var15 mensual	66	delete_var15mensual
199	Can add var2 mensual	67	add_var2mensual
200	Can change var2 mensual	67	change_var2mensual
201	Can delete var2 mensual	67	delete_var2mensual
202	Can add var24 mensual	68	add_var24mensual
203	Can change var24 mensual	68	change_var24mensual
204	Can delete var24 mensual	68	delete_var24mensual
205	Can add var1 mensual	69	add_var1mensual
206	Can change var1 mensual	69	change_var1mensual
207	Can delete var1 mensual	69	delete_var1mensual
208	Can add var4 mensual	70	add_var4mensual
209	Can change var4 mensual	70	change_var4mensual
210	Can delete var4 mensual	70	delete_var4mensual
211	Can add var3 mensual	71	add_var3mensual
212	Can change var3 mensual	71	change_var3mensual
213	Can delete var3 mensual	71	delete_var3mensual
214	Can add var10 mensual	72	add_var10mensual
215	Can change var10 mensual	72	change_var10mensual
216	Can delete var10 mensual	72	delete_var10mensual
217	Can add curva descarga	73	add_curvadescarga
218	Can change curva descarga	73	change_curvadescarga
219	Can delete curva descarga	73	delete_curvadescarga
220	Can add control	74	add_control
221	Can change control	74	change_control
222	Can delete control	74	delete_control
223	Can add unidad	75	add_unidad
224	Can change unidad	75	change_unidad
225	Can delete unidad	75	delete_unidad
226	Can add variable	76	add_variable
227	Can change variable	76	change_variable
228	Can delete variable	76	delete_variable
229	Can add fecha	77	add_fecha
230	Can change fecha	77	change_fecha
231	Can delete fecha	77	delete_fecha
232	Can add hora	78	add_hora
233	Can change hora	78	change_hora
234	Can delete hora	78	delete_hora
235	Can add formato	79	add_formato
236	Can change formato	79	change_formato
237	Can delete formato	79	delete_formato
238	Can add clasificacion	80	add_clasificacion
239	Can change clasificacion	80	change_clasificacion
240	Can delete clasificacion	80	delete_clasificacion
241	Can add extension	81	add_extension
242	Can change extension	81	change_extension
243	Can delete extension	81	delete_extension
244	Can add delimitador	82	add_delimitador
245	Can change delimitador	82	change_delimitador
246	Can delete delimitador	82	delete_delimitador
247	Can add asociacion	83	add_asociacion
248	Can change asociacion	83	change_asociacion
249	Can delete asociacion	83	delete_asociacion
250	Can add datalogger	84	add_datalogger
251	Can change datalogger	84	change_datalogger
252	Can delete datalogger	84	delete_datalogger
253	Can add marca	85	add_marca
254	Can change marca	85	change_marca
255	Can delete marca	85	delete_marca
256	Can add tipo	86	add_tipo
257	Can change tipo	86	change_tipo
258	Can delete tipo	86	delete_tipo
259	Can add sensor	87	add_sensor
260	Can change sensor	87	change_sensor
261	Can delete sensor	87	delete_sensor
262	Can add marca	88	add_marca
263	Can change marca	88	change_marca
264	Can delete marca	88	delete_marca
265	Can add estacion	89	add_estacion
266	Can change estacion	89	change_estacion
267	Can delete estacion	89	delete_estacion
268	Can add provincia	90	add_provincia
269	Can change provincia	90	change_provincia
270	Can delete provincia	90	delete_provincia
271	Can add tipo	91	add_tipo
272	Can change tipo	91	change_tipo
273	Can delete tipo	91	delete_tipo
274	Can add sistema	92	add_sistema
275	Can change sistema	92	change_sistema
276	Can delete sistema	92	delete_sistema
277	Can add cuenca	93	add_cuenca
278	Can change cuenca	93	change_cuenca
279	Can delete cuenca	93	delete_cuenca
280	Can add sistema cuenca	94	add_sistemacuenca
281	Can change sistema cuenca	94	change_sistemacuenca
282	Can delete sistema cuenca	94	delete_sistemacuenca
283	Can add var20 medicion	95	add_var20medicion
284	Can change var20 medicion	95	change_var20medicion
285	Can delete var20 medicion	95	delete_var20medicion
286	Can add var6 medicion	96	add_var6medicion
287	Can change var6 medicion	96	change_var6medicion
288	Can delete var6 medicion	96	delete_var6medicion
289	Can add var1 medicion	97	add_var1medicion
290	Can change var1 medicion	97	change_var1medicion
291	Can delete var1 medicion	97	delete_var1medicion
292	Can add var8 medicion	98	add_var8medicion
293	Can change var8 medicion	98	change_var8medicion
294	Can delete var8 medicion	98	delete_var8medicion
295	Can add medicion	99	add_medicion
296	Can change medicion	99	change_medicion
297	Can delete medicion	99	delete_medicion
298	Can add var5 medicion	100	add_var5medicion
299	Can change var5 medicion	100	change_var5medicion
300	Can delete var5 medicion	100	delete_var5medicion
301	Can add var18 medicion	101	add_var18medicion
302	Can change var18 medicion	101	change_var18medicion
303	Can delete var18 medicion	101	delete_var18medicion
304	Can add var19 medicion	102	add_var19medicion
305	Can change var19 medicion	102	change_var19medicion
306	Can delete var19 medicion	102	delete_var19medicion
307	Can add var10 medicion	103	add_var10medicion
308	Can change var10 medicion	103	change_var10medicion
309	Can delete var10 medicion	103	delete_var10medicion
310	Can add var16 medicion	104	add_var16medicion
311	Can change var16 medicion	104	change_var16medicion
312	Can delete var16 medicion	104	delete_var16medicion
313	Can add var17 medicion	105	add_var17medicion
314	Can change var17 medicion	105	change_var17medicion
315	Can delete var17 medicion	105	delete_var17medicion
316	Can add reporte validacion	106	add_reportevalidacion
317	Can change reporte validacion	106	change_reportevalidacion
318	Can delete reporte validacion	106	delete_reportevalidacion
319	Can add var24 medicion	107	add_var24medicion
320	Can change var24 medicion	107	change_var24medicion
321	Can delete var24 medicion	107	delete_var24medicion
322	Can add var2 medicion	108	add_var2medicion
323	Can change var2 medicion	108	change_var2medicion
324	Can delete var2 medicion	108	delete_var2medicion
325	Can add cursor dbclima	109	add_cursordbclima
326	Can change cursor dbclima	109	change_cursordbclima
327	Can delete cursor dbclima	109	delete_cursordbclima
328	Can add var7 medicion	110	add_var7medicion
329	Can change var7 medicion	110	change_var7medicion
330	Can delete var7 medicion	110	delete_var7medicion
331	Can add var11 medicion	111	add_var11medicion
332	Can change var11 medicion	111	change_var11medicion
333	Can delete var11 medicion	111	delete_var11medicion
334	Can add var23 medicion	112	add_var23medicion
335	Can change var23 medicion	112	change_var23medicion
336	Can delete var23 medicion	112	delete_var23medicion
337	Can add var15 medicion	113	add_var15medicion
338	Can change var15 medicion	113	change_var15medicion
339	Can delete var15 medicion	113	delete_var15medicion
340	Can add var22 medicion	114	add_var22medicion
341	Can change var22 medicion	114	change_var22medicion
342	Can delete var22 medicion	114	delete_var22medicion
343	Can add var12 medicion	115	add_var12medicion
344	Can change var12 medicion	115	change_var12medicion
345	Can delete var12 medicion	115	delete_var12medicion
346	Can add var14 medicion	116	add_var14medicion
347	Can change var14 medicion	116	change_var14medicion
348	Can delete var14 medicion	116	delete_var14medicion
349	Can add cursor emaaphidro	117	add_cursoremaaphidro
350	Can change cursor emaaphidro	117	change_cursoremaaphidro
351	Can delete cursor emaaphidro	117	delete_cursoremaaphidro
352	Can add var13 medicion	118	add_var13medicion
353	Can change var13 medicion	118	change_var13medicion
354	Can delete var13 medicion	118	delete_var13medicion
355	Can add curva descarga	119	add_curvadescarga
356	Can change curva descarga	119	change_curvadescarga
357	Can delete curva descarga	119	delete_curvadescarga
358	Can add var21 medicion	120	add_var21medicion
359	Can change var21 medicion	120	change_var21medicion
360	Can delete var21 medicion	120	delete_var21medicion
361	Can add var4 medicion	121	add_var4medicion
362	Can change var4 medicion	121	change_var4medicion
363	Can delete var4 medicion	121	delete_var4medicion
364	Can add var9 medicion	122	add_var9medicion
365	Can change var9 medicion	122	change_var9medicion
366	Can delete var9 medicion	122	delete_var9medicion
367	Can add var3 medicion	123	add_var3medicion
368	Can change var3 medicion	123	change_var3medicion
369	Can delete var3 medicion	123	delete_var3medicion
370	Can add caudal via estacion	124	add_caudalviaestacion
371	Can change caudal via estacion	124	change_caudalviaestacion
372	Can delete caudal via estacion	124	delete_caudalviaestacion
373	Can add vacios	125	add_vacios
374	Can change vacios	125	change_vacios
375	Can delete vacios	125	delete_vacios
376	Can add consulta	126	add_consulta
377	Can change consulta	126	change_consulta
378	Can delete consulta	126	delete_consulta
379	Can add frecuencia	127	add_frecuencia
380	Can change frecuencia	127	change_frecuencia
381	Can delete frecuencia	127	delete_frecuencia
382	Can add importacion temp	128	add_importaciontemp
383	Can change importacion temp	128	change_importaciontemp
384	Can delete importacion temp	128	delete_importaciontemp
385	Can add importacion	129	add_importacion
386	Can change importacion	129	change_importacion
387	Can delete importacion	129	delete_importacion
388	Can add var24 validado	130	add_var24validado
389	Can change var24 validado	130	change_var24validado
390	Can delete var24 validado	130	delete_var24validado
391	Can add var19 validado	131	add_var19validado
392	Can change var19 validado	131	change_var19validado
393	Can delete var19 validado	131	delete_var19validado
394	Can add var14 validado	132	add_var14validado
395	Can change var14 validado	132	change_var14validado
396	Can delete var14 validado	132	delete_var14validado
397	Can add var13 validado	133	add_var13validado
398	Can change var13 validado	133	change_var13validado
399	Can delete var13 validado	133	delete_var13validado
400	Can add validacion	134	add_validacion
401	Can change validacion	134	change_validacion
402	Can delete validacion	134	delete_validacion
403	Can add var10 validado	135	add_var10validado
404	Can change var10 validado	135	change_var10validado
405	Can delete var10 validado	135	delete_var10validado
406	Can add var16 validado	136	add_var16validado
407	Can change var16 validado	136	change_var16validado
408	Can delete var16 validado	136	delete_var16validado
409	Can add var11 validado	137	add_var11validado
410	Can change var11 validado	137	change_var11validado
411	Can delete var11 validado	137	delete_var11validado
412	Can add var21 validado	138	add_var21validado
413	Can change var21 validado	138	change_var21validado
414	Can delete var21 validado	138	delete_var21validado
415	Can add var1 validado	139	add_var1validado
416	Can change var1 validado	139	change_var1validado
417	Can delete var1 validado	139	delete_var1validado
418	Can add var2 validado	140	add_var2validado
419	Can change var2 validado	140	change_var2validado
420	Can delete var2 validado	140	delete_var2validado
421	Can add var3 validado	141	add_var3validado
422	Can change var3 validado	141	change_var3validado
423	Can delete var3 validado	141	delete_var3validado
424	Can add var15 validado	142	add_var15validado
425	Can change var15 validado	142	change_var15validado
426	Can delete var15 validado	142	delete_var15validado
427	Can add var5 validado	143	add_var5validado
428	Can change var5 validado	143	change_var5validado
429	Can delete var5 validado	143	delete_var5validado
430	Can add var4 validado	144	add_var4validado
431	Can change var4 validado	144	change_var4validado
432	Can delete var4 validado	144	delete_var4validado
433	Can add var8 validado	145	add_var8validado
434	Can change var8 validado	145	change_var8validado
435	Can delete var8 validado	145	delete_var8validado
436	Can add var20 validado	146	add_var20validado
437	Can change var20 validado	146	change_var20validado
438	Can delete var20 validado	146	delete_var20validado
439	Can add comentario validacion	147	add_comentariovalidacion
440	Can change comentario validacion	147	change_comentariovalidacion
441	Can delete comentario validacion	147	delete_comentariovalidacion
442	Can add var7 validado	148	add_var7validado
443	Can change var7 validado	148	change_var7validado
444	Can delete var7 validado	148	delete_var7validado
445	Can add var12 validado	149	add_var12validado
446	Can change var12 validado	149	change_var12validado
447	Can delete var12 validado	149	delete_var12validado
448	Can add var17 validado	150	add_var17validado
449	Can change var17 validado	150	change_var17validado
450	Can delete var17 validado	150	delete_var17validado
451	Can add var18 validado	151	add_var18validado
452	Can change var18 validado	151	change_var18validado
453	Can delete var18 validado	151	delete_var18validado
454	Can add var23 validado	152	add_var23validado
455	Can change var23 validado	152	change_var23validado
456	Can delete var23 validado	152	delete_var23validado
457	Can add consulta	153	add_consulta
458	Can change consulta	153	change_consulta
459	Can delete consulta	153	delete_consulta
460	Can add var9 validado	154	add_var9validado
461	Can change var9 validado	154	change_var9validado
462	Can delete var9 validado	154	delete_var9validado
463	Can add var22 validado	155	add_var22validado
464	Can change var22 validado	155	change_var22validado
465	Can delete var22 validado	155	delete_var22validado
466	Can add var6 validado	156	add_var6validado
467	Can change var6 validado	156	change_var6validado
468	Can delete var6 validado	156	delete_var6validado
469	Can add datos	157	add_datos
470	Can change datos	157	change_datos
471	Can delete datos	157	delete_datos
472	Can add radiacion maxima	158	add_radiacionmaxima
473	Can change radiacion maxima	158	change_radiacionmaxima
474	Can delete radiacion maxima	158	delete_radiacionmaxima
475	Can add temperatura aire	159	add_temperaturaaire
476	Can change temperatura aire	159	change_temperaturaaire
477	Can delete temperatura aire	159	delete_temperaturaaire
478	Can add radiacion solar	160	add_radiacionsolar
479	Can change radiacion solar	160	change_radiacionsolar
480	Can delete radiacion solar	160	delete_radiacionsolar
481	Can add temperatura agua	161	add_temperaturaagua
482	Can change temperatura agua	161	change_temperaturaagua
483	Can delete temperatura agua	161	delete_temperaturaagua
484	Can add radiacion minima	162	add_radiacionminima
485	Can change radiacion minima	162	change_radiacionminima
486	Can delete radiacion minima	162	delete_radiacionminima
487	Can add caudal	163	add_caudal
488	Can change caudal	163	change_caudal
489	Can delete caudal	163	delete_caudal
490	Can add presion atmosferica	164	add_presionatmosferica
491	Can change presion atmosferica	164	change_presionatmosferica
492	Can delete presion atmosferica	164	delete_presionatmosferica
493	Can add humedad suelo	165	add_humedadsuelo
494	Can change humedad suelo	165	change_humedadsuelo
495	Can delete humedad suelo	165	delete_humedadsuelo
496	Can add viento	166	add_viento
497	Can change viento	166	change_viento
498	Can delete viento	166	delete_viento
499	Can add precipitacion	167	add_precipitacion
500	Can change precipitacion	167	change_precipitacion
501	Can delete precipitacion	167	delete_precipitacion
502	Can add nivel agua	168	add_nivelagua
503	Can change nivel agua	168	change_nivelagua
504	Can delete nivel agua	168	delete_nivelagua
505	Can add humedad aire	169	add_humedadaire
506	Can change humedad aire	169	change_humedadaire
507	Can delete humedad aire	169	delete_humedadaire
508	Can add instalacion	170	add_instalacion
509	Can change instalacion	170	change_instalacion
510	Can delete instalacion	170	delete_instalacion
511	Can add bitacora	171	add_bitacora
512	Can change bitacora	171	change_bitacora
513	Can delete bitacora	171	delete_bitacora
514	Can add cruce	172	add_cruce
515	Can change cruce	172	change_cruce
516	Can delete cruce	172	delete_cruce
517	Can add log medicion	173	add_logmedicion
518	Can change log medicion	173	change_logmedicion
519	Can delete log medicion	173	delete_logmedicion
520	Can add consulta generica fecha	174	add_consultagenericafecha
521	Can change consulta generica fecha	174	change_consultagenericafecha
522	Can delete consulta generica fecha	174	delete_consultagenericafecha
523	Can add consulta generica fecha hora	175	add_consultagenericafechahora
524	Can change consulta generica fecha hora	175	change_consultagenericafechahora
525	Can delete consulta generica fecha hora	175	delete_consultagenericafechahora
526	Can add log entry	176	add_logentry
527	Can change log entry	176	change_logentry
528	Can delete log entry	176	delete_logentry
529	Can add permission	177	add_permission
530	Can change permission	177	change_permission
531	Can delete permission	177	delete_permission
532	Can add user	178	add_user
533	Can change user	178	change_user
534	Can delete user	178	delete_user
535	Can add group	179	add_group
536	Can change group	179	change_group
537	Can delete group	179	delete_group
538	Can add content type	180	add_contenttype
539	Can change content type	180	change_contenttype
540	Can delete content type	180	delete_contenttype
541	Can add session	181	add_session
542	Can change session	181	change_session
543	Can delete session	181	delete_session
544	Can add config visualizar	182	add_configvisualizar
545	Can change config visualizar	182	change_configvisualizar
546	Can delete config visualizar	182	delete_configvisualizar
547	Can add viento polar	183	add_vientopolar
548	Can change viento polar	183	change_vientopolar
549	Can delete viento polar	183	delete_vientopolar
550	Can add alarma estado	184	add_alarmaestado
551	Can change alarma estado	184	change_alarmaestado
552	Can delete alarma estado	184	delete_alarmaestado
553	Can add alarma variable	185	add_alarmavariable
554	Can change alarma variable	185	change_alarmavariable
555	Can delete alarma variable	185	delete_alarmavariable
556	Can add alarma tipo estado	186	add_alarmatipoestado
557	Can change alarma tipo estado	186	change_alarmatipoestado
558	Can delete alarma tipo estado	186	delete_alarmatipoestado
559	Can add alarma email	187	add_alarmaemail
560	Can change alarma email	187	change_alarmaemail
561	Can delete alarma email	187	delete_alarmaemail
562	Can add variable	185	add_variable
563	Can change variable	185	change_variable
564	Can delete variable	185	delete_variable
565	Can add tele variables	188	add_televariables
566	Can change tele variables	188	change_televariables
567	Can delete tele variables	188	delete_televariables
568	Can add var30 horario	189	add_var30horario
569	Can change var30 horario	189	change_var30horario
570	Can delete var30 horario	189	delete_var30horario
571	Can add var29 horario	190	add_var29horario
572	Can change var29 horario	190	change_var29horario
573	Can delete var29 horario	190	delete_var29horario
574	Can add var27 horario	191	add_var27horario
575	Can change var27 horario	191	change_var27horario
576	Can delete var27 horario	191	delete_var27horario
577	Can add var25 horario	192	add_var25horario
578	Can change var25 horario	192	change_var25horario
579	Can delete var25 horario	192	delete_var25horario
580	Can add var28 horario	193	add_var28horario
581	Can change var28 horario	193	change_var28horario
582	Can delete var28 horario	193	delete_var28horario
583	Can add var31 horario	194	add_var31horario
584	Can change var31 horario	194	change_var31horario
585	Can delete var31 horario	194	delete_var31horario
586	Can add var26 horario	195	add_var26horario
587	Can change var26 horario	195	change_var26horario
588	Can delete var26 horario	195	delete_var26horario
589	Can add var27 diario	196	add_var27diario
590	Can change var27 diario	196	change_var27diario
591	Can delete var27 diario	196	delete_var27diario
592	Can add var29 diario	197	add_var29diario
593	Can change var29 diario	197	change_var29diario
594	Can delete var29 diario	197	delete_var29diario
595	Can add var28 diario	198	add_var28diario
596	Can change var28 diario	198	change_var28diario
597	Can delete var28 diario	198	delete_var28diario
598	Can add var25 diario	199	add_var25diario
599	Can change var25 diario	199	change_var25diario
600	Can delete var25 diario	199	delete_var25diario
601	Can add var31 diario	200	add_var31diario
602	Can change var31 diario	200	change_var31diario
603	Can delete var31 diario	200	delete_var31diario
604	Can add var26 diario	201	add_var26diario
605	Can change var26 diario	201	change_var26diario
606	Can delete var26 diario	201	delete_var26diario
607	Can add var30 diario	202	add_var30diario
608	Can change var30 diario	202	change_var30diario
609	Can delete var30 diario	202	delete_var30diario
610	Can add var30 mensual	203	add_var30mensual
611	Can change var30 mensual	203	change_var30mensual
612	Can delete var30 mensual	203	delete_var30mensual
613	Can add var28 mensual	204	add_var28mensual
614	Can change var28 mensual	204	change_var28mensual
615	Can delete var28 mensual	204	delete_var28mensual
616	Can add var26 mensual	205	add_var26mensual
617	Can change var26 mensual	205	change_var26mensual
618	Can delete var26 mensual	205	delete_var26mensual
619	Can add var27 mensual	206	add_var27mensual
620	Can change var27 mensual	206	change_var27mensual
621	Can delete var27 mensual	206	delete_var27mensual
622	Can add var29 mensual	207	add_var29mensual
623	Can change var29 mensual	207	change_var29mensual
624	Can delete var29 mensual	207	delete_var29mensual
625	Can add var31 mensual	208	add_var31mensual
626	Can change var31 mensual	208	change_var31mensual
627	Can delete var31 mensual	208	delete_var31mensual
628	Can add var25 mensual	209	add_var25mensual
629	Can change var25 mensual	209	change_var25mensual
630	Can delete var25 mensual	209	delete_var25mensual
631	Can add var30 medicion	210	add_var30medicion
632	Can change var30 medicion	210	change_var30medicion
633	Can delete var30 medicion	210	delete_var30medicion
634	Can add var27 medicion	211	add_var27medicion
635	Can change var27 medicion	211	change_var27medicion
636	Can delete var27 medicion	211	delete_var27medicion
637	Can add var25 medicion	212	add_var25medicion
638	Can change var25 medicion	212	change_var25medicion
639	Can delete var25 medicion	212	delete_var25medicion
640	Can add var29 medicion	213	add_var29medicion
641	Can change var29 medicion	213	change_var29medicion
642	Can delete var29 medicion	213	delete_var29medicion
643	Can add var31 medicion	214	add_var31medicion
644	Can change var31 medicion	214	change_var31medicion
645	Can delete var31 medicion	214	delete_var31medicion
646	Can add var28 medicion	215	add_var28medicion
647	Can change var28 medicion	215	change_var28medicion
648	Can delete var28 medicion	215	delete_var28medicion
649	Can add var26 medicion	216	add_var26medicion
650	Can change var26 medicion	216	change_var26medicion
651	Can delete var26 medicion	216	delete_var26medicion
652	Can add var25 validado	217	add_var25validado
653	Can change var25 validado	217	change_var25validado
654	Can delete var25 validado	217	delete_var25validado
655	Can add var28 validado	218	add_var28validado
656	Can change var28 validado	218	change_var28validado
657	Can delete var28 validado	218	delete_var28validado
658	Can add var30 validado	219	add_var30validado
659	Can change var30 validado	219	change_var30validado
660	Can delete var30 validado	219	delete_var30validado
661	Can add var31 validado	220	add_var31validado
662	Can change var31 validado	220	change_var31validado
663	Can delete var31 validado	220	delete_var31validado
664	Can add var29 validado	221	add_var29validado
665	Can change var29 validado	221	change_var29validado
666	Can delete var29 validado	221	delete_var29validado
667	Can add var27 validado	222	add_var27validado
668	Can change var27 validado	222	change_var27validado
669	Can delete var27 validado	222	delete_var27validado
670	Can add var26 validado	223	add_var26validado
671	Can change var26 validado	223	change_var26validado
672	Can delete var26 validado	223	delete_var26validado
673	Can add var106 horario	224	add_var106horario
674	Can change var106 horario	224	change_var106horario
675	Can delete var106 horario	224	delete_var106horario
676	Can add var107 horario	225	add_var107horario
677	Can change var107 horario	225	change_var107horario
678	Can delete var107 horario	225	delete_var107horario
679	Can add var102 horario	226	add_var102horario
680	Can change var102 horario	226	change_var102horario
681	Can delete var102 horario	226	delete_var102horario
682	Can add var104 horario	227	add_var104horario
683	Can change var104 horario	227	change_var104horario
684	Can delete var104 horario	227	delete_var104horario
685	Can add var103 horario	228	add_var103horario
686	Can change var103 horario	228	change_var103horario
687	Can delete var103 horario	228	delete_var103horario
688	Can add var101 horario	229	add_var101horario
689	Can change var101 horario	229	change_var101horario
690	Can delete var101 horario	229	delete_var101horario
691	Can add var105 horario	230	add_var105horario
692	Can change var105 horario	230	change_var105horario
693	Can delete var105 horario	230	delete_var105horario
694	Can add var102 diario	231	add_var102diario
695	Can change var102 diario	231	change_var102diario
696	Can delete var102 diario	231	delete_var102diario
697	Can add var106 diario	232	add_var106diario
698	Can change var106 diario	232	change_var106diario
699	Can delete var106 diario	232	delete_var106diario
700	Can add var104 diario	233	add_var104diario
701	Can change var104 diario	233	change_var104diario
702	Can delete var104 diario	233	delete_var104diario
703	Can add var107 diario	234	add_var107diario
704	Can change var107 diario	234	change_var107diario
705	Can delete var107 diario	234	delete_var107diario
706	Can add var101 diario	235	add_var101diario
707	Can change var101 diario	235	change_var101diario
708	Can delete var101 diario	235	delete_var101diario
709	Can add var105 diario	236	add_var105diario
710	Can change var105 diario	236	change_var105diario
711	Can delete var105 diario	236	delete_var105diario
712	Can add var103 diario	237	add_var103diario
713	Can change var103 diario	237	change_var103diario
714	Can delete var103 diario	237	delete_var103diario
715	Can add var107 mensual	238	add_var107mensual
716	Can change var107 mensual	238	change_var107mensual
717	Can delete var107 mensual	238	delete_var107mensual
718	Can add var106 mensual	239	add_var106mensual
719	Can change var106 mensual	239	change_var106mensual
720	Can delete var106 mensual	239	delete_var106mensual
721	Can add var101 mensual	240	add_var101mensual
722	Can change var101 mensual	240	change_var101mensual
723	Can delete var101 mensual	240	delete_var101mensual
724	Can add var105 mensual	241	add_var105mensual
725	Can change var105 mensual	241	change_var105mensual
726	Can delete var105 mensual	241	delete_var105mensual
727	Can add var103 mensual	242	add_var103mensual
728	Can change var103 mensual	242	change_var103mensual
729	Can delete var103 mensual	242	delete_var103mensual
730	Can add var102 mensual	243	add_var102mensual
731	Can change var102 mensual	243	change_var102mensual
732	Can delete var102 mensual	243	delete_var102mensual
733	Can add var104 mensual	244	add_var104mensual
734	Can change var104 mensual	244	change_var104mensual
735	Can delete var104 mensual	244	delete_var104mensual
736	Can add var103 medicion	245	add_var103medicion
737	Can change var103 medicion	245	change_var103medicion
738	Can delete var103 medicion	245	delete_var103medicion
739	Can add var105 medicion	246	add_var105medicion
740	Can change var105 medicion	246	change_var105medicion
741	Can delete var105 medicion	246	delete_var105medicion
742	Can add var106 medicion	247	add_var106medicion
743	Can change var106 medicion	247	change_var106medicion
744	Can delete var106 medicion	247	delete_var106medicion
745	Can add var101 medicion	248	add_var101medicion
746	Can change var101 medicion	248	change_var101medicion
747	Can delete var101 medicion	248	delete_var101medicion
748	Can add var104 medicion	249	add_var104medicion
749	Can change var104 medicion	249	change_var104medicion
750	Can delete var104 medicion	249	delete_var104medicion
751	Can add var107 medicion	250	add_var107medicion
752	Can change var107 medicion	250	change_var107medicion
753	Can delete var107 medicion	250	delete_var107medicion
754	Can add var102 medicion	251	add_var102medicion
755	Can change var102 medicion	251	change_var102medicion
756	Can delete var102 medicion	251	delete_var102medicion
757	Can add var103 validado	252	add_var103validado
758	Can change var103 validado	252	change_var103validado
759	Can delete var103 validado	252	delete_var103validado
760	Can add var106 validado	253	add_var106validado
761	Can change var106 validado	253	change_var106validado
762	Can delete var106 validado	253	delete_var106validado
763	Can add var107 validado	254	add_var107validado
764	Can change var107 validado	254	change_var107validado
765	Can delete var107 validado	254	delete_var107validado
766	Can add var101 validado	255	add_var101validado
767	Can change var101 validado	255	change_var101validado
768	Can delete var101 validado	255	delete_var101validado
769	Can add var105 validado	256	add_var105validado
770	Can change var105 validado	256	change_var105validado
771	Can delete var105 validado	256	delete_var105validado
772	Can add var102 validado	257	add_var102validado
773	Can change var102 validado	257	change_var102validado
774	Can delete var102 validado	257	delete_var102validado
775	Can add var104 validado	258	add_var104validado
776	Can change var104 validado	258	change_var104validado
777	Can delete var104 validado	258	delete_var104validado
778	Can add estacion variable	259	add_estacionvariable
779	Can change estacion variable	259	change_estacionvariable
780	Can delete estacion variable	259	delete_estacionvariable
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 780, true);


--
-- PostgreSQL database dump complete
--

