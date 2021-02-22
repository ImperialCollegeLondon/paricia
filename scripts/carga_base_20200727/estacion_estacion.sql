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
-- Data for Name: estacion_estacion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estacion_estacion (est_id, est_codigo, est_nombre, est_estado, est_longitud, est_latitud, est_altura, est_ficha, provincia_id, sistemacuenca_id, tipo_id, est_externa) FROM stdin;
1	C01	Maucatambo	t	517419.37	9924715.44	3840		19	23	2	f
3	C03	Rumihurco	f	497475.40	9986185.39	3122		9	2	2	f
5	C05	Bellavista	t	504265.47	9979906.20	2960		9	3	2	f
9	C09	Mica Campamento	f	530496.39	9942059.04	3995		19	12	2	f
10	C10	La Mica Presa	t	530267.20	9939548.97	3922		19	12	2	f
12	C12	Quijos Campamento	t	550490.30	9947685.48	2596		19	21	2	f
13	C13	Salve Faccha	t	538701.84	9974481.34	3888		19	19	2	f
14	H01	Rumihurco Media	f	496175.58	9985335.35	3316		9	16	3	f
15	H04	Rumipamba Baja	f	498225.98	9980136.00	3081		9	17	3	f
16	H07	Conocoto	f	503685.28	9968843.14	2460		9	9	3	f
666	CAL001	Boya Salve Faccha	t	\N	\N	\N	\N	19	19	5	f
17	H08	Tránsito	f	492270.13	9967886.69	2960		9	4	3	f
18	H10	Capulí	f	495684.73	9967438.74	2880		9	4	3	f
21	H15	Ramon Huañuna	f	533533.37	9933428.27	3691		19	12	3	f
22	H16	Antisana Diguchi	f	530043.27	9937214.86	3813		19	12	3	f
23	H18	Tambo 2A	t	516572.13	9917480.51	3823		19	22	3	f
24	H20	Tambo 12	f	526654.17	9921801.42	3520		19	24	3	f
25	H22	Palmira	t	484805.77	9974099.28	2680		9	5	3	f
26	H24	Guambi San Lorenzo	f	529291.94	9973110.13	3760		9	9	3	f
27	H26	Salve Faccha	f	542688.51	9974182.46	3760		19	19	3	f
28	H27	Guambicocha	f	542734.36	9974133.15	3760		19	19	3	f
29	H28	Sucus	t	534606.30	9959887.11	3760		19	20	3	f
30	H29	San Juan	t	534188.43	9960111.21	3800		19	20	3	f
31	H31	Blanco Grande	f	547573.10	9957780.65	2665		19	20	3	f
32	H32	Cojanco	t	539449.69	9957520.21	3200		19	20	3	f
33	H33	Quijos Norte	f	550305.17	9947283.65	2567		19	21	3	f
659	P75	Laguna Los Patos	t	544539.22	9972457.12	4028		19	18	1	f
90	P43	Antisana Limboasi	t	532466.92	9934401.31	3734		19	12	1	f
35	H35	Quijos Sur	f	550321.91	9947254.46	2562		19	21	3	f
36	H36	Tuminguina Ramal Papallacta	t	539440.22	9957531.24	3200		19	20	3	f
37	H38	Río Encantada	f	547297.36	9963539.42	3253		19	18	3	f
38	H39	Chalpi A	f	546500.60	9963955.80	3200		19	18	3	f
39	H40	Chalpi B	f	545525.73	9962791.42	3239		19	18	3	f
40	H41	Chalpi C	f	544766.37	9961523.74	3394		19	18	3	f
41	H42	Chalpi Norte	t	544792.97	9971225.83	3840		19	18	3	f
42	H43	Blanco Grande Captación	f	545781.58	9955492.38	3200		19	20	3	f
43	H44	Antisana DJ Diguchi	t	530065.24	9937175.32	3812		19	12	3	f
44	H45	Río Papallacta DJ Río Blanco Chico	t	542179.56	9958195.92	2960		19	20	3	f
45	H46	Papallacta DJ Blanco chico	f	541831.95	9957725.92	2960		19	20	3	f
46	H48	Mudadero	t	513442.00	9931434.54	3873		9	25	3	f
47	H52	Alambrado	t	533830.67	9940172.97	3922		19	12	3	f
49	H54	Sarpache	t	534296.31	9938264.80	3942		19	12	3	f
50	H55	Río Antisana AC	t	530386.57	9940670.39	3957		19	12	3	f
51	H56	Salve Faccha A1	t	537864.55	9973335.71	3896		19	19	3	f
52	H57	Salve Faccha A2	t	537491.59	9973502.27	3898		19	19	3	f
53	H58	Salve Faccha A6	t	537411.98	9974970.17	3918		19	19	3	f
54	P03	Rumihurco Machángara	t	497026.08	9985543.76	3245		9	2	1	f
55	P05	Rumihurco Occidental	f	498850.23	9986785.46	2920		9	2	1	f
56	P08	Rumipamba Bodegas	t	498892.65	9979986.62	3005		9	3	1	f
58	P10	Dac Aeropuerto	f	501200.29	9983561.01	2811		9	3	1	f
59	P11	Antenas	t	497326.67	9981633.83	3800		9	3	1	f
61	P13	Cumbaya	t	507800.34	9976387.82	2339		9	9	1	f
62	P14	Zámbiza	t	505970.78	9983673.19	2677		9	9	1	f
64	P16	Izobamba	t	493859.16	9959517.34	3046		9	8	1	f
66	P18	Guayllabamba	f	516072.28	9991335.91	2259		9	9	1	f
67	P19	La Tola (Tumbaco)	t	514419.41	9974348.23	2480		9	9	1	f
69	P21	Río Grande Chillogallo	f	490658.44	9968455.47	3103		9	4	1	f
71	P23	Atacazo	t	488666.66	9964786.15	3877		9	4	1	f
72	P24	Observatorio	f	499736.40	9976216.59	2827		9	1	1	f
79	P31	Pichán	t	492032.35	9987187.85	3516		9	15	1	f
80	P32	Mindo Bajo	f	489100.98	9984909.70	3330		9	14	1	f
81	P33	Nunalviro	f	531440.61	9971261.10	4116		9	9	1	f
82	P34	Papallacta	t	539936.28	9957892.78	3156		19	20	1	f
83	P35	Bocatoma Pita	f	506779.71	9945059.32	3361		9	25	1	f
84	P37	Salve Faccha	f	538297.75	9974118.36	3880		19	19	1	f
85	P38	San Simón	t	538914.71	9942255.90	4303		19	12	1	f
86	P39	Yangahuagra	t	515068.11	9926804.23	3972		9	25	1	f
87	P40	Tambo 2a	t	515838.44	9916833.32	3880		19	22	1	f
89	P42	Antisana Ramón Huañuna	t	533533.37	9933428.27	3691		19	12	1	f
76	P28	Cruz Loma	t	495770.84	9979839.05	4012		9	3	1	f
2	C02	Rumihurco	t	495826.29	9985646.41	3586		9	2	2	f
77	P29	Palmira	t	485032.59	9973924.91	2673		9	5	1	f
4	C04	Rumipamba	t	496515.57	9980594.73	3355		9	3	2	f
78	P30	Santa Rosa	t	488572.27	9971789.71	2913		9	5	1	f
6	C06	Yaruquí	t	521558.16	9981817.92	2680		9	9	2	f
7	C07	San Antonio	t	504966.01	9997963.62	2467		9	10	2	f
11	C11	Pita Campamento	t	506872.94	9945112.99	3387		9	25	2	f
88	P41	Guayllabamba Hacienda	t	516939.90	9990666.10	2373		9	9	1	f
57	P09	Iñaquito INAMHI	t	501372.08	9980269.60	2804		9	3	1	f
60	P12	Toctiuco	t	496962.95	9977180.18	3232		9	4	1	f
63	P15	El Cinto	t	492222.74	9972532.36	3273		9	4	1	f
65	P17	El Tingo	t	506337.01	9967507.34	2483		9	9	1	f
68	P20	Calderón	t	507421.06	9991397.36	2771		9	10	1	f
70	P22	Chillogallo	t	490453.88	9969226.21	3202		9	4	1	f
20	H13	Chalpi Grande	t	546168.00	9960742.44	2880		19	18	3	f
73	C19	El Troje	t	497372.93	9963120.85	3122		9	4	2	f
74	C18	Puengasí	t	500769.56	9973818.84	2970		9	4	2	f
95	P52	Pintag	t	513777.27	9959882.66	2814		9	9	1	f
97	P54	El Carmen	t	515012.27	9949730.50	3283		9	25	1	f
98	P55	Antisana Diguchi	t	526392.68	9936650.63	3958		19	12	1	f
99	P56	Tanque Solanda	t	496576.51	9968833.19	2916		9	4	1	f
100	P57	Quijos Campamento	f	550312.65	9948004.12	2698		19	21	1	f
102	P59	Calacalí	t	498369.85	10000783.43	2894		9	10	1	f
103	P60	San José de Minas	t	509664.02	10019182.05	2466		9	10	1	f
104	P61	Perucho	t	508705.65	10012229.77	1858		9	10	1	f
105	P62	Blanco Chico Alto	t	539591.68	9949890.69	4320		19	20	1	f
107	P64	Laguna Encantada	t	547840.09	9968126.57	4000		19	18	1	f
108	P65	Laguna Santa Lucía	t	535420.41	9948588.36	4379		19	12	1	f
111	P68	Salve Faccha alto	t	536741.69	9974088.22	3919		19	19	1	f
117	AB03	Qda Atacazo	f	\N	\N	\N		\N	\N	4	f
118	AB04	Qda El Tundal 1	f	\N	\N	\N		\N	\N	4	f
119	AB05	Qda El Tundal 2	f	\N	\N	\N		\N	\N	4	f
120	AB06	Qda De la Plata 1	f	\N	\N	\N		\N	\N	4	f
121	AB07	Qda De la Plata 2	f	\N	\N	\N		\N	\N	4	f
122	AB08	Qda Cristal	f	\N	\N	\N		\N	\N	4	f
123	AB09	Qda Zapallar (Paylon)	f	\N	\N	\N		\N	\N	4	f
124	AB10	Qda Caracha	f	\N	\N	\N		\N	\N	4	f
125	AB11	Qda Chuzalongo	f	\N	\N	\N		\N	\N	4	f
126	AB12	Canal  Atacazo en Chuzalongo	f	\N	\N	\N		\N	\N	4	f
127	AB16	Qda Huaspa	f	\N	\N	\N		\N	\N	4	f
48	H53	Moyas	t	535162.30	9939880.59	4019		19	12	3	f
128	AB17	Canal Atacazo entrada túnel	f	\N	\N	\N		\N	\N	4	f
129	AB18	Quebrada Cerro Negro DJ El Arenal	f	\N	\N	\N		\N	\N	4	f
130	AB19	Canal cerro Negro DJ Qda. Atacazo	f	\N	\N	\N		\N	\N	4	f
131	AB20	Canal Cerro Negro entrada al túnel	f	\N	\N	\N		\N	\N	4	f
132	AC01	Vertiente Tesalia	f	\N	\N	2835		\N	\N	4	f
133	AC01_2	Vertiente Tesalia2	f	\N	\N	2835		\N	\N	4	f
134	AC01_3	Vertiente Tesalia3	f	\N	\N	2835		\N	\N	4	f
135	AC01_4	VertienteTesalia4	f	\N	\N	2835		\N	\N	4	f
136	AC02	Acequia La Compañía	f	\N	\N	2865		\N	\N	4	f
137	AC02_2	Acequia La Compañía2	f	\N	\N	2865		\N	\N	4	f
138	AC02_3	Acequia La Compañía3	f	\N	\N	2865		\N	\N	4	f
139	AC03	Acequia La Compañía para fábrica Sillunchi	f	\N	\N	\N		\N	\N	4	f
140	AC04	Rio San Pedro AJ Vert Tesalia	f	\N	\N	2835		\N	\N	4	f
141	AC05	Vertiente Medrano	f	\N	\N	2640		\N	\N	4	f
142	AC05_1	Vertiente Medrano	f	\N	\N	2640		\N	\N	4	f
143	AC05_2	Vertiente Medrano	f	\N	\N	2640		\N	\N	4	f
144	AC05_3	Vertiente Medrano	f	\N	\N	2640		\N	\N	4	f
145	AC08	Vertiente Cristalina Nº3	f	\N	\N	\N		\N	\N	4	f
146	AC09	Vertiente Cachaco	f	\N	\N	\N		\N	\N	4	f
147	AC10	Vertiente Paredes	f	\N	\N	\N		\N	\N	4	f
148	AC12	Vertinete Tesalia desborde	f	\N	\N	\N		\N	\N	4	f
149	CC01	Qda Monjas sector Manuelita Saenz	f	\N	\N	\N		\N	\N	4	f
150	CC02	Qda Shanshaya Puente la Ecuatoriana	f	\N	\N	\N		\N	\N	4	f
151	CC03	Qda Ortega La Ecuatoriana	f	\N	\N	\N		\N	\N	4	f
152	CC04	Qda Shanshayacu AJ Qda Ortega	f	\N	\N	\N		\N	\N	4	f
153	CC05	Qda Ortega AJ Qda Shanshayacu	f	\N	\N	\N		\N	\N	4	f
154	CC06	Qda Shanshayacu parada TroleSur	f	\N	\N	2883		\N	\N	4	f
155	CC07	Qda Shanshayacu AJ Machángara calle Quimiac	f	\N	\N	\N		\N	\N	4	f
156	CC08	Río Grande estación El Tránsito	f	\N	\N	3276		\N	\N	4	f
157	CC09	Río Grande Santa Bárbara	f	\N	\N	\N		\N	\N	4	f
158	CC10	Rìo Grande En Puente Viejo Santa Rita	f	\N	\N	\N		\N	\N	4	f
159	CC11	Río Grande Solanda	f	\N	\N	\N		\N	\N	4	f
160	CC12	Rìo Grande AJ Machàngara Colegio CPP	f	\N	\N	\N		\N	\N	4	f
161	CC13	Qda Caupicho AJ Rìo Machángara	f	\N	\N	\N		\N	\N	4	f
162	CC14	Río Machángara AJ Qda Caupicho	f	\N	\N	\N		\N	\N	4	f
163	CC15	Río Machángara el Beaterio rieles	f	\N	\N	\N		\N	\N	4	f
164	CC16	Río Machángara Oleoducto	f	\N	\N	\N		\N	\N	4	f
165	CC17	Río Machángara AJ Qda Capuli	f	\N	\N	\N		\N	\N	4	f
166	CC18	Qda.Capulí AJ Machángara	f	\N	\N	2876		\N	\N	4	f
167	CC19	Rìo Machàngara ( Lucha de los Pobres)	f	\N	\N	\N		\N	\N	4	f
168	CC20	Rìo Machàngara Fosforera Ecuatoriana	f	\N	\N	\N		\N	\N	4	f
169	CC21	Rìo Machangara en el Mayorista	f	\N	\N	\N		\N	\N	4	f
170	CC22	Río Machángara AJ Río Grande (QuitoSur)	f	\N	\N	\N		\N	\N	4	f
171	CC23	Río Machángara Centro Comercial el Recreo	f	\N	\N	2860		\N	\N	4	f
172	CC24	Colector El Recreo AJ Machángara	f	\N	\N	\N		\N	\N	4	f
173	CC25	Río Machángara en VillaFlora	f	\N	\N	2830		\N	\N	4	f
174	CC26	Rìo Machàngara en el Sena Recoleta	f	\N	\N	\N		\N	\N	4	f
175	CC27	Rìo Machangara Sector El Trébol	f	\N	\N	\N		\N	\N	4	f
176	CC28	Río Machángara Monjas Orquideas	f	\N	\N	2630		\N	\N	4	f
177	CC29	Colector El Batán descarga	f	\N	\N	\N		\N	\N	4	f
178	CC30	Río Machangara Trasvase Central Nayon	f	\N	\N	2214		\N	\N	4	f
179	CC31	Qda Rumipamba	f	\N	\N	\N		\N	\N	4	f
180	CC34	Qda Rumihurco-estación	f	\N	\N	\N		\N	\N	4	f
181	CC35	Qda El Colegio AJ Rumihurco	f	\N	\N	\N		\N	\N	4	f
182	CC36	Qda El Colegio DJ Rumihurco	f	\N	\N	\N		\N	\N	4	f
183	CC37	Río Monjas estación El Colegio	f	\N	\N	\N		\N	\N	4	f
93	P46	Chalpi Grande	t	546170.21	9960778.58	2905		19	18	1	f
96	P53	Paluguillo	t	523709.79	9970416.81	2969		9	9	1	f
106	P63	La Virgen Papallacta	t	534308.65	9964564.66	4365		19	20	1	f
109	P66	Blanco Grande	t	545738.02	9955637.48	3208		19	20	1	f
110	P67	Relleno El Inga	t	516046.18	9967465.44	2658		9	9	1	f
112	P70	CC El Bosque	t	500293.65	9982112.95	2903		9	3	1	f
113	P71	Collaloma Medio	t	502983.59	9986436.34	2968		9	2	1	f
114	P72	Colinas Alto	t	497432.65	9988624.02	3088		9	2	1	f
94	C14	Mindo Captación	t	490186.09	9983470.18	3600		9	14	2	f
91	C16	Guaytaloma	t	542097.78	9967076.30	3782		19	18	2	f
101	C15	Nanegalito	t	479360.46	10006618.39	1767		9	10	2	f
184	CC38	Rìo Monjas Pusuquí	f	\N	\N	\N		\N	\N	4	f
185	CC39	Rìo Monjas Pomasqui	f	\N	\N	\N		\N	\N	4	f
186	CC40	Rìo Monjas Sector San Antonio-Piscinas	f	\N	\N	\N		\N	\N	4	f
187	CC41	Río Monjas canal La Internacional AJ	f	\N	\N	\N		\N	\N	4	f
188	CC42	Qda La Armenia Conocoto estación	f	\N	\N	\N		\N	\N	4	f
189	CC43	Ríos Monjas nueva estación Contraloría	f	\N	\N	\N		\N	\N	4	f
190	CC44	Qda Monjas Alto	f	\N	\N	\N		\N	\N	4	f
191	CC45	Qda Monjas Bajo	f	\N	\N	\N		\N	\N	4	f
192	CC46	Qda San José	f	\N	\N	\N		\N	\N	4	f
193	CC47	Qda Ortega(Antes del Terminal Quitumbe)	f	\N	\N	\N		\N	\N	4	f
194	CC48	Qda Shanshayacu(En la Piscina)	f	\N	\N	\N		\N	\N	4	f
195	CG01	Río Pita DJ Guapal  Playa Chica	f	\N	\N	2740		\N	\N	4	f
196	CG02	Río Pita AJ San Pedro  ALOAG	f	\N	\N	2430		\N	\N	4	f
197	CG03	Río San Pedro puente Uyumbicho Trópico	f	\N	\N	2610		\N	\N	4	f
198	CG04	Río San Pedro AJ Río Pita puente Amaguaña	f	\N	\N	2425		\N	\N	4	f
199	CG05	Río San Pedro Puente Guangopolo	f	\N	\N	2240		\N	\N	4	f
200	CG06	Río San Pedro Triángulo vía Conocoto AJ Pita	f	\N	\N	2440		\N	\N	4	f
201	CG07	Río San pedro puente Cerveceria Cumbayá	f	\N	\N	2180		\N	\N	4	f
202	CG08	Río San Pedro AJ Machangara (minas de	f	\N	\N	2480		\N	\N	4	f
203	CG09	Río San Pedro y Machangara AJ turbinado C Hd	f	\N	\N	2240		\N	\N	4	f
204	CG10	Canal Tumbaco Toma Río Pita	f	\N	\N	2230		\N	\N	4	f
205	CG11	Qda Los Alemanes	f	\N	\N	2270		\N	\N	4	f
206	CG12	Qda Retraida	f	\N	\N	2120		\N	\N	4	f
207	CG13	Qda  Lalagachi (Checa)	f	\N	\N	2100		\N	\N	4	f
208	CG14	Río Uravia ( la victoria - El Quinche)	f	\N	\N	3200		\N	\N	4	f
209	CG15	Río Alcantarilla Tumbaco	f	\N	\N	3150		\N	\N	4	f
210	CG16	Río Chiche Puente Viejo	f	\N	\N	1980		\N	\N	4	f
211	CG17	Río Guambi camino antiguo	f	\N	\N	1790		\N	\N	4	f
212	CG18	Río Guambi puente  Pifo-Puembo	f	\N	\N	1810		\N	\N	4	f
213	CG19	Qda El Quinche (Guayllabamba)	f	\N	\N	1930		\N	\N	4	f
214	CG20	Qda Ormaza puente Llano Chico	f	\N	\N	1950		\N	\N	4	f
215	CG21	Río Coyago  puente Guayllabamba	f	\N	\N	1250		\N	\N	4	f
216	CG22	Río Granobles en el puente	f	\N	\N	2740		\N	\N	4	f
217	CG23	Río Guachalá ( puente)	f	\N	\N	1680		\N	\N	4	f
218	CG24	Río Pisque puente panamericana	f	\N	\N	1190		\N	\N	4	f
219	CG25	Río Cubi Perucho	f	\N	\N	\N		\N	\N	4	f
220	CG26	Río Quinde (Selva Alegre)	f	\N	\N	1530		\N	\N	4	f
221	CG27	Río Intag García Moreno	f	\N	\N	\N		\N	\N	4	f
222	CG28	Río Pichán	f	\N	\N	2645		\N	\N	4	f
223	CG29	Río Alambi Nanegalito	f	\N	\N	\N		\N	\N	4	f
224	CG30	Río Alambi  Nanegal	f	\N	\N	\N		\N	\N	4	f
225	CG31	Río Pachijal (Saloya)	f	\N	\N	\N		\N	\N	4	f
226	CG32	Río Pachijal (Puerto Rico)	f	\N	\N	\N		\N	\N	4	f
227	CG33	Río Piganta	f	\N	\N	\N		\N	\N	4	f
228	CG34	Sobrante Canal Tumbaco Toma Río Pita	f	\N	\N	\N		\N	\N	4	f
229	CT01	Vertiente Sambopogyo	f	\N	\N	2600		\N	\N	4	f
230	CT02	Vertiente Guápulo piscinas	f	\N	\N	2600		\N	\N	4	f
231	CT03	Vertiente El Inga	f	\N	\N	2795		\N	\N	4	f
232	CT04	Vertientes Chirimoyas (3)	f	\N	\N	2146		\N	\N	4	f
233	CT05	Qda Larios	f	\N	\N	\N		\N	\N	4	f
234	CT06	Tanque Guapulo Guashayacu Sitios 1, 2, 3, 4	f	\N	\N	\N		\N	\N	4	f
235	CT07	Galería Guápulo	f	\N	\N	\N		\N	\N	4	f
236	CT20	Qda. Batan	f	\N	\N	\N		\N	\N	4	f
237	CTI1	Canal Tumbaco Bocatoma	f	\N	\N	\N		\N	\N	4	f
238	CTI10	Canal Ilalo Después  Toma Planta Tumbaco	f	\N	\N	\N		\N	\N	4	f
239	CTI2	Canla Tumbaco Sector Rumiplaya	f	\N	\N	\N		\N	\N	4	f
240	CTI3	Canal Tumbaco Sector San Elias	f	\N	\N	\N		\N	\N	4	f
241	CTI4	Canal Tumbaco Sector  El Refugio	f	\N	\N	\N		\N	\N	4	f
242	CTI5	Canal Tumbaco Sector Guangal	f	\N	\N	\N		\N	\N	4	f
243	CTI6	Canal Tumbaco Antes Canal Ilalo (Catalino)	f	\N	\N	\N		\N	\N	4	f
244	CTI7	Canal Tumbaco (Universidad)	f	\N	\N	\N		\N	\N	4	f
245	CTI8	Canal Ilalo Sector Ilusión	f	\N	\N	\N		\N	\N	4	f
246	CTI9	Canal Ilalo Antes de la toma Planta Tumbaco	f	\N	\N	\N		\N	\N	4	f
247	INS01	Canal Tumbaco Viejo	f	\N	\N	\N		\N	\N	4	f
248	INS02	Río Arturo	f	\N	\N	\N		\N	\N	4	f
249	INS03	Río Boquerón	f	\N	\N	\N		\N	\N	4	f
250	INS04	Río San Pedro	f	\N	\N	\N		\N	\N	4	f
251	INS05	Azuela AJ San Pedro	f	\N	\N	\N		\N	\N	4	f
252	INS06	Río La Chimba  sitio de Emblase de	f	\N	\N	\N		\N	\N	4	f
253	INSP	Varios	f	\N	\N	\N		\N	\N	4	f
254	LL01	Río Cinto en Palmira	f	\N	\N	3650		\N	\N	4	f
255	LL02	Qda Chimborazo cantera	f	\N	\N	2960		\N	\N	4	f
256	LL03	Río Cinto en Santa Rosa	f	\N	\N	2920		\N	\N	4	f
257	LL04	Qda Chalhuayacu	f	\N	\N	2925		\N	\N	4	f
258	LL05	Ramal Pugnahua-Chimborazo-Cotogyacu	f	\N	\N	3060		\N	\N	4	f
259	LL06	Ramal ElChazo-Pogyo-Cuchicorral	f	\N	\N	3184		\N	\N	4	f
260	LL07	Ramal Oriental (DiqueTambillo)	f	\N	\N	3184		\N	\N	4	f
261	LL08	Entrada Túnel Ungui	f	\N	\N	3055		\N	\N	4	f
262	LL09	Vertiente San Ignacio	f	\N	\N	3400		\N	\N	4	f
263	LL10	Acequia Pichincha	f	\N	\N	3680		\N	\N	4	f
264	LL11	Acequia Pichincha (chorrera)	f	\N	\N	\N		\N	\N	4	f
265	LL12	Acequia La Palma(CruzLoma)	f	\N	\N	3940		\N	\N	4	f
266	LL13	Acequia La Palma (B.Armero) 10 sitios	f	\N	\N	3940		\N	\N	4	f
267	LL14	Vertientes Llugllucchas	f	\N	\N	\N		\N	\N	4	f
268	LL15	Vertiente Padre Encantado	f	\N	\N	\N		\N	\N	4	f
269	LL16	Ac.Pichincha DJ Padre Encantado	f	\N	\N	\N		\N	\N	4	f
270	LL17	Qda Arcocucho 1y2	f	\N	\N	\N		\N	\N	4	f
271	LL18	Ac Pichincha DJ Qda Arcocucho	f	\N	\N	\N		\N	\N	4	f
272	LL19	Qda Las Palmas	f	\N	\N	\N		\N	\N	4	f
273	LL20	Ac Pichincha DJ Qda Las Palmas	f	\N	\N	\N		\N	\N	4	f
274	LL21	Ac Pichincha Ugshapugro	f	\N	\N	\N		\N	\N	4	f
275	LL22	Captación Tunel Garzón	f	\N	\N	\N		\N	\N	4	f
276	LL23	Captación Cuchicorral	f	\N	\N	\N		\N	\N	4	f
277	MS01	Río Antisana DJ Diguchi	f	\N	\N	3800		\N	\N	4	f
278	MS02	Río Antisana AJ Micahuayco	f	\N	\N	3920		\N	\N	4	f
279	MS03	Río Micahuayco AJ Antisana	f	\N	\N	3960		\N	\N	4	f
280	MS037	Río Moyas Parte Alta	f	\N	\N	3945		\N	\N	4	f
281	MS04	Río Diguchi antes captación	f	\N	\N	3940		\N	\N	4	f
282	MS05	Río Jatunhuayco antes captación	f	\N	\N	3900		\N	\N	4	f
283	MS06	Río Antisana antes captación	f	\N	\N	3900		\N	\N	4	f
285	MS09	Río Moyas (Sarpache 1)	f	\N	\N	3960		\N	\N	4	f
286	MS10	Río Sarpache	f	\N	\N	3940		\N	\N	4	f
287	MS11	Río Socavón	f	\N	\N	3915		\N	\N	4	f
288	MS12	Desborde Central El Carmen	f	\N	\N	4000		\N	\N	4	f
289	MS13	Río I	f	\N	\N	4040		\N	\N	4	f
290	MS14	Río J	f	\N	\N	3740		\N	\N	4	f
291	MS15	Río Piedra Azufre despues de la chorrera	f	\N	\N	3540		\N	\N	4	f
292	MS15a	Río Piedra Azufre  parte Alta  (Captación)	f	\N	\N	\N		\N	\N	4	f
293	MS16	Río Quijos Sur AJ Tablas	f	\N	\N	3480		\N	\N	4	f
294	MS17	Río Tablas AJ Quijos Sur	f	\N	\N	3480		\N	\N	4	f
295	MS17a	Río Tablas Muestreo	f	\N	\N	\N		\N	\N	4	f
296	MS18	Vertiente Yacupamba	f	\N	\N	4120		\N	\N	4	f
297	MS19	Vertiente Black	f	\N	\N	4000		\N	\N	4	f
298	MS20	Vertiente Humboldt	f	\N	\N	4120		\N	\N	4	f
299	MS21	Río Antisana estación Humboldt	f	\N	\N	4040		\N	\N	4	f
300	MS22	Entrada al Tunel Nº2	f	\N	\N	4070		\N	\N	4	f
301	MS23	Salida del Tunel Nº2	f	\N	\N	4090		\N	\N	4	f
302	MS24	Qda Pullurima	f	\N	\N	4080		\N	\N	4	f
303	MS25	Desborde Estribo Derecho	f	\N	\N	3920		\N	\N	4	f
304	MS26	Río Quijos Sur DJ Tablas	f	\N	\N	3440		\N	\N	4	f
305	MS27	Río Diguchi AJ Antisana	f	\N	\N	\N		\N	\N	4	f
306	MS28	Glaciar Los Crespos Estación	f	\N	\N	\N		\N	\N	4	f
307	MS29	Río H	f	\N	\N	\N		\N	\N	4	f
308	MS30	Río Jatunhuaycu  AJ Vert Yacupamba	f	\N	\N	\N		\N	\N	4	f
309	MS31	Vert Yacupamba AJ río Jatunhuaycu	f	\N	\N	\N		\N	\N	4	f
310	MS32	Vert Yacupamba atras de la choza Ovejeria	f	\N	\N	\N		\N	\N	4	f
311	MS33	Río Antisana DJ Micahuayco total	f	\N	\N	\N		\N	\N	4	f
312	MS34	Río Antisana estación Elétrica	f	\N	\N	\N		\N	\N	4	f
313	MS35	Río Sarpache A.J ríos I - J (camino)	f	\N	\N	\N		\N	\N	4	f
314	MS36	Río Diguchi (desborde aguas abajo de	f	\N	\N	\N		\N	\N	4	f
315	MS37	RIO MOYAS PARTE ALTA	f	\N	\N	\N		\N	\N	4	f
316	MS38	Qda. Ladrillos AJ rio Pullurima	f	\N	\N	\N		\N	\N	4	f
317	MS39	Qda. Pullurima AJ Qda Ladrillos	f	\N	\N	\N		\N	\N	4	f
318	MS40	RIO PULLURIMA ENTRADA LAGUNA SECAS	f	\N	\N	\N		\N	\N	4	f
319	NC01	Vert Chinchimbe-Nanegalito	f	\N	\N	1630		\N	\N	4	f
320	NC02	Vert San Francisco-Nanegalito	f	\N	\N	1735		\N	\N	4	f
321	NC03	Río Ingapi-Pacto	f	\N	\N	1485		\N	\N	4	f
322	NC09	Río Tandayapa total	f	\N	\N	\N		\N	\N	4	f
323	NC10	Qda Tandayapa #1-Nanegalito	f	\N	\N	\N		\N	\N	4	f
324	NC11	Qda Tandayapa # 2-Nanegalito	f	\N	\N	\N		\N	\N	4	f
325	NC12	Qda. Zuro # 1 (Nanegalito)	f	\N	\N	\N		\N	\N	4	f
326	NC13	Qda. Zuro # 2 (Nanegalito)	f	\N	\N	\N		\N	\N	4	f
327	NC14	Qda. El Rayo (Nanegalito)	f	\N	\N	\N		\N	\N	4	f
328	NC15	Qda San José- Nanegalito	f	\N	\N	\N		\N	\N	4	f
329	NO01	Qda Pichán	f	\N	\N	3520		\N	\N	4	f
330	NO02	VertienteTaurichupa	f	\N	\N	3580		\N	\N	4	f
331	NO03	Vertiente No.7	f	\N	\N	3580		\N	\N	4	f
332	NO04	Vertiente No.8	f	\N	\N	3580		\N	\N	4	f
333	NO05	Río Mindo - Captación No.9	f	\N	\N	3580		\N	\N	4	f
334	NO06	Vertiente No.10	f	\N	\N	3580		\N	\N	4	f
335	NO07	Vertiente No.11	f	\N	\N	3580		\N	\N	4	f
336	NO08	Vertiente No.12	f	\N	\N	3580		\N	\N	4	f
337	NO09	Río Mindo Bajo estacón	f	\N	\N	3100		\N	\N	4	f
338	NO10a	Qda Santa Ana-captación	f	\N	\N	3200		\N	\N	4	f
339	NO10b	Qda Santa Ana-Desborde	f	\N	\N	\N		\N	\N	4	f
340	NO11	Ac Moncayo	f	\N	\N	3520		\N	\N	4	f
341	NO12	Qda Pichán antes captación	f	\N	\N	3520		\N	\N	4	f
342	NO14	Ac Quito Tenis	f	\N	\N	\N		\N	\N	4	f
343	NO15	Ac Río Mindo	f	\N	\N	\N		\N	\N	4	f
344	NO16	Unión Vertiente 11 y 12	f	\N	\N	\N		\N	\N	4	f
345	NO17	Río Mindo Puente Población	f	\N	\N	\N		\N	\N	4	f
346	NO18	Río Mindo-Saguambi Puente	f	\N	\N	\N		\N	\N	4	f
347	NO22	Río Mindo sitio Mariposas parte alta	f	\N	\N	\N		\N	\N	4	f
348	NO23	Qda Yanayacu AJ  Mindo parte alta	f	\N	\N	\N		\N	\N	4	f
349	NO24	Qda Pungú AJ  Mindo	f	\N	\N	\N		\N	\N	4	f
350	NO25	Río Mindo Bajo captación	f	\N	\N	\N		\N	\N	4	f
351	NO26	Vertiente Nono	f	\N	\N	\N		\N	\N	4	f
352	NO27	Vertiente Las Canteritas (sitio No. 1)	f	\N	\N	\N		\N	\N	4	f
353	NO28	Vertiente Las Canteritas (sitio No. 2)	f	\N	\N	\N		\N	\N	4	f
354	NO29	Vertiente Las Canteritas (sitio No. 3)	f	\N	\N	\N		\N	\N	4	f
355	NO30	Vertiente Las Canteritas (sitio No. 4)	f	\N	\N	\N		\N	\N	4	f
356	NR02	Qda Sigsipamba ( Lalagachi)-Yaruquí	f	\N	\N	2770		\N	\N	4	f
357	NR03	Vert San Carlos-Yaruquí	f	\N	\N	2520		\N	\N	4	f
358	NR04	Ac Changahuaniuna (ovalo)	f	\N	\N	\N		\N	\N	4	f
359	NR05	Ac para Yaruqui	f	\N	\N	\N		\N	\N	4	f
360	NR06	Ac para Barrio Oyambaro	f	\N	\N	\N		\N	\N	4	f
361	NR07	Ac para Barrio Oyambarillo	f	\N	\N	\N		\N	\N	4	f
362	NR08	Qda Sicsipugro-capt planta Yaruquí	f	\N	\N	\N		\N	\N	4	f
363	NR10	Vert Totoras-Checa	f	\N	\N	3500		\N	\N	4	f
364	NR13	Acequia Iguiñaro	f	\N	\N	\N		\N	\N	4	f
365	NT01a	Vert Santo Domingo1-Guayllabamba	f	\N	\N	2280		\N	\N	4	f
366	NT01b	Vert Santo Domingo 2-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
367	NT01c	Vert Santo Domingo 3-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
368	NT01d	Vert Santo Domingo 4-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
369	NT01e	Vert Santo Domingo A1-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
370	NT01g	Vert Santo Domingo C3-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
371	NT01h	Vert Santo Domingo D4-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
372	NT02a	Vert Las Caleras 1-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
373	NT02b	Vert Las Caleras 2-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
374	NT02c	Vert Las Caleras 3-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
375	NT02d	Vert Las Caleras 4-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
376	NT02e	Vert Las Caleras 4A-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
377	NT02f	Vert Las Caleras 4B-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
378	NT02g	Vert Las Caleras 5-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
379	NT02h	Vert Las Caleras 6-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
380	NT02i	Vert Las Caleras 7-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
381	NT02j	Vert Las Caleras 8-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
382	NT02k	Vert Las Caleras 9-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
383	NT03	Vert El Lomón-Chavespamba	f	\N	\N	2300		\N	\N	4	f
384	NT05	Vert Mojanda-Atahualpa	f	\N	\N	2600		\N	\N	4	f
385	NT06	Vert Torucho-Atahualpa	f	\N	\N	2600		\N	\N	4	f
386	NT07	Vert Machay-Atahualpa	f	\N	\N	2600		\N	\N	4	f
387	NT08a	Vert La Rinconada 1-San José de Minas	f	\N	\N	2970		\N	\N	4	f
388	NT08b	Vert la Rinconada 2-San José de Minas	f	\N	\N	\N		\N	\N	4	f
389	NT08c	Vert La Rinconada 3-San José de Minas	f	\N	\N	\N		\N	\N	4	f
390	NT09	Vert Puéllaro-Puéllaro	f	\N	\N	2250		\N	\N	4	f
391	NT10	Vert El Capulí-Puéllaro	f	\N	\N	2400		\N	\N	4	f
392	NT11	Vert  Padre Encantado-San José de Minas	f	\N	\N	\N		\N	\N	4	f
393	NT12	Vert Cumalpí-San José de Minas	f	\N	\N	\N		\N	\N	4	f
395	NT17	Vertiente Cartagena	f	\N	\N	\N		\N	\N	4	f
396	Nt01f	Vert Santo Domingo B2-Guayllabamba	f	\N	\N	\N		\N	\N	4	f
397	PB01	Río Papallacta -piscinas	f	\N	\N	3240		\N	\N	4	f
398	PB02	Río Tuminguina lag Papallacta	f	\N	\N	3060		\N	\N	4	f
399	PB03	Río Tuminguina lag Cojanco	f	\N	\N	3160		\N	\N	4	f
400	PB04	Río Blanco Chico antes captación	f	\N	\N	3180		\N	\N	4	f
401	PB05	Río Papallacta DJ Lag Mentala	f	\N	\N	3380		\N	\N	4	f
402	PB06	Río Papallacta antes capt puente	f	\N	\N	\N		\N	\N	4	f
403	PB07	Qda Guarmihuaico	f	\N	\N	\N		\N	\N	4	f
404	PB08	Qda Carihuaico	f	\N	\N	\N		\N	\N	4	f
405	PB09	Qda Muyuco	f	\N	\N	\N		\N	\N	4	f
406	PB10	Río Tuminguina DJ Cojanco (Total)	f	\N	\N	\N		\N	\N	4	f
407	PB11	Río Blanco Chico A.J Papallacta (desborde)	f	\N	\N	\N		\N	\N	4	f
408	PB12	Río Blanco Chico en elevadora	f	\N	\N	\N		\N	\N	4	f
409	PB13	Qda. Cachaco AJ Papallacta	f	\N	\N	\N		\N	\N	4	f
410	PB14	Qda Jerez AJ Papallacta	f	\N	\N	\N		\N	\N	4	f
411	PB15	Salida laguna Papallacta AJ Tuminguina	f	\N	\N	\N		\N	\N	4	f
412	PB16	Río Papallacta DJ río Blanco Chico	f	\N	\N	\N		\N	\N	4	f
413	PB17	Río Papallacta puente después de Captación	f	\N	\N	\N		\N	\N	4	f
414	PN01	Río Sucus antes captación	f	\N	\N	3760		\N	\N	4	f
415	PN02	Río Sucus en desarenador	f	\N	\N	3760		\N	\N	4	f
416	PN03	Río San Juan antes captación	f	\N	\N	3740		\N	\N	4	f
417	PN04	Río San Juan en desarenador	f	\N	\N	3740		\N	\N	4	f
418	PN05	Río Desaguadero lag Mentala	f	\N	\N	3800		\N	\N	4	f
419	PN06	Río Desaguadero lag El Peine	f	\N	\N	3760		\N	\N	4	f
420	PN07	Río Desaguadero lag Loreto	f	\N	\N	3680		\N	\N	4	f
421	PN08	Río Desaguadero lag Parcacocha	f	\N	\N	3960		\N	\N	4	f
422	PN09	Río Desaguadero Captación lag Guaytaloma	f	\N	\N	3800		\N	\N	4	f
423	PN10	Río Desaguadero lag Mogotes	f	\N	\N	3800		\N	\N	4	f
424	PN11	Qda Quillugsha 1	f	\N	\N	3880		\N	\N	4	f
425	PN12	Qda Quillugsha 2	f	\N	\N	3880		\N	\N	4	f
426	PN13	Qda Quillugsha 3	f	\N	\N	3720		\N	\N	4	f
427	PN14	Río Chalpi Norte antes Captaciòn	f	\N	\N	3820		\N	\N	4	f
428	PN15	Desaguadero lag Guambicocha	f	\N	\N	3880		\N	\N	4	f
429	PN16	Río Guambicocha AJ Salve Faccha estación	f	\N	\N	3840		\N	\N	4	f
430	PN17	Río Salve Faccha-presa (Proyecto)	f	\N	\N	3880		\N	\N	4	f
431	PN18	Río Salve Faccha AJ Guambicocha estación	f	\N	\N	3840		\N	\N	4	f
432	PN21	Río Oyacachi	f	\N	\N	3720		\N	\N	4	f
433	PN22	Río Desaguadero Lag Mentala (camino)	f	\N	\N	3560		\N	\N	4	f
434	PN23	Río Desaguadero lag El Peine (camino)	f	\N	\N	3520		\N	\N	4	f
435	PN24	Entrada Laguna Loreto	f	\N	\N	3720		\N	\N	4	f
436	PN25	Entrada Laguna Mogotes Nº1	f	\N	\N	4000		\N	\N	4	f
437	PN26	Entrada Laguna Mogotes Nº2	f	\N	\N	4000		\N	\N	4	f
438	PN27	Entrada Laguna Mogotes Nº3	f	\N	\N	3990		\N	\N	4	f
439	PN28	Entrada Laguna Mogotes Nº4	f	\N	\N	4000		\N	\N	4	f
440	PN29	Río Mogotes antes captación	f	\N	\N	3670		\N	\N	4	f
441	PN29A	Filtración Captación Mogotes	f	\N	\N	\N		\N	\N	4	f
442	PN30	Captación Venado	f	\N	\N	3880		\N	\N	4	f
443	PN31	Embalse Salve Faccha Afluente Nº1	f	\N	\N	3920		\N	\N	4	f
444	PN32	Embalse Salve Faccha Afluente Nº2	f	\N	\N	3920		\N	\N	4	f
445	PN33	Embalse Salve Faccha Afluente Nº3	f	\N	\N	3920		\N	\N	4	f
446	PN34	Embalse Salve Faccha Afluente Nº4	f	\N	\N	3920		\N	\N	4	f
447	PN35	Embalse Salve Faccha Afluente Nº5	f	\N	\N	3920		\N	\N	4	f
448	PN36	Embalse Salve Faccha Afluente Nº6	f	\N	\N	3920		\N	\N	4	f
449	PN37	Río Desaguadero Lag Patos	f	\N	\N	4000		\N	\N	4	f
450	PN38	Qda Gonzalito antes captación	f	\N	\N	3800		\N	\N	4	f
451	PN39	Afluentes embalse Sucus (8 aportes)	f	\N	\N	3920		\N	\N	4	f
452	PN40	Qda Intermedia Nº1 entre Peine y Mentala	f	\N	\N	3800		\N	\N	4	f
453	PN41	Qda Intermedia Nº2 entre Peine y Mentala	f	\N	\N	3800		\N	\N	4	f
454	PN43	Río Mogotes AJ Qda Guaytaloma	f	\N	\N	\N		\N	\N	4	f
455	PN44	Qda. Guaytaloma AJ Río Mogotes	f	\N	\N	\N		\N	\N	4	f
456	PN45	Río Mogotes Puente	f	\N	\N	\N		\N	\N	4	f
457	PN46	Chalpi Norte despúes Captación (desborde)	f	\N	\N	\N		\N	\N	4	f
458	PN47	Río Sucus DJ San Juan	f	\N	\N	\N		\N	\N	4	f
459	PN48	Río Sucus - Puente	f	\N	\N	\N		\N	\N	4	f
460	PN49	Rio San Juan - Puente	f	\N	\N	\N		\N	\N	4	f
461	PN50	Río Sucus después captacion	f	\N	\N	\N		\N	\N	4	f
462	PN51	Río San Juan después captación	f	\N	\N	\N		\N	\N	4	f
463	PN52	Rio Papallacta en puente	f	\N	\N	\N		\N	\N	4	f
464	PN53	Qda Gonzalito AJ Glaciar (captación)	f	\N	\N	3800		\N	\N	4	f
465	PN54	Captación Glaciar	f	\N	\N	\N		\N	\N	4	f
466	PN55	Salida de la laguna San Cristobal	f	\N	\N	\N		\N	\N	4	f
467	PN56	Río  Sucus despúes captación (Desborde)	f	\N	\N	\N		\N	\N	4	f
468	PN57	Despues captación Quillugsha 1 y 2 (Desborde	f	\N	\N	\N		\N	\N	4	f
469	PN58	Despues capatción Quillugsha # 3 ( Desborde)	f	\N	\N	\N		\N	\N	4	f
470	PN60	Desborde de Captación Gonzalito	f	\N	\N	\N		\N	\N	4	f
471	PN61	Captación Guaytaloma (deborde)	f	\N	\N	\N		\N	\N	4	f
472	PN62	Captación Mogotes (desborde)	f	\N	\N	\N		\N	\N	4	f
473	PN63	Captación Venado (Desborde)	f	\N	\N	\N		\N	\N	4	f
474	PN64	Captación Vikingos	f	\N	\N	\N		\N	\N	4	f
475	PN65	Río Salve Faccha capt Cangahua	f	\N	\N	\N		\N	\N	4	f
476	PN66	Rio Salve faccha en el puente (Camino)	f	\N	\N	\N		\N	\N	4	f
477	PN67	Qda Quillugshas en el camino 1 y 2	f	\N	\N	\N		\N	\N	4	f
561	RO28	Qda Seimond AJ Quijos Sur	f	\N	\N	\N		\N	\N	4	f
562	RO29	Río Quijos Sur AJ Seimond	f	\N	\N	\N		\N	\N	4	f
478	PN68	DESBORDE CAPTACION GLACIAR(AUDITORIA)	f	\N	\N	\N		\N	\N	4	f
479	PP01	Vertiente Mulauco	f	\N	\N	2960		\N	\N	4	f
480	PP02	Qda Guarmihuaycu antes pozo infil	f	\N	\N	2800		\N	\N	4	f
481	PP03	Qda Guarmihuaycu después de la chorrera	f	\N	\N	2760		\N	\N	4	f
482	PP04	Vertiente Chántag	f	\N	\N	2589		\N	\N	4	f
483	PP05	Vertiente Chántag para Chaupi Molina	f	\N	\N	\N		\N	\N	4	f
484	PP06	Río Guambi antes acequia San Lorenzo	f	\N	\N	3730		\N	\N	4	f
485	PP07	Río Desaguadero lag Nunalviro	f	\N	\N	4040		\N	\N	4	f
486	PP08	Acequia San Lorenzo	f	\N	\N	\N		\N	\N	4	f
487	PP09	Acequia para Hda. Los Andes	f	\N	\N	\N		\N	\N	4	f
488	PP10	Vertiente Piedras Negras	f	\N	\N	\N		\N	\N	4	f
489	PP11	Río Guarmihuayco tras Recuperadora	f	\N	\N	\N		\N	\N	4	f
490	PS01	Qda Afluente lag Cojanco capt.1	f	\N	\N	3480		\N	\N	4	f
491	PS02	Qda Afluente lag Potrerillos capt4	f	\N	\N	3880		\N	\N	4	f
492	PS03	Qda Afluente laguna Potrerillos capt5	f	\N	\N	3760		\N	\N	4	f
493	PS04	Qda Afluente lag Potrerillos capt6	f	\N	\N	3800		\N	\N	4	f
494	PS05	Qda Afluente lag Potrerillos capt7	f	\N	\N	4000		\N	\N	4	f
495	PS06	Río Tambo parte alta	f	\N	\N	3730		\N	\N	4	f
496	PS07	Río Guamaní capt1	f	\N	\N	4040		\N	\N	4	f
497	PS08	Río Guamaní capt2	f	\N	\N	3880		\N	\N	4	f
498	PS09	Río Guamaní capt3	f	\N	\N	4000		\N	\N	4	f
499	PS10	Río Tambo antes lag Papallacta	f	\N	\N	3370		\N	\N	4	f
500	PS11	Rìo Tambo DJ Guamaní	f	\N	\N	3700		\N	\N	4	f
501	PS12	Qda Guamaní AJ Tambo	f	\N	\N	3720		\N	\N	4	f
502	PS13	Qda Jerez	f	\N	\N	3440		\N	\N	4	f
503	PS14	Entrada a la Laguna Potrerillos	f	\N	\N	\N		\N	\N	4	f
504	PS15	Río Tambo	f	\N	\N	\N		\N	\N	4	f
505	PS16	Vertiente Aguas Termales	f	\N	\N	\N		\N	\N	4	f
506	PS17	Vertiente Guamaní # 4	f	\N	\N	\N		\N	\N	4	f
507	PS18	Vertiente Guamaní # 5	f	\N	\N	\N		\N	\N	4	f
508	PT01	Canal Alumis desborde Pita	f	\N	\N	3911		\N	\N	4	f
509	PT02	Río Mudadero AJ Pita	f	\N	\N	3879		\N	\N	4	f
510	PT03	Río Pita AJ Mudadero	f	\N	\N	3879		\N	\N	4	f
511	PT04	Río Pita sitio Salitre	f	\N	\N	3748		\N	\N	4	f
512	PT05	Acequia Patichubamba	f	\N	\N	3640		\N	\N	4	f
513	PT06	Acequia San José	f	\N	\N	3670		\N	\N	4	f
514	PT07	Acequia Guitig en el camino	f	\N	\N	3480		\N	\N	4	f
515	PT08	Acequia Guitig en la toma	f	\N	\N	3840		\N	\N	4	f
516	PT09	Acequia Taxohurcu	f	\N	\N	3840		\N	\N	4	f
517	PT10	Acequia Taxohurco en la toma	f	\N	\N	3840		\N	\N	4	f
518	PT11	Qda Cortijo AJ Toruno parte alta	f	\N	\N	3310		\N	\N	4	f
519	PT12	Qda Cortijo bajo la Chorrera	f	\N	\N	3300		\N	\N	4	f
520	PT13	Qda Toruno AJ Cortijo	f	\N	\N	3377		\N	\N	4	f
521	PT14	Río El Salto en el puente	f	\N	\N	3260		\N	\N	4	f
522	PT15	Río Pita antes Bocatoma estación	f	\N	\N	3365		\N	\N	4	f
523	PT16	Río Pita Campamento Proaño	f	\N	\N	3631		\N	\N	4	f
524	PT17	Canal Pita Entrada Sifon San Pedro	f	\N	\N	3180		\N	\N	4	f
525	PT18	Canal Pita Salida Sifón San Pedro	f	\N	\N	2880		\N	\N	4	f
526	PT19	Canal Pita DJ Planta El Troje	f	\N	\N	3000		\N	\N	4	f
527	PT20	Canal Pita AJ Planta Conocoto	f	\N	\N	3000		\N	\N	4	f
528	PT21	Canal Pita Aliviadero No.27	f	\N	\N	2960		\N	\N	4	f
529	PT22	Canal Pita Planta Puengasí	f	\N	\N	2960		\N	\N	4	f
530	PT23	Canal del Pita Aliviadero 25	f	\N	\N	2486		\N	\N	4	f
531	PT24	Río Pita AJ río El Salto	f	\N	\N	\N		\N	\N	4	f
532	PT25	Río El Salto AJ río Pita	f	\N	\N	\N		\N	\N	4	f
533	PT26	Río Pita Desborde Bocatoma	f	\N	\N	\N		\N	\N	4	f
534	PT27	Canal Pita Desarenador	f	\N	\N	\N		\N	\N	4	f
535	PT28	Aporte Panzatilin	f	\N	\N	\N		\N	\N	4	f
536	PT29	SALIDA DEL TUNEL # 2 (PARSHAL)	f	\N	\N	\N		\N	\N	4	f
537	RO01	Río Tolda AJ Chaupibolsa	f	\N	\N	3460		\N	\N	4	f
538	RO02	Río Chaupibolsa AJ Tolda	f	\N	\N	3400		\N	\N	4	f
539	RO05	Río Antisana DJ Ramón Huañuna estación	f	\N	\N	3690		\N	\N	4	f
540	RO06	Río Maquimallanda AJ Antisana	f	\N	\N	3605		\N	\N	4	f
541	RO07	Río Antisana AJ Maquimallanda	f	\N	\N	3555		\N	\N	4	f
542	RO08	Río Jabas	f	\N	\N	3560		\N	\N	4	f
543	RO09	Río Cosanga	f	\N	\N	3220		\N	\N	4	f
544	RO10	Río Quijos Norte AJ Quijos Sur	f	\N	\N	2680		\N	\N	4	f
545	RO11	Río Blanco Grande estación	f	\N	\N	2760		\N	\N	4	f
546	RO12	Río Encantado AJ Chalpi Grande	f	\N	\N	3100		\N	\N	4	f
547	RO13	Río Chalpi Grande en estación	f	\N	\N	2820		\N	\N	4	f
548	RO14	Río Chalpi Grande AJ Encantada	f	\N	\N	3120		\N	\N	4	f
549	RO15	Río Quijos Sur A.J río Quijos Norte	f	\N	\N	\N		\N	\N	4	f
550	RO16	Río Quijos Norte DJ Cristal	f	\N	\N	2900		\N	\N	4	f
551	RO17	Río Cristal AJ Quijos Norte	f	\N	\N	3060		\N	\N	4	f
552	RO18	Río Quijos Norte AJ Tablón	f	\N	\N	3120		\N	\N	4	f
553	RO20	Río Quijos Norte - Captación	f	\N	\N	3220		\N	\N	4	f
554	RO21	Rìo Tablón Saccha AJ Antisana	f	\N	\N	3680		\N	\N	4	f
555	RO22	Río Condor Pamba AJ Antisana	f	\N	\N	3600		\N	\N	4	f
556	RO23	Qda Lorena AJ Antisana	f	\N	\N	3600		\N	\N	4	f
557	RO24	Río Tolda DJ Chaupibolsa	f	\N	\N	3620		\N	\N	4	f
558	RO25	Río Quijos Sur AJ  Pucalca	f	\N	\N	3600		\N	\N	4	f
559	RO26	Río Pucalca AJ Quijos Sur	f	\N	\N	3560		\N	\N	4	f
560	RO27	Río Pucalca	f	\N	\N	3380		\N	\N	4	f
563	RO30	Río Asufrado AJ Quijos Sur	f	\N	\N	\N		\N	\N	4	f
564	RO31	Río Quijos Norte DJ Tablón	f	\N	\N	\N		\N	\N	4	f
8	C08	IASA	t	509533.41	9956640.29	2727		9	11	2	f
34	H34	Papallacta	t	539642.40	9958274.93	3160		19	20	3	f
717	M5021	Yurafaccha Oyacachi	t	-78.11	-0.19	3710	documents/M5021.xlsx	19	27	2	t
718	M5022	Control Baños	t	-78.15	-0.32	3620	documents/M5022.xlsx	19	28	1	t
719	M5023	Papallacta	t	-78.14	-0.38	3100	documents/M5023.xlsx	19	28	1	t
720	M5024	El Tambo	t	-78.20	-0.38	3637	documents/M5024.xlsx	19	28	1	t
721	M5025	La Virgen Papallacta	t	-78.20	-0.33	3920	documents/M5025.xlsx	19	28	2	t
722	M5026	Cotopaxi Control Norte	t	-78.44	-0.56	3670	documents/M5026.xlsx	9	24	2	t
723	M5027	Lomahurco	t	-78.66	-0.58	3727	documents/M5027.xlsx	9	5	2	t
724	M5028	Hcda Prado Miranda	t	-78.39	-0.48	3526	documents/M5028.xlsx	9	24	2	t
725	M5029	El Carmen	t	-78.33	-0.50	4100	documents/M5029.xlsx	9	24	2	t
726	M5030	Hcda Gordillo	t	-78.36	-0.42	3248	documents/M5030.xlsx	9	24	1	t
727	M5031	Chumillos	t	-78.21	-0.09	3750	documents/M5031.xlsx	9	6	2	t
728	M5074	Puntas	t	-78.22	-0.17	4142	documents/M5074.xlsx	9	6	2	t
729	M5075	Itulcachi	t	-78.26	-0.29	4029	documents/M5075.xlsx	9	6	2	t
730	M5076	PNC	t	-78.40	-0.62	3866	documents/M5076.xlsx	9	24	1	t
731	M5077	REI	t	-78.69	-0.63	3983	documents/M5077.xlsx	9	5	1	t
732	M5078	Pifo	t	-78.32	-0.24	2857	documents/M5078.xlsx	9	6	1	t
733	H5006	Aglla en captacion	t	-78.20	-0.17	3765	documents/H5006.xlsx	9	6	3	t
734	JTU01PT11	Jatunhuaycu11	t	-78.24	-0.50	4023	documents/JTU_01_PT_11_FICHA.xlsx	19	10	1	t
735	JTU01PT22	Jatunhuaycu22	f	-78.24	-0.49	4104	documents/JTU_01_PT_22_FICHA.xlsx	19	10	1	t
736	JTU01PT32	Jatunhuaycu32	t	-78.24	-0.49	4148	documents/JTU_01_PT_32_FICHA.xlsx	19	10	1	t
737	JTU01PT42	Jatunhuaycu42	f	-78.24	-0.48	4110	documents/JTU_01_PT_43_FICHA.xlsx	19	10	1	t
738	JTU01PT53	Jatunhuaycu53	t	-78.24	-0.47	4271	documents/JTU_01_PT_53_FICHA.xlsx	19	10	1	t
739	JTU01PT63	Jatunhuaycu63	t	-78.23	-0.47	4203	documents/JTU_01_PT_63_FICHA.xlsx	19	10	1	t
740	JTU01PT73	Jatunhuaycu73	t	-78.23	-0.47	4231	documents/JTU_01_PT_73_FICHA.xlsx	19	10	1	t
741	JTU01PT83	Jatunhuaycu83	t	-78.21	-0.47	4289	documents/JTU_01_PT_83_FICHA.xlsx	19	10	1	t
742	JTU01HQ11	Jatunhuaycu11	t	-78.24	-0.50	4103	documents/JTU_01_HQ_11_FICHA.xlsx	19	10	3	t
743	JTU01HQ22	Jatunhuaycu22	t	-78.24	-0.49	4075	documents/JTU_01_HQ_22_FICHA.xlsx	19	10	3	t
744	JTU01HQ32	Jatunhuaycu32	t	-78.24	-0.48	4085	documents/JTU_01_HQ_32_FICHA.xlsx	19	10	3	t
745	JTU01HQ43	Jatunhuaycu43	t	-78.23	-0.47	4144	documents/JTU_01_HQ_43_FICHA.xlsx	19	10	3	t
746	H5028	Tayango antes captación	t	-78.59	-0.20	3825	documents/H5028_Tecnica.xlsx	9	1	3	t
747	M5125	Guamani Antisana	t	-78.26	-0.50	4148	documents/M5125_FICHA.xlsx	19	24	2	t
748	M5126	Jatunhuayco	t	-78.23	-0.49	4040	documents/H5126_FICHA.xlsx	19	10	2	t
749	H5025	Pita DJ Hualpaloma	t	-78.38	-0.62	3870	documents/H5025_Técnica.xlsx	9	24	3	t
750	M5179	Paluguillo	t	-78.23	-0.31	3685	documents/M5179_Tecnica.xlsx	9	6	2	t
751	H5026	Carihuayco en Paluguillo	t	-78.22	-0.34	3839	documents/H5026_Tecnica.xlsx	9	6	3	t
752	M5178	Tayango Guagua Pichincha	t	-78.59	-0.19	4077	documents/M5178_Tecnica.xlsx	9	1	2	t
753	M5181	Yuracyacu Guagua Pichincha	t	-78.59	-0.18	4220	documents/M5181_Tecnica.xlsx	9	1	1	t
754	ATP01PT01	Pluviometrica Tungurahua	t	-78.36	-0.60	3948	documents/ATP_01_PT_01_FICHA.xlsx	6	24	1	t
755	ATP01PT02	Pluviometrica Tungurahua-Chamilco	t	-78.37	-0.59	3973	documents/ATP_01_PT_02_FICHA.xlsx	6	24	1	t
756	ATP02PT01	Pluviometrica Chamilco	t	-78.37	-0.55	4111	documents/ATP_02_PT_01_FICHA.xlsx	6	24	1	t
757	ATP01HI01	Tungurahua	t	-78.39	-0.61	3840	documents/ATP_01_HI_01_FICHA.xlsx	6	24	3	t
758	ATP02HI01	Chamilco	t	-78.39	-0.61	3840	documents/ATP_02_HI_01_FICHA.xlsx	6	24	3	t
759	LLO02PO01	LLOA	f	-78.59	-0.19	4188	documents/LLO-02-PO-01.csv	9	1	1	t
760	LLO01PO02	LLOA	t	-78.59	-0.20	4076	documents/LLO-01-PO-02.csv	9	1	1	t
761	LLO01PO01	LLOA	t	-78.59	-0.20	3897	documents/LLO-01-PO-01.csv	9	1	1	t
762	LLO01HI01	LLOA	t	-78.59	-0.20	3824	documents/LLO-01-HI-01.csv	9	1	3	t
763	LLO02HI01	LLOA	t	-78.58	-0.19	4097	documents/LLO-02-HI-01.csv	9	1	3	t
764	H5027	Yuracyacu antes canal	t	-78.58	-0.19	4088	documents/H5027_Tecnica.xlsx	9	1	3	t
765	H5010	Jatunhuaycu	t	-78.25	-0.53	3943	documents/H5010_2017-3-29_nCfDK1e.csv	9	10	3	t
766	M5180	Atacazo	t	-78.60	-0.32	3865	documents/M5180_Tecnica.xlsx	9	6	2	t
767	M5182	Mindo Guagua Pichincha	t	-78.59	-0.17	4334	documents/M5182_Tecnica.xlsx	9	16	1	t
768	CAR02PT01	Pluviométrica Carachas	t	-78.61	-0.31	3575	documents/CAR02PT01.xlsx	9	36	1	t
769	H5010	Jatunhuaycu INAMHI	t	-78.25	-0.53	4050	documents/H5010_2017-3-29.csv	19	10	3	t
770	CAR02HC01	Carachas - Atacazo	t	-78.61	-0.31	3570	documents/CAR_02_HC_01_min5.dat	9	37	3	t
771	DQS01HC01	Dique Sur, Filtros Pichincha	t	-78.60	-0.33	3648	documents/1_min5_2020-01-08T14-21.dat	9	37	3	t
116	AB02	Qda CERRO NEGRO	f	\N	\N	\N		\N	\N	4	f
284	MS08	Río Alambrado	f	\N	\N	3920		\N	\N	4	f
394	NT16	Vert  Apangora	f	\N	\N	\N		\N	\N	4	f
565	RO32	Aporte 2 al Río Cristal	f	\N	\N	\N		\N	\N	4	f
566	RO33	Río Cristal en Captación	f	\N	\N	\N		\N	\N	4	f
567	RO34	Aporte 1 al Río Cristal	f	\N	\N	\N		\N	\N	4	f
568	RO35	Río Tablón en Captación	f	\N	\N	\N		\N	\N	4	f
569	RO36	Aporte Río Quijos Norte Campamento	f	\N	\N	\N		\N	\N	4	f
570	RO37	Aporte Río Quijos Norte en captación	f	\N	\N	\N		\N	\N	4	f
571	RO38	Río Quijos Norte AJ  Cristal	f	\N	\N	\N		\N	\N	4	f
572	RO39	Aporte 1 al  Río Chalpi Grande	f	\N	\N	\N		\N	\N	4	f
573	RO40	Aporte 2 al Río Chalpi Grande	f	\N	\N	\N		\N	\N	4	f
574	RO41	Río Verde Parte Alta captación	f	\N	\N	\N		\N	\N	4	f
575	RO42	Río Chalpi Grande Captación A	f	\N	\N	\N		\N	\N	4	f
576	RO43	Río Encantada captación (estación)	f	\N	\N	\N		\N	\N	4	f
577	RO45	Río Blanco Grande captación	f	\N	\N	\N		\N	\N	4	f
578	RO46	Río  Chalpi Grande captación C (estación)	f	\N	\N	\N		\N	\N	4	f
579	RO47	Río Chalpi Grande captación B (estación)	f	\N	\N	\N		\N	\N	4	f
580	RO48	Río Chalpi Grande captación A (estación)	f	\N	\N	\N		\N	\N	4	f
581	RO50	Qda. Huila	f	\N	\N	\N		\N	\N	4	f
582	RO51	Rio Zuno Coca Orellana	f	\N	\N	\N		\N	\N	4	f
583	SC01	Vertientes San Antonio piscinas	f	\N	\N	2340		\N	\N	4	f
584	SC02	Vertiente El Carnero	f	\N	\N	2720		\N	\N	4	f
585	SC04	Vertiente El Boliche	f	\N	\N	2800		\N	\N	4	f
586	SC05	Vertiente Curipoglio	f	\N	\N	3100		\N	\N	4	f
587	SC06	Vertiente Papatena	f	\N	\N	\N		\N	\N	4	f
588	SC07	Vertiente Papatena N°.-2	f	\N	\N	\N		\N	\N	4	f
589	SP04	Qda Atacazo	f	\N	\N	\N		\N	\N	4	f
590	SP05	Qda Cerro negro	f	\N	\N	\N		\N	\N	4	f
591	SP06	Canal Atacazo DJ Cerro Negro Romoleroux	f	\N	\N	\N		\N	\N	4	f
592	SP07	Canal Atacazo mas Qda. Cristal	f	\N	\N	\N		\N	\N	4	f
593	SP08	Canal Atacazo en Chusalongo	f	\N	\N	\N		\N	\N	4	f
594	SP09	Canal Atacazo vertedero El Rosario	f	\N	\N	\N		\N	\N	4	f
595	SP10	Canal Atacazo desarenador Checa	f	\N	\N	\N		\N	\N	4	f
596	SP11	Canal Atacazo sifón la Libertad	f	\N	\N	\N		\N	\N	4	f
597	SP12	Qda. Cristal para Canal Cerro Negro	f	\N	\N	\N		\N	\N	4	f
598	SP13	Qda.Cristal A. J Canal Atacazo (puente)	f	\N	\N	\N		\N	\N	4	f
599	SP14	Canal Atacazo A.J Qda. Cristal	f	\N	\N	\N		\N	\N	4	f
600	TP01	Planta Noroccidente	f	\N	\N	\N		\N	\N	4	f
601	TP02	Planta Cochapamba	f	\N	\N	\N		\N	\N	4	f
602	TP03	Planta Rumipamba	f	\N	\N	\N		\N	\N	4	f
603	TP04	Planta Placer	f	\N	\N	\N		\N	\N	4	f
604	TP05	Planta Toctiuco	f	\N	\N	\N		\N	\N	4	f
605	TP06	Planta Chilibulo	f	\N	\N	\N		\N	\N	4	f
606	TP07	Planta El Troje	f	\N	\N	\N		\N	\N	4	f
607	TP08	Planta Conocoto	f	\N	\N	\N		\N	\N	4	f
608	TP09	Planta El Quinche	f	\N	\N	2594		\N	\N	4	f
609	TP10	Planta Yaruqui	f	\N	\N	2584		\N	\N	4	f
610	TP11	Planta Checa	f	\N	\N	\N		\N	\N	4	f
611	TP12	Planta Tababela	f	\N	\N	2471		\N	\N	4	f
612	TP13	Planta Filambanco	f	\N	\N	2275		\N	\N	4	f
613	TP14	Planta IEOS	f	\N	\N	2319		\N	\N	4	f
614	TP15	Planta Uyachul	f	\N	\N	\N		\N	\N	4	f
615	TT01	Río Tamboyacu DJ Tambo estación	f	\N	\N	3515		\N	\N	4	f
616	TT02	Río Yanahurco AJ Valle	f	\N	\N	3600		\N	\N	4	f
617	TT03	Río Valle AJ Yanahurco	f	\N	\N	3600		\N	\N	4	f
618	TT04	Río Valle DJ Yanahurco total	f	\N	\N	2820		\N	\N	4	f
619	TT05	Qda Pazaguano	f	\N	\N	3880		\N	\N	4	f
620	TT06	Río Tambo estación 2A	f	\N	\N	3800		\N	\N	4	f
621	TT07	Qda Yaragcocha	f	\N	\N	4040		\N	\N	4	f
622	TT08	Río Tambo Sur	f	\N	\N	3980		\N	\N	4	f
623	TT10	Río Tambo Norte	f	\N	\N	3900		\N	\N	4	f
624	TT11	Qda Pucarrumi A	f	\N	\N	4000		\N	\N	4	f
625	TT12	Qda Curipogllo B	f	\N	\N	4000		\N	\N	4	f
626	TT13	Canal Alumis	f	\N	\N	3960		\N	\N	4	f
627	TT14	Río Tamboyacu estasción 5	f	\N	\N	3880		\N	\N	4	f
628	TT15	Qda Maucatambo	f	\N	\N	3840		\N	\N	4	f
629	TT16	Rio Tamboyacu DJ Zalazar	f	\N	\N	3660		\N	\N	4	f
630	TT17	Qda Gaspar Puñuna	f	\N	\N	3880		\N	\N	4	f
631	TT18	Río Yanahurco DJ Valle	f	\N	\N	3590		\N	\N	4	f
632	TT19	Qda Zalazar AJ Tamboyacu	f	\N	\N	4020		\N	\N	4	f
633	TT20	Qda Verdeloma	f	\N	\N	4080		\N	\N	4	f
634	TT21	Canal Alumis para Latacunga camino	f	\N	\N	3940		\N	\N	4	f
635	TT22	Río Tambo DJ Toruno	f	\N	\N	4000		\N	\N	4	f
636	TT23	Río Tamboyacu AJ  Tambo	f	\N	\N	\N		\N	\N	4	f
637	TT24	Río Tambo AJ Tamboyacu	f	\N	\N	\N		\N	\N	4	f
638	TT25	Qbda Toruno AJ Tambo	f	\N	\N	\N		\N	\N	4	f
639	TT26	Canal Alumis  en Mudadero	f	\N	\N	\N		\N	\N	4	f
640	VC01	Qda El Volcán (excedentes)	f	\N	\N	3080		\N	\N	4	f
641	VC02	Acequia La Cocha	f	\N	\N	3000		\N	\N	4	f
642	VC03	Acequia San Elias	f	\N	\N	3000		\N	\N	4	f
643	VC04	Acequia Valencia	f	\N	\N	3000		\N	\N	4	f
644	VC05	Acequia San Alfonso	f	\N	\N	3040		\N	\N	4	f
645	VC06	Vertiente de Secas	f	\N	\N	3440		\N	\N	4	f
646	VC08	Río Cariacu	f	\N	\N	2920		\N	\N	4	f
647	VC09	Qda Ubillus	f	\N	\N	2960		\N	\N	4	f
648	VC10	Vertiente Cariacu en galería	f	\N	\N	2920		\N	\N	4	f
649	VC11	Vertiente La Peña	f	\N	\N	2840		\N	\N	4	f
650	VC12	Río Pita (antes capt canal Tumbaco)	f	\N	\N	2760		\N	\N	4	f
651	VC13	Canal Tumbaco	f	\N	\N	2720		\N	\N	4	f
652	VC14	Entrada Laguna Secas	f	\N	\N	3440		\N	\N	4	f
653	VC15	Salida Laguna Secas	f	\N	\N	3400		\N	\N	4	f
654	VC16	Río Pita AJ Guapal	f	\N	\N	\N		\N	\N	4	f
655	VC17	Río Pita despues capt canal Tumbaco	f	\N	\N	\N		\N	\N	4	f
656	VC18	Bombeo del Volcan  para Yuraquí	f	\N	\N	\N		\N	\N	4	f
657	VC19	RIO TINAGILLA	f	\N	\N	\N		\N	\N	4	f
658	P74	Mogotes	t	538745.15	9970661.70	4003		19	18	1	f
75	P27	San Francisco	t	495580.29	9977632.63	3551		9	4	1	f
92	P45	El Quinche	t	523254.72	9987683.71	2686		9	9	1	f
115	P73	Rayocucho	t	500713.80	9996168.70	2901		9	10	1	f
19	H12	Pita Bocatoma	t	507165.22	9945068.14	3368		9	25	3	f
662	H61	Sucus A2	t	534805.74	9962954.61	3892		19	20	3	f
663	H59	Mogotes A2	t	538658.96	9970340.73	4008		19	18	3	f
664	H60	Mogotes A3	t	539265.66	9970719.71	4004		19	18	3	f
\.


--
-- Name: estacion_estacion_est_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.estacion_estacion_est_id_seq', 771, true);


--
-- PostgreSQL database dump complete
--

