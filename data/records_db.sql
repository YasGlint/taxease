--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3
-- Dumped by pg_dump version 16.3

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: dates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dates (
    date_id integer NOT NULL,
    date date,
    year integer,
    quarter integer
);


ALTER TABLE public.dates OWNER TO postgres;

--
-- Name: dates_date_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dates_date_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dates_date_id_seq OWNER TO postgres;

--
-- Name: dates_date_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dates_date_id_seq OWNED BY public.dates.date_id;


--
-- Name: tax_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tax_categories (
    tax_category_id integer NOT NULL,
    tax_category_name character varying(255)
);


ALTER TABLE public.tax_categories OWNER TO postgres;

--
-- Name: tax_categories_tax_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tax_categories_tax_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tax_categories_tax_category_id_seq OWNER TO postgres;

--
-- Name: tax_categories_tax_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tax_categories_tax_category_id_seq OWNED BY public.tax_categories.tax_category_id;


--
-- Name: tax_transactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tax_transactions (
    transaction_id integer NOT NULL,
    taxpayer_id integer,
    tax_category_id integer,
    date_id integer,
    amount numeric,
    annual_target numeric,
    quarterly_target numeric
);


ALTER TABLE public.tax_transactions OWNER TO postgres;

--
-- Name: tax_transactions_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tax_transactions_transaction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tax_transactions_transaction_id_seq OWNER TO postgres;

--
-- Name: tax_transactions_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tax_transactions_transaction_id_seq OWNED BY public.tax_transactions.transaction_id;


--
-- Name: taxpayers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.taxpayers (
    taxpayer_id integer NOT NULL,
    taxpayer_name character varying(255),
    location character varying(255)
);


ALTER TABLE public.taxpayers OWNER TO postgres;

--
-- Name: taxpayers_taxpayer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.taxpayers_taxpayer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.taxpayers_taxpayer_id_seq OWNER TO postgres;

--
-- Name: taxpayers_taxpayer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.taxpayers_taxpayer_id_seq OWNED BY public.taxpayers.taxpayer_id;


--
-- Name: dates date_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dates ALTER COLUMN date_id SET DEFAULT nextval('public.dates_date_id_seq'::regclass);


--
-- Name: tax_categories tax_category_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tax_categories ALTER COLUMN tax_category_id SET DEFAULT nextval('public.tax_categories_tax_category_id_seq'::regclass);


--
-- Name: tax_transactions transaction_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tax_transactions ALTER COLUMN transaction_id SET DEFAULT nextval('public.tax_transactions_transaction_id_seq'::regclass);


--
-- Name: taxpayers taxpayer_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxpayers ALTER COLUMN taxpayer_id SET DEFAULT nextval('public.taxpayers_taxpayer_id_seq'::regclass);


--
-- Data for Name: dates; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.dates (date_id, date, year, quarter) FROM stdin;
\.


--
-- Data for Name: tax_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tax_categories (tax_category_id, tax_category_name) FROM stdin;
190	PPT
191	oil taxes
192	Total
193	Oil Tax\nPetroleum Profits Tax
194	Company Income Tax
195	Gas Income
196	B\nCapital Gains Tax
197	Stamp Duty
198	total
199	Import VAT
200	D\nEDT
201	F\nNITDEF
202	Oil Tax\nCompany Income Tax
203	Capital Gains Tax
204	Petroleum Profits Tax
205	OIL TAX\nCompany Income Tax
206	OIL TAXES\nCompany Income Tax
207	Oil Taxes\nCompany Income Tax
208	Oil Tax\nPetroleum Profit Tax
209	D\nEDUCATION TAX
210	G\nElectronic Money Transfer Levy
\.


--
-- Data for Name: tax_transactions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tax_transactions (transaction_id, taxpayer_id, tax_category_id, date_id, amount, annual_target, quarterly_target) FROM stdin;
2	\N	\N	\N	266.9164	\N	\N
3	\N	\N	\N	523.8653	\N	\N
4	\N	\N	\N	790.7817	\N	\N
5	\N	\N	\N	265.3192	\N	\N
6	\N	\N	\N	0.9014	\N	\N
7	\N	\N	\N	0.2995	\N	\N
8	\N	\N	\N	1.4468	\N	\N
9	\N	\N	\N	267.9669	\N	\N
10	\N	\N	\N	47.0531	\N	\N
11	\N	\N	\N	136.3968	\N	\N
12	\N	\N	\N	183.4499	\N	\N
13	\N	\N	\N	59.8651	\N	\N
14	\N	\N	\N	1.1238	\N	\N
15	\N	\N	\N	329.3897	\N	\N
16	\N	\N	\N	426.9986	\N	\N
17	\N	\N	\N	756.3883	\N	\N
18	\N	\N	\N	164.7873	\N	\N
19	\N	\N	\N	2.3935	\N	\N
20	\N	\N	\N	1.7974	\N	\N
21	\N	\N	\N	168.9782	\N	\N
22	\N	\N	\N	49.868	\N	\N
23	\N	\N	\N	174.6063	\N	\N
24	\N	\N	\N	224.4743	\N	\N
25	\N	\N	\N	14.8401	\N	\N
26	\N	\N	\N	0.1205	\N	\N
27	\N	\N	\N	493.6067	\N	\N
28	\N	\N	\N	636.6406	\N	\N
29	\N	\N	\N	1130.2473	\N	\N
30	\N	\N	\N	313.4608	\N	\N
31	\N	\N	\N	0.399	\N	\N
32	\N	\N	\N	2.4794	\N	\N
33	\N	\N	\N	316.3392	\N	\N
34	\N	\N	\N	254.1039	\N	\N
35	\N	\N	\N	35.9885	\N	\N
36	\N	\N	\N	0.1708	\N	\N
37	\N	\N	\N	672.5694	\N	\N
38	\N	\N	\N	760.0463	\N	\N
39	\N	\N	\N	1432.6157	\N	\N
40	\N	\N	\N	371.3172	\N	\N
41	\N	\N	\N	7.1144	\N	\N
42	\N	\N	\N	0.2707	\N	\N
43	\N	\N	\N	5.3274	\N	\N
44	\N	\N	\N	384.0297	\N	\N
45	\N	\N	\N	56.5959	\N	\N
46	\N	\N	\N	241.4146	\N	\N
47	\N	\N	\N	298.0105	\N	\N
48	\N	\N	\N	57.9939	\N	\N
49	\N	\N	\N	0.1649	\N	\N
50	\N	\N	\N	525.5075	\N	\N
51	\N	\N	\N	724.3417	\N	\N
52	\N	\N	\N	1249.8492	\N	\N
53	\N	\N	\N	354.5373	\N	\N
54	\N	\N	\N	7.469	\N	\N
55	\N	\N	\N	3.6068	\N	\N
56	\N	\N	\N	7.3897	\N	\N
57	\N	\N	\N	373.0028	\N	\N
58	\N	\N	\N	60.6586	\N	\N
59	\N	\N	\N	249.224	\N	\N
60	\N	\N	\N	309.8826	\N	\N
61	\N	\N	\N	21.5674	\N	\N
62	\N	\N	\N	0.2602	\N	\N
63	\N	\N	\N	201.2455	\N	\N
64	\N	\N	\N	867.59	\N	\N
65	\N	\N	\N	1068.8355	\N	\N
66	\N	\N	\N	281.7342	\N	\N
67	\N	\N	\N	13.9878	\N	\N
68	\N	\N	\N	0.4742	\N	\N
69	\N	\N	\N	45.5659	\N	\N
70	\N	\N	\N	341.7621	\N	\N
71	\N	\N	\N	98.8109	\N	\N
72	\N	\N	\N	355.8774	\N	\N
73	\N	\N	\N	454.6883	\N	\N
74	\N	\N	\N	20.6394	\N	\N
75	\N	\N	\N	0.2669	\N	\N
76	\N	\N	\N	1059.17	\N	\N
77	\N	\N	\N	1150.69	\N	\N
78	\N	\N	\N	2209.86	\N	\N
79	\N	\N	\N	425.83	\N	\N
80	\N	\N	\N	34.77	\N	\N
81	\N	\N	\N	1.2	\N	\N
82	\N	\N	\N	21.35	\N	\N
83	\N	\N	\N	483.15	\N	\N
84	\N	\N	\N	436.82	\N	\N
85	\N	\N	\N	126.9	\N	\N
86	\N	\N	\N	56.46	\N	\N
87	\N	\N	\N	3.58	\N	\N
88	\N	\N	\N	111.84	\N	\N
89	\N	\N	\N	1095.01	\N	\N
90	\N	\N	\N	1585.63	\N	\N
91	\N	\N	\N	2680.64	\N	\N
92	\N	\N	\N	1095.0145	\N	\N
93	\N	\N	\N	731.0965	\N	\N
94	\N	\N	\N	35.7325	\N	\N
95	\N	\N	\N	20.4039	\N	\N
96	\N	\N	\N	29.6748	\N	\N
97	\N	\N	\N	816.9076	\N	\N
98	\N	\N	\N	567.9539	\N	\N
99	\N	\N	\N	129.425	\N	\N
100	\N	\N	\N	697.3789	\N	\N
101	\N	\N	\N	19.4333	\N	\N
102	\N	\N	\N	1.2014	\N	\N
103	\N	\N	\N	35.6803	\N	\N
\.


--
-- Data for Name: taxpayers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.taxpayers (taxpayer_id, taxpayer_name, location) FROM stdin;
1	Vick	Abuja
\.


--
-- Name: dates_date_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dates_date_id_seq', 1, false);


--
-- Name: tax_categories_tax_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tax_categories_tax_category_id_seq', 210, true);


--
-- Name: tax_transactions_transaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tax_transactions_transaction_id_seq', 103, true);


--
-- Name: taxpayers_taxpayer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.taxpayers_taxpayer_id_seq', 4, true);


--
-- Name: dates dates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dates
    ADD CONSTRAINT dates_pkey PRIMARY KEY (date_id);


--
-- Name: tax_categories tax_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tax_categories
    ADD CONSTRAINT tax_categories_pkey PRIMARY KEY (tax_category_id);


--
-- Name: tax_transactions tax_transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tax_transactions
    ADD CONSTRAINT tax_transactions_pkey PRIMARY KEY (transaction_id);


--
-- Name: taxpayers taxpayers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.taxpayers
    ADD CONSTRAINT taxpayers_pkey PRIMARY KEY (taxpayer_id);


--
-- Name: idx_date_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_date_id ON public.tax_transactions USING btree (date_id);


--
-- Name: idx_tax_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tax_category_id ON public.tax_transactions USING btree (tax_category_id);


--
-- Name: idx_taxpayer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_taxpayer_id ON public.tax_transactions USING btree (taxpayer_id);


--
-- Name: tax_transactions fk_taxpayer; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tax_transactions
    ADD CONSTRAINT fk_taxpayer FOREIGN KEY (taxpayer_id) REFERENCES public.taxpayers(taxpayer_id);


--
-- PostgreSQL database dump complete
--

