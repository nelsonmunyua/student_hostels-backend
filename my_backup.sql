--
-- PostgreSQL database dump
--

\restrict M4M6fOg5WK0VJPXnTGWZsv8KT2R3znDiGUSCuQdYPWF0tGkWQQizHR1gNL7jNA5

-- Dumped from database version 15.15 (Homebrew)
-- Dumped by pg_dump version 15.15 (Homebrew)

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
-- Name: booking_status; Type: TYPE; Schema: public; Owner: root
--

CREATE TYPE public.booking_status AS ENUM (
    'pending',
    'confirmed',
    'cancelled',
    'completed'
);


ALTER TYPE public.booking_status OWNER TO root;

--
-- Name: payment_methods; Type: TYPE; Schema: public; Owner: root
--

CREATE TYPE public.payment_methods AS ENUM (
    'mpesa',
    'card',
    'bank'
);


ALTER TYPE public.payment_methods OWNER TO root;

--
-- Name: payment_status; Type: TYPE; Schema: public; Owner: root
--

CREATE TYPE public.payment_status AS ENUM (
    'pending',
    'paid',
    'failed',
    'refunded'
);


ALTER TYPE public.payment_status OWNER TO root;

--
-- Name: role_type; Type: TYPE; Schema: public; Owner: root
--

CREATE TYPE public.role_type AS ENUM (
    'student',
    'host',
    'admin'
);


ALTER TYPE public.role_type OWNER TO root;

--
-- Name: room_types; Type: TYPE; Schema: public; Owner: root
--

CREATE TYPE public.room_types AS ENUM (
    'single',
    'double',
    'bed_sitter',
    'studio'
);


ALTER TYPE public.room_types OWNER TO root;

--
-- Name: ticket_status; Type: TYPE; Schema: public; Owner: root
--

CREATE TYPE public.ticket_status AS ENUM (
    'open',
    'in_progress',
    'resolved',
    'closed'
);


ALTER TYPE public.ticket_status OWNER TO root;

--
-- Name: verification_status; Type: TYPE; Schema: public; Owner: root
--

CREATE TYPE public.verification_status AS ENUM (
    'pending',
    'approved',
    'rejected'
);


ALTER TYPE public.verification_status OWNER TO root;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO root;

--
-- Name: bookings; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.bookings (
    id integer NOT NULL,
    student_id integer,
    room_id integer,
    start_date date NOT NULL,
    end_date date,
    status public.booking_status,
    total_amount integer NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.bookings OWNER TO root;

--
-- Name: bookings_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.bookings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bookings_id_seq OWNER TO root;

--
-- Name: bookings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.bookings_id_seq OWNED BY public.bookings.id;


--
-- Name: host_earnings; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.host_earnings (
    id integer NOT NULL,
    host_id integer,
    booking_id integer,
    gross_amount integer,
    commission integer,
    net_amount integer,
    created_at timestamp without time zone
);


ALTER TABLE public.host_earnings OWNER TO root;

--
-- Name: host_earnings_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.host_earnings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.host_earnings_id_seq OWNER TO root;

--
-- Name: host_earnings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.host_earnings_id_seq OWNED BY public.host_earnings.id;


--
-- Name: host_verifications; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.host_verifications (
    id integer NOT NULL,
    host_id integer,
    document_type character varying(50),
    document_url character varying(255),
    status public.verification_status,
    reviewed_by integer,
    reviewed_at timestamp without time zone,
    created_at timestamp without time zone
);


ALTER TABLE public.host_verifications OWNER TO root;

--
-- Name: host_verifications_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.host_verifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.host_verifications_id_seq OWNER TO root;

--
-- Name: host_verifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.host_verifications_id_seq OWNED BY public.host_verifications.id;


--
-- Name: hostels; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.hostels (
    id integer NOT NULL,
    host_id integer,
    name character varying(255) NOT NULL,
    description text,
    location character varying(255) NOT NULL,
    latitude double precision,
    longitude double precision,
    amenities json,
    rules text,
    is_verified boolean,
    is_active boolean,
    created_at timestamp without time zone
);


ALTER TABLE public.hostels OWNER TO root;

--
-- Name: hostels_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.hostels_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hostels_id_seq OWNER TO root;

--
-- Name: hostels_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.hostels_id_seq OWNED BY public.hostels.id;


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.notifications (
    id integer NOT NULL,
    user_id integer,
    title character varying(255),
    message text,
    is_read boolean,
    created_at timestamp without time zone
);


ALTER TABLE public.notifications OWNER TO root;

--
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notifications_id_seq OWNER TO root;

--
-- Name: notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;


--
-- Name: payments; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.payments (
    id integer NOT NULL,
    booking_id integer,
    reference character varying(100),
    method public.payment_methods NOT NULL,
    amount integer NOT NULL,
    status public.payment_status,
    paid_at timestamp without time zone,
    created_at timestamp without time zone
);


ALTER TABLE public.payments OWNER TO root;

--
-- Name: payments_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.payments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.payments_id_seq OWNER TO root;

--
-- Name: payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.payments_id_seq OWNED BY public.payments.id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.reviews (
    id integer NOT NULL,
    booking_id integer,
    user_id integer,
    hostel_id integer,
    rating integer NOT NULL,
    comment text,
    created_at timestamp without time zone
);


ALTER TABLE public.reviews OWNER TO root;

--
-- Name: reviews_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.reviews_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reviews_id_seq OWNER TO root;

--
-- Name: reviews_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.reviews_id_seq OWNED BY public.reviews.id;


--
-- Name: room_availability; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.room_availability (
    id integer NOT NULL,
    room_id integer,
    date date NOT NULL,
    is_available boolean
);


ALTER TABLE public.room_availability OWNER TO root;

--
-- Name: room_availability_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.room_availability_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.room_availability_id_seq OWNER TO root;

--
-- Name: room_availability_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.room_availability_id_seq OWNED BY public.room_availability.id;


--
-- Name: rooms; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.rooms (
    id integer NOT NULL,
    hostel_id integer,
    room_type public.room_types NOT NULL,
    price integer NOT NULL,
    capacity integer,
    available_units integer,
    is_available boolean,
    created_at timestamp without time zone
);


ALTER TABLE public.rooms OWNER TO root;

--
-- Name: rooms_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.rooms_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rooms_id_seq OWNER TO root;

--
-- Name: rooms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.rooms_id_seq OWNED BY public.rooms.id;


--
-- Name: settings; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.settings (
    id integer NOT NULL,
    key character varying(100),
    value character varying(255),
    updated_at timestamp without time zone
);


ALTER TABLE public.settings OWNER TO root;

--
-- Name: settings_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.settings_id_seq OWNER TO root;

--
-- Name: settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.settings_id_seq OWNED BY public.settings.id;


--
-- Name: support_tickets; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.support_tickets (
    id integer NOT NULL,
    user_id integer,
    subject character varying(255),
    message text,
    status public.ticket_status,
    created_at timestamp without time zone
);


ALTER TABLE public.support_tickets OWNER TO root;

--
-- Name: support_tickets_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.support_tickets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.support_tickets_id_seq OWNER TO root;

--
-- Name: support_tickets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.support_tickets_id_seq OWNED BY public.support_tickets.id;


--
-- Name: tokens; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.tokens (
    id integer NOT NULL,
    user_id integer NOT NULL,
    token character varying(255) NOT NULL,
    token_type character varying(50) NOT NULL,
    expires_at timestamp without time zone,
    created_at timestamp without time zone
);


ALTER TABLE public.tokens OWNER TO root;

--
-- Name: tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tokens_id_seq OWNER TO root;

--
-- Name: tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.tokens_id_seq OWNED BY public.tokens.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.users (
    id integer NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    phone character varying(20),
    role public.role_type NOT NULL,
    is_verified boolean,
    last_login_at timestamp without time zone,
    login_count integer,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO root;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO root;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: wishlists; Type: TABLE; Schema: public; Owner: root
--

CREATE TABLE public.wishlists (
    id integer NOT NULL,
    user_id integer,
    hostel_id integer,
    created_at timestamp without time zone
);


ALTER TABLE public.wishlists OWNER TO root;

--
-- Name: wishlists_id_seq; Type: SEQUENCE; Schema: public; Owner: root
--

CREATE SEQUENCE public.wishlists_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wishlists_id_seq OWNER TO root;

--
-- Name: wishlists_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: root
--

ALTER SEQUENCE public.wishlists_id_seq OWNED BY public.wishlists.id;


--
-- Name: bookings id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.bookings ALTER COLUMN id SET DEFAULT nextval('public.bookings_id_seq'::regclass);


--
-- Name: host_earnings id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.host_earnings ALTER COLUMN id SET DEFAULT nextval('public.host_earnings_id_seq'::regclass);


--
-- Name: host_verifications id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.host_verifications ALTER COLUMN id SET DEFAULT nextval('public.host_verifications_id_seq'::regclass);


--
-- Name: hostels id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.hostels ALTER COLUMN id SET DEFAULT nextval('public.hostels_id_seq'::regclass);


--
-- Name: notifications id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);


--
-- Name: payments id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.payments ALTER COLUMN id SET DEFAULT nextval('public.payments_id_seq'::regclass);


--
-- Name: reviews id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.reviews ALTER COLUMN id SET DEFAULT nextval('public.reviews_id_seq'::regclass);


--
-- Name: room_availability id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.room_availability ALTER COLUMN id SET DEFAULT nextval('public.room_availability_id_seq'::regclass);


--
-- Name: rooms id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.rooms ALTER COLUMN id SET DEFAULT nextval('public.rooms_id_seq'::regclass);


--
-- Name: settings id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.settings ALTER COLUMN id SET DEFAULT nextval('public.settings_id_seq'::regclass);


--
-- Name: support_tickets id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.support_tickets ALTER COLUMN id SET DEFAULT nextval('public.support_tickets_id_seq'::regclass);


--
-- Name: tokens id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.tokens ALTER COLUMN id SET DEFAULT nextval('public.tokens_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: wishlists id; Type: DEFAULT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.wishlists ALTER COLUMN id SET DEFAULT nextval('public.wishlists_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.alembic_version (version_num) FROM stdin;
1b7d00e6ee49
\.


--
-- Data for Name: bookings; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.bookings (id, student_id, room_id, start_date, end_date, status, total_amount, created_at) FROM stdin;
1	5	9	2025-12-02	2026-05-14	pending	113817	2025-11-28 15:26:53.159169
2	5	17	2025-11-22	2026-01-13	completed	27521	2025-11-16 15:26:53.163377
3	6	8	2026-01-01	2026-06-10	completed	116325	2025-12-23 15:26:53.176849
4	6	5	2025-12-25	2026-01-29	completed	22634	2025-12-21 15:26:53.184171
5	6	16	2026-01-09	2026-04-26	confirmed	73437	2026-01-03 15:26:53.195133
6	7	20	2025-12-29	2026-04-01	cancelled	68107	2025-12-26 15:26:53.203387
7	7	5	2025-12-15	2026-02-13	cancelled	38802	2025-12-12 15:26:53.217129
8	7	13	2026-01-27	2026-05-12	confirmed	69538	2026-01-20 15:26:53.218165
9	7	19	2025-12-12	2026-01-21	completed	11806	2025-12-11 15:26:53.233116
10	8	16	2025-11-25	2026-05-10	confirmed	113931	2025-11-24 15:26:53.243049
11	8	8	2026-01-21	2026-06-18	cancelled	107600	2026-01-16 15:26:53.243148
\.


--
-- Data for Name: host_earnings; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.host_earnings (id, host_id, booking_id, gross_amount, commission, net_amount, created_at) FROM stdin;
1	3	2	27521	2752	24769	2025-11-17 15:26:53.163377
2	2	3	116325	11632	104693	2025-12-24 15:26:53.176849
3	2	4	22634	2263	20371	2025-12-22 15:26:53.184171
4	2	5	73437	7343	66094	2026-01-04 15:26:53.195133
5	2	8	69538	6953	62585	2026-01-21 15:26:53.218165
6	3	9	11806	1180	10626	2025-12-12 15:26:53.233116
7	2	10	113931	11393	102538	2025-11-25 15:26:53.243049
\.


--
-- Data for Name: host_verifications; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.host_verifications (id, host_id, document_type, document_url, status, reviewed_by, reviewed_at, created_at) FROM stdin;
1	2	Lease Agreement	https://storage.hostelhub.com/documents/2/document.pdf	approved	1	2026-01-13 15:26:52.958771	2025-12-25 15:26:52.958786
2	3	ID	https://storage.hostelhub.com/documents/3/document.pdf	approved	1	2026-01-25 15:26:52.958935	2026-01-19 15:26:52.958942
3	4	ID	https://storage.hostelhub.com/documents/4/document.pdf	pending	\N	\N	2026-01-25 15:26:52.959014
\.


--
-- Data for Name: hostels; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.hostels (id, host_id, name, description, location, latitude, longitude, amenities, rules, is_verified, is_active, created_at) FROM stdin;
1	2	Campus View Apartments	Modern student apartments with great campus views. Perfect for serious students.	Westlands, Nairobi	-1.2625	36.8022	["wifi", "water", "security", "parking", "laundry", "gym", "study_room"]	No pets. No smoking. Quiet hours 10PM-7AM.	t	t	2025-05-14 15:26:52.999136
2	2	Green Valley Hostel	Eco-friendly hostel with beautiful gardens and study spaces.	Kilimani, Nairobi	-1.2921	36.7921	["wifi", "water", "security", "parking", "garden", "library"]	Sustainable living encouraged. Recycling mandatory.	t	t	2025-03-06 15:26:53.053337
3	3	University Heights	Affordable accommodation near the university. Great for budget-conscious students.	Kileleshwa, Nairobi	-1.271	36.7825	["wifi", "water", "security", "common_room"]	Visitors allowed until 9PM. Monthly cleaning required.	t	t	2025-11-26 15:26:53.075329
4	4	Digital Nomad Hub	High-speed internet and coworking spaces for tech students.	Upper Hill, Nairobi	-1.2833	36.8167	["wifi", "water", "security", "parking", "coworking", "printing"]	24/7 access. Respect quiet zones.	f	t	2025-08-21 15:26:53.085387
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.notifications (id, user_id, title, message, is_read, created_at) FROM stdin;
1	1	Message	Payment received successfully	t	2026-01-25 15:26:53.650291
2	1	Message	Your booking has been confirmed!	f	2026-01-20 15:26:53.650429
3	1	Message	Booking reminder: Check-in tomorrow	t	2026-01-15 15:26:53.650492
4	1	Message	New message from a host	t	2026-02-07 15:26:53.650546
5	1	Message	Welcome to HostelHub!	t	2026-02-04 15:26:53.650598
6	1	Booking Update	Welcome to HostelHub!	t	2026-01-16 15:26:53.650648
7	2	Booking Update	Payment received successfully	f	2026-01-15 15:26:53.661703
8	2	System	New message from a host	t	2026-01-12 15:26:53.661883
9	3	Message	Welcome to HostelHub!	t	2026-01-12 15:26:53.669473
10	3	System	Your booking has been confirmed!	t	2026-01-08 15:26:53.669638
11	3	Booking Update	New review on your hostel	t	2026-01-18 15:26:53.669726
12	4	Message	Payment received successfully	f	2026-01-09 15:26:53.676919
13	4	Booking Update	Payment received successfully	t	2026-02-01 15:26:53.677113
14	4	Payment	Host verification approved	t	2026-01-24 15:26:53.677268
15	4	Message	Your booking has been confirmed!	f	2026-02-06 15:26:53.677358
16	4	Message	Booking reminder: Check-in tomorrow	t	2026-01-14 15:26:53.677414
17	4	Booking Update	Maintenance scheduled for this weekend	t	2026-01-10 15:26:53.677467
18	5	Booking Update	New review on your hostel	t	2026-01-13 15:26:53.683875
19	5	Message	New review on your hostel	t	2026-02-01 15:26:53.684007
20	5	Payment	Special discount available	t	2026-01-29 15:26:53.684068
21	5	Booking Update	Welcome to HostelHub!	t	2026-01-29 15:26:53.684125
22	5	Booking Update	New review on your hostel	t	2026-01-11 15:26:53.684177
23	5	Booking Update	Booking reminder: Check-in tomorrow	t	2026-01-12 15:26:53.684228
24	5	System	Welcome to HostelHub!	t	2026-01-16 15:26:53.684277
25	5	Message	Your payment is due tomorrow	f	2026-01-28 15:26:53.684326
26	6	Message	Your payment is due tomorrow	f	2026-01-31 15:26:53.695942
27	6	Booking Update	Payment received successfully	t	2026-01-19 15:26:53.696355
28	6	System	Special discount available	f	2026-01-23 15:26:53.696456
29	6	Payment	Welcome to HostelHub!	t	2026-01-27 15:26:53.69652
30	6	Message	New message from a host	f	2026-01-24 15:26:53.696578
31	6	Booking Update	Your booking has been confirmed!	t	2026-01-10 15:26:53.696634
32	6	System	Special discount available	f	2026-01-23 15:26:53.696689
33	7	System	Maintenance scheduled for this weekend	t	2026-01-25 15:26:53.700925
34	7	System	Your booking has been confirmed!	f	2026-02-02 15:26:53.701062
35	7	Message	Booking reminder: Check-in tomorrow	f	2026-01-16 15:26:53.701123
36	8	Booking Update	Maintenance scheduled for this weekend	t	2026-01-26 15:26:53.709158
37	8	Message	Host verification approved	t	2026-02-06 15:26:53.7093
38	8	System	Maintenance scheduled for this weekend	t	2026-01-27 15:26:53.709361
39	8	System	Welcome to HostelHub!	f	2026-01-21 15:26:53.709415
40	8	Booking Update	Your booking has been confirmed!	t	2026-01-23 15:26:53.709467
41	8	Booking Update	Welcome to HostelHub!	t	2026-01-16 15:26:53.709518
42	8	Payment	Maintenance scheduled for this weekend	t	2026-01-27 15:26:53.709567
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.payments (id, booking_id, reference, method, amount, status, paid_at, created_at) FROM stdin;
1	1	PYMT421563	card	113817	pending	\N	2025-11-28 15:26:53.159169
2	2	PYMT188301	bank	9173	paid	2025-11-19 15:26:53.163377	2025-11-16 15:26:53.163377
3	2	PYMT409953	card	9173	paid	2025-11-17 15:26:53.163377	2025-11-17 15:26:53.163377
4	2	PYMT446772	card	9175	paid	2025-11-19 15:26:53.163377	2025-11-18 15:26:53.163377
5	3	PYMT931029	card	58162	paid	2025-12-25 15:26:53.176849	2025-12-23 15:26:53.176849
6	3	PYMT472183	bank	58163	paid	2025-12-25 15:26:53.176849	2025-12-24 15:26:53.176849
7	4	PYMT357820	mpesa	11317	paid	2025-12-23 15:26:53.184171	2025-12-21 15:26:53.184171
8	4	PYMT115647	bank	11317	paid	2025-12-24 15:26:53.184171	2025-12-22 15:26:53.184171
9	5	PYMT451769	card	73437	paid	2026-01-04 15:26:53.195133	2026-01-03 15:26:53.195133
10	8	PYMT503577	card	69538	paid	2026-01-21 15:26:53.218165	2026-01-20 15:26:53.218165
11	9	PYMT958293	mpesa	5903	paid	2025-12-14 15:26:53.233116	2025-12-11 15:26:53.233116
12	9	PYMT487180	bank	5903	paid	2025-12-12 15:26:53.233116	2025-12-12 15:26:53.233116
13	10	PYMT694134	card	113931	paid	2025-11-25 15:26:53.243049	2025-11-24 15:26:53.243049
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.reviews (id, booking_id, user_id, hostel_id, rating, comment, created_at) FROM stdin;
1	3	6	1	3	Great place to stay! Very clean and comfortable.	2026-06-15 00:00:00
2	9	7	3	3	Minor issues but overall good experience.	2026-01-22 00:00:00
\.


--
-- Data for Name: room_availability; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.room_availability (id, room_id, date, is_available) FROM stdin;
1	1	2026-02-07	t
2	1	2026-02-08	t
3	1	2026-02-09	t
4	1	2026-02-10	f
5	1	2026-02-11	f
6	1	2026-02-12	t
7	1	2026-02-13	t
8	1	2026-02-14	t
9	1	2026-02-15	t
10	1	2026-02-16	t
11	1	2026-02-17	t
12	1	2026-02-18	t
13	1	2026-02-19	t
14	1	2026-02-20	f
15	1	2026-02-21	t
16	1	2026-02-22	t
17	1	2026-02-23	t
18	1	2026-02-24	t
19	1	2026-02-25	f
20	1	2026-02-26	f
21	1	2026-02-27	f
22	1	2026-02-28	t
23	1	2026-03-01	t
24	1	2026-03-02	t
25	1	2026-03-03	t
26	1	2026-03-04	t
27	1	2026-03-05	f
28	1	2026-03-06	t
29	1	2026-03-07	t
30	1	2026-03-08	t
31	1	2026-03-09	t
32	1	2026-03-10	t
33	1	2026-03-11	f
34	1	2026-03-12	t
35	1	2026-03-13	t
36	1	2026-03-14	f
37	1	2026-03-15	t
38	1	2026-03-16	f
39	1	2026-03-17	t
40	1	2026-03-18	f
41	1	2026-03-19	t
42	1	2026-03-20	f
43	1	2026-03-21	f
44	1	2026-03-22	t
45	1	2026-03-23	t
46	1	2026-03-24	f
47	1	2026-03-25	t
48	1	2026-03-26	t
49	1	2026-03-27	t
50	1	2026-03-28	t
51	1	2026-03-29	t
52	1	2026-03-30	t
53	1	2026-03-31	t
54	1	2026-04-01	t
55	1	2026-04-02	t
56	1	2026-04-03	t
57	1	2026-04-04	t
58	1	2026-04-05	t
59	1	2026-04-06	t
60	1	2026-04-07	t
61	1	2026-04-08	t
62	1	2026-04-09	t
63	1	2026-04-10	t
64	1	2026-04-11	t
65	1	2026-04-12	f
66	1	2026-04-13	f
67	1	2026-04-14	t
68	1	2026-04-15	t
69	1	2026-04-16	t
70	1	2026-04-17	f
71	1	2026-04-18	t
72	1	2026-04-19	t
73	1	2026-04-20	t
74	1	2026-04-21	t
75	1	2026-04-22	t
76	1	2026-04-23	t
77	1	2026-04-24	t
78	1	2026-04-25	t
79	1	2026-04-26	t
80	1	2026-04-27	t
81	1	2026-04-28	f
82	1	2026-04-29	t
83	1	2026-04-30	t
84	1	2026-05-01	t
85	1	2026-05-02	t
86	1	2026-05-03	f
87	1	2026-05-04	f
88	1	2026-05-05	t
89	1	2026-05-06	t
90	1	2026-05-07	f
91	2	2026-02-07	t
92	2	2026-02-08	t
93	2	2026-02-09	t
94	2	2026-02-10	t
95	2	2026-02-11	t
96	2	2026-02-12	t
97	2	2026-02-13	t
98	2	2026-02-14	t
99	2	2026-02-15	t
100	2	2026-02-16	t
101	2	2026-02-17	f
102	2	2026-02-18	t
103	2	2026-02-19	t
104	2	2026-02-20	t
105	2	2026-02-21	f
106	2	2026-02-22	t
107	2	2026-02-23	t
108	2	2026-02-24	t
109	2	2026-02-25	t
110	2	2026-02-26	t
111	2	2026-02-27	t
112	2	2026-02-28	t
113	2	2026-03-01	t
114	2	2026-03-02	t
115	2	2026-03-03	t
116	2	2026-03-04	t
117	2	2026-03-05	t
118	2	2026-03-06	t
119	2	2026-03-07	t
120	2	2026-03-08	t
121	2	2026-03-09	f
122	2	2026-03-10	t
123	2	2026-03-11	t
124	2	2026-03-12	t
125	2	2026-03-13	f
126	2	2026-03-14	f
127	2	2026-03-15	t
128	2	2026-03-16	f
129	2	2026-03-17	f
130	2	2026-03-18	f
131	2	2026-03-19	t
132	2	2026-03-20	t
133	2	2026-03-21	f
134	2	2026-03-22	t
135	2	2026-03-23	t
136	2	2026-03-24	t
137	2	2026-03-25	t
138	2	2026-03-26	f
139	2	2026-03-27	f
140	2	2026-03-28	f
141	2	2026-03-29	t
142	2	2026-03-30	t
143	2	2026-03-31	t
144	2	2026-04-01	t
145	2	2026-04-02	f
146	2	2026-04-03	f
147	2	2026-04-04	t
148	2	2026-04-05	t
149	2	2026-04-06	f
150	2	2026-04-07	f
151	2	2026-04-08	t
152	2	2026-04-09	t
153	2	2026-04-10	t
154	2	2026-04-11	t
155	2	2026-04-12	f
156	2	2026-04-13	t
157	2	2026-04-14	t
158	2	2026-04-15	t
159	2	2026-04-16	t
160	2	2026-04-17	t
161	2	2026-04-18	f
162	2	2026-04-19	t
163	2	2026-04-20	t
164	2	2026-04-21	t
165	2	2026-04-22	f
166	2	2026-04-23	t
167	2	2026-04-24	t
168	2	2026-04-25	t
169	2	2026-04-26	t
170	2	2026-04-27	t
171	2	2026-04-28	t
172	2	2026-04-29	t
173	2	2026-04-30	t
174	2	2026-05-01	t
175	2	2026-05-02	t
176	2	2026-05-03	t
177	2	2026-05-04	t
178	2	2026-05-05	t
179	2	2026-05-06	t
180	2	2026-05-07	f
181	3	2026-02-07	t
182	3	2026-02-08	t
183	3	2026-02-09	t
184	3	2026-02-10	t
185	3	2026-02-11	t
186	3	2026-02-12	t
187	3	2026-02-13	t
188	3	2026-02-14	t
189	3	2026-02-15	t
190	3	2026-02-16	f
191	3	2026-02-17	f
192	3	2026-02-18	t
193	3	2026-02-19	t
194	3	2026-02-20	f
195	3	2026-02-21	t
196	3	2026-02-22	t
197	3	2026-02-23	t
198	3	2026-02-24	t
199	3	2026-02-25	t
200	3	2026-02-26	f
201	3	2026-02-27	f
202	3	2026-02-28	t
203	3	2026-03-01	t
204	3	2026-03-02	f
205	3	2026-03-03	f
206	3	2026-03-04	t
207	3	2026-03-05	t
208	3	2026-03-06	t
209	3	2026-03-07	t
210	3	2026-03-08	f
211	3	2026-03-09	f
212	3	2026-03-10	t
213	3	2026-03-11	f
214	3	2026-03-12	f
215	3	2026-03-13	f
216	3	2026-03-14	t
217	3	2026-03-15	t
218	3	2026-03-16	t
219	3	2026-03-17	t
220	3	2026-03-18	f
221	3	2026-03-19	f
222	3	2026-03-20	f
223	3	2026-03-21	t
224	3	2026-03-22	t
225	3	2026-03-23	t
226	3	2026-03-24	f
227	3	2026-03-25	f
228	3	2026-03-26	f
229	3	2026-03-27	t
230	3	2026-03-28	t
231	3	2026-03-29	t
232	3	2026-03-30	t
233	3	2026-03-31	t
234	3	2026-04-01	t
235	3	2026-04-02	t
236	3	2026-04-03	t
237	3	2026-04-04	f
238	3	2026-04-05	f
239	3	2026-04-06	t
240	3	2026-04-07	t
241	3	2026-04-08	f
242	3	2026-04-09	t
243	3	2026-04-10	t
244	3	2026-04-11	t
245	3	2026-04-12	t
246	3	2026-04-13	t
247	3	2026-04-14	f
248	3	2026-04-15	t
249	3	2026-04-16	t
250	3	2026-04-17	t
251	3	2026-04-18	f
252	3	2026-04-19	t
253	3	2026-04-20	f
254	3	2026-04-21	f
255	3	2026-04-22	t
256	3	2026-04-23	f
257	3	2026-04-24	t
258	3	2026-04-25	t
259	3	2026-04-26	t
260	3	2026-04-27	t
261	3	2026-04-28	t
262	3	2026-04-29	t
263	3	2026-04-30	t
264	3	2026-05-01	f
265	3	2026-05-02	t
266	3	2026-05-03	f
267	3	2026-05-04	t
268	3	2026-05-05	t
269	3	2026-05-06	t
270	3	2026-05-07	t
271	4	2026-02-07	t
272	4	2026-02-08	t
273	4	2026-02-09	t
274	4	2026-02-10	t
275	4	2026-02-11	t
276	4	2026-02-12	t
277	4	2026-02-13	t
278	4	2026-02-14	t
279	4	2026-02-15	t
280	4	2026-02-16	t
281	4	2026-02-17	f
282	4	2026-02-18	t
283	4	2026-02-19	t
284	4	2026-02-20	t
285	4	2026-02-21	t
286	4	2026-02-22	t
287	4	2026-02-23	t
288	4	2026-02-24	f
289	4	2026-02-25	f
290	4	2026-02-26	t
291	4	2026-02-27	f
292	4	2026-02-28	t
293	4	2026-03-01	t
294	4	2026-03-02	t
295	4	2026-03-03	t
296	4	2026-03-04	t
297	4	2026-03-05	t
298	4	2026-03-06	t
299	4	2026-03-07	t
300	4	2026-03-08	t
301	4	2026-03-09	t
302	4	2026-03-10	f
303	4	2026-03-11	t
304	4	2026-03-12	t
305	4	2026-03-13	t
306	4	2026-03-14	t
307	4	2026-03-15	t
308	4	2026-03-16	f
309	4	2026-03-17	f
310	4	2026-03-18	t
311	4	2026-03-19	t
312	4	2026-03-20	t
313	4	2026-03-21	t
314	4	2026-03-22	t
315	4	2026-03-23	f
316	4	2026-03-24	t
317	4	2026-03-25	f
318	4	2026-03-26	t
319	4	2026-03-27	f
320	4	2026-03-28	t
321	4	2026-03-29	t
322	4	2026-03-30	f
323	4	2026-03-31	t
324	4	2026-04-01	f
325	4	2026-04-02	t
326	4	2026-04-03	t
327	4	2026-04-04	t
328	4	2026-04-05	t
329	4	2026-04-06	t
330	4	2026-04-07	t
331	4	2026-04-08	f
332	4	2026-04-09	t
333	4	2026-04-10	f
334	4	2026-04-11	t
335	4	2026-04-12	t
336	4	2026-04-13	t
337	4	2026-04-14	f
338	4	2026-04-15	t
339	4	2026-04-16	t
340	4	2026-04-17	t
341	4	2026-04-18	t
342	4	2026-04-19	t
343	4	2026-04-20	f
344	4	2026-04-21	f
345	4	2026-04-22	t
346	4	2026-04-23	f
347	4	2026-04-24	t
348	4	2026-04-25	f
349	4	2026-04-26	t
350	4	2026-04-27	t
351	4	2026-04-28	f
352	4	2026-04-29	t
353	4	2026-04-30	f
354	4	2026-05-01	f
355	4	2026-05-02	t
356	4	2026-05-03	t
357	4	2026-05-04	t
358	4	2026-05-05	t
359	4	2026-05-06	t
360	4	2026-05-07	f
361	5	2026-02-07	t
362	5	2026-02-08	t
363	5	2026-02-09	t
364	5	2026-02-10	t
365	5	2026-02-11	t
366	5	2026-02-12	t
367	5	2026-02-13	t
368	5	2026-02-14	t
369	5	2026-02-15	t
370	5	2026-02-16	t
371	5	2026-02-17	t
372	5	2026-02-18	t
373	5	2026-02-19	t
374	5	2026-02-20	t
375	5	2026-02-21	t
376	5	2026-02-22	t
377	5	2026-02-23	t
378	5	2026-02-24	t
379	5	2026-02-25	f
380	5	2026-02-26	f
381	5	2026-02-27	f
382	5	2026-02-28	f
383	5	2026-03-01	t
384	5	2026-03-02	t
385	5	2026-03-03	t
386	5	2026-03-04	t
387	5	2026-03-05	t
388	5	2026-03-06	t
389	5	2026-03-07	t
390	5	2026-03-08	t
391	5	2026-03-09	t
392	5	2026-03-10	t
393	5	2026-03-11	t
394	5	2026-03-12	t
395	5	2026-03-13	t
396	5	2026-03-14	t
397	5	2026-03-15	t
398	5	2026-03-16	t
399	5	2026-03-17	f
400	5	2026-03-18	f
401	5	2026-03-19	t
402	5	2026-03-20	t
403	5	2026-03-21	t
404	5	2026-03-22	t
405	5	2026-03-23	t
406	5	2026-03-24	t
407	5	2026-03-25	f
408	5	2026-03-26	t
409	5	2026-03-27	t
410	5	2026-03-28	t
411	5	2026-03-29	f
412	5	2026-03-30	f
413	5	2026-03-31	t
414	5	2026-04-01	t
415	5	2026-04-02	t
416	5	2026-04-03	t
417	5	2026-04-04	f
418	5	2026-04-05	t
419	5	2026-04-06	t
420	5	2026-04-07	t
421	5	2026-04-08	t
422	5	2026-04-09	t
423	5	2026-04-10	t
424	5	2026-04-11	f
425	5	2026-04-12	t
426	5	2026-04-13	f
427	5	2026-04-14	t
428	5	2026-04-15	f
429	5	2026-04-16	t
430	5	2026-04-17	t
431	5	2026-04-18	t
432	5	2026-04-19	t
433	5	2026-04-20	t
434	5	2026-04-21	t
435	5	2026-04-22	t
436	5	2026-04-23	f
437	5	2026-04-24	f
438	5	2026-04-25	t
439	5	2026-04-26	t
440	5	2026-04-27	t
441	5	2026-04-28	f
442	5	2026-04-29	t
443	5	2026-04-30	f
444	5	2026-05-01	t
445	5	2026-05-02	t
446	5	2026-05-03	t
447	5	2026-05-04	t
448	5	2026-05-05	t
449	5	2026-05-06	t
450	5	2026-05-07	t
451	6	2026-02-07	t
452	6	2026-02-08	f
453	6	2026-02-09	t
454	6	2026-02-10	t
455	6	2026-02-11	t
456	6	2026-02-12	t
457	6	2026-02-13	t
458	6	2026-02-14	t
459	6	2026-02-15	t
460	6	2026-02-16	t
461	6	2026-02-17	t
462	6	2026-02-18	t
463	6	2026-02-19	t
464	6	2026-02-20	t
465	6	2026-02-21	t
466	6	2026-02-22	t
467	6	2026-02-23	t
468	6	2026-02-24	t
469	6	2026-02-25	f
470	6	2026-02-26	t
471	6	2026-02-27	t
472	6	2026-02-28	t
473	6	2026-03-01	t
474	6	2026-03-02	f
475	6	2026-03-03	t
476	6	2026-03-04	t
477	6	2026-03-05	t
478	6	2026-03-06	t
479	6	2026-03-07	f
480	6	2026-03-08	t
481	6	2026-03-09	t
482	6	2026-03-10	t
483	6	2026-03-11	f
484	6	2026-03-12	t
485	6	2026-03-13	t
486	6	2026-03-14	t
487	6	2026-03-15	t
488	6	2026-03-16	t
489	6	2026-03-17	t
490	6	2026-03-18	f
491	6	2026-03-19	f
492	6	2026-03-20	t
493	6	2026-03-21	t
494	6	2026-03-22	t
495	6	2026-03-23	f
496	6	2026-03-24	t
497	6	2026-03-25	t
498	6	2026-03-26	f
499	6	2026-03-27	f
500	6	2026-03-28	t
501	6	2026-03-29	t
502	6	2026-03-30	t
503	6	2026-03-31	t
504	6	2026-04-01	f
505	6	2026-04-02	f
506	6	2026-04-03	t
507	6	2026-04-04	t
508	6	2026-04-05	t
509	6	2026-04-06	t
510	6	2026-04-07	t
511	6	2026-04-08	t
512	6	2026-04-09	t
513	6	2026-04-10	t
514	6	2026-04-11	t
515	6	2026-04-12	t
516	6	2026-04-13	t
517	6	2026-04-14	f
518	6	2026-04-15	t
519	6	2026-04-16	t
520	6	2026-04-17	t
521	6	2026-04-18	t
522	6	2026-04-19	t
523	6	2026-04-20	t
524	6	2026-04-21	t
525	6	2026-04-22	t
526	6	2026-04-23	t
527	6	2026-04-24	f
528	6	2026-04-25	t
529	6	2026-04-26	t
530	6	2026-04-27	f
531	6	2026-04-28	t
532	6	2026-04-29	f
533	6	2026-04-30	f
534	6	2026-05-01	f
535	6	2026-05-02	t
536	6	2026-05-03	t
537	6	2026-05-04	t
538	6	2026-05-05	t
539	6	2026-05-06	f
540	6	2026-05-07	t
541	7	2026-02-07	t
542	7	2026-02-08	t
543	7	2026-02-09	f
544	7	2026-02-10	t
545	7	2026-02-11	t
546	7	2026-02-12	f
547	7	2026-02-13	t
548	7	2026-02-14	f
549	7	2026-02-15	f
550	7	2026-02-16	t
551	7	2026-02-17	f
552	7	2026-02-18	f
553	7	2026-02-19	t
554	7	2026-02-20	t
555	7	2026-02-21	t
556	7	2026-02-22	t
557	7	2026-02-23	t
558	7	2026-02-24	t
559	7	2026-02-25	t
560	7	2026-02-26	t
561	7	2026-02-27	t
562	7	2026-02-28	t
563	7	2026-03-01	t
564	7	2026-03-02	t
565	7	2026-03-03	f
566	7	2026-03-04	t
567	7	2026-03-05	t
568	7	2026-03-06	f
569	7	2026-03-07	t
570	7	2026-03-08	f
571	7	2026-03-09	t
572	7	2026-03-10	t
573	7	2026-03-11	t
574	7	2026-03-12	f
575	7	2026-03-13	t
576	7	2026-03-14	t
577	7	2026-03-15	t
578	7	2026-03-16	t
579	7	2026-03-17	t
580	7	2026-03-18	t
581	7	2026-03-19	f
582	7	2026-03-20	f
583	7	2026-03-21	t
584	7	2026-03-22	f
585	7	2026-03-23	t
586	7	2026-03-24	t
587	7	2026-03-25	t
588	7	2026-03-26	t
589	7	2026-03-27	f
590	7	2026-03-28	t
591	7	2026-03-29	t
592	7	2026-03-30	t
593	7	2026-03-31	t
594	7	2026-04-01	t
595	7	2026-04-02	t
596	7	2026-04-03	t
597	7	2026-04-04	t
598	7	2026-04-05	t
599	7	2026-04-06	t
600	7	2026-04-07	f
601	7	2026-04-08	t
602	7	2026-04-09	t
603	7	2026-04-10	t
604	7	2026-04-11	f
605	7	2026-04-12	t
606	7	2026-04-13	t
607	7	2026-04-14	t
608	7	2026-04-15	f
609	7	2026-04-16	f
610	7	2026-04-17	t
611	7	2026-04-18	f
612	7	2026-04-19	t
613	7	2026-04-20	t
614	7	2026-04-21	f
615	7	2026-04-22	f
616	7	2026-04-23	f
617	7	2026-04-24	f
618	7	2026-04-25	t
619	7	2026-04-26	t
620	7	2026-04-27	t
621	7	2026-04-28	t
622	7	2026-04-29	t
623	7	2026-04-30	t
624	7	2026-05-01	t
625	7	2026-05-02	t
626	7	2026-05-03	t
627	7	2026-05-04	t
628	7	2026-05-05	t
629	7	2026-05-06	f
630	7	2026-05-07	t
631	8	2026-02-07	t
632	8	2026-02-08	t
633	8	2026-02-09	t
634	8	2026-02-10	f
635	8	2026-02-11	t
636	8	2026-02-12	t
637	8	2026-02-13	f
638	8	2026-02-14	t
639	8	2026-02-15	t
640	8	2026-02-16	t
641	8	2026-02-17	f
642	8	2026-02-18	t
643	8	2026-02-19	t
644	8	2026-02-20	f
645	8	2026-02-21	t
646	8	2026-02-22	f
647	8	2026-02-23	t
648	8	2026-02-24	t
649	8	2026-02-25	f
650	8	2026-02-26	f
651	8	2026-02-27	f
652	8	2026-02-28	t
653	8	2026-03-01	t
654	8	2026-03-02	t
655	8	2026-03-03	f
656	8	2026-03-04	t
657	8	2026-03-05	t
658	8	2026-03-06	t
659	8	2026-03-07	t
660	8	2026-03-08	t
661	8	2026-03-09	f
662	8	2026-03-10	t
663	8	2026-03-11	t
664	8	2026-03-12	t
665	8	2026-03-13	t
666	8	2026-03-14	t
667	8	2026-03-15	f
668	8	2026-03-16	f
669	8	2026-03-17	t
670	8	2026-03-18	f
671	8	2026-03-19	t
672	8	2026-03-20	t
673	8	2026-03-21	t
674	8	2026-03-22	t
675	8	2026-03-23	t
676	8	2026-03-24	t
677	8	2026-03-25	t
678	8	2026-03-26	t
679	8	2026-03-27	t
680	8	2026-03-28	f
681	8	2026-03-29	t
682	8	2026-03-30	t
683	8	2026-03-31	t
684	8	2026-04-01	t
685	8	2026-04-02	f
686	8	2026-04-03	t
687	8	2026-04-04	t
688	8	2026-04-05	t
689	8	2026-04-06	t
690	8	2026-04-07	t
691	8	2026-04-08	t
692	8	2026-04-09	f
693	8	2026-04-10	f
694	8	2026-04-11	t
695	8	2026-04-12	t
696	8	2026-04-13	f
697	8	2026-04-14	f
698	8	2026-04-15	t
699	8	2026-04-16	t
700	8	2026-04-17	t
701	8	2026-04-18	f
702	8	2026-04-19	t
703	8	2026-04-20	f
704	8	2026-04-21	f
705	8	2026-04-22	t
706	8	2026-04-23	t
707	8	2026-04-24	f
708	8	2026-04-25	f
709	8	2026-04-26	t
710	8	2026-04-27	t
711	8	2026-04-28	t
712	8	2026-04-29	f
713	8	2026-04-30	t
714	8	2026-05-01	t
715	8	2026-05-02	t
716	8	2026-05-03	t
717	8	2026-05-04	t
718	8	2026-05-05	f
719	8	2026-05-06	t
720	8	2026-05-07	t
721	9	2026-02-07	t
722	9	2026-02-08	t
723	9	2026-02-09	t
724	9	2026-02-10	t
725	9	2026-02-11	f
726	9	2026-02-12	t
727	9	2026-02-13	t
728	9	2026-02-14	t
729	9	2026-02-15	f
730	9	2026-02-16	t
731	9	2026-02-17	t
732	9	2026-02-18	t
733	9	2026-02-19	t
734	9	2026-02-20	t
735	9	2026-02-21	t
736	9	2026-02-22	t
737	9	2026-02-23	t
738	9	2026-02-24	t
739	9	2026-02-25	f
740	9	2026-02-26	t
741	9	2026-02-27	t
742	9	2026-02-28	t
743	9	2026-03-01	t
744	9	2026-03-02	f
745	9	2026-03-03	t
746	9	2026-03-04	t
747	9	2026-03-05	t
748	9	2026-03-06	t
749	9	2026-03-07	t
750	9	2026-03-08	t
751	9	2026-03-09	t
752	9	2026-03-10	t
753	9	2026-03-11	t
754	9	2026-03-12	t
755	9	2026-03-13	t
756	9	2026-03-14	t
757	9	2026-03-15	t
758	9	2026-03-16	t
759	9	2026-03-17	f
760	9	2026-03-18	t
761	9	2026-03-19	f
762	9	2026-03-20	t
763	9	2026-03-21	t
764	9	2026-03-22	t
765	9	2026-03-23	f
766	9	2026-03-24	t
767	9	2026-03-25	t
768	9	2026-03-26	f
769	9	2026-03-27	t
770	9	2026-03-28	t
771	9	2026-03-29	f
772	9	2026-03-30	t
773	9	2026-03-31	f
774	9	2026-04-01	t
775	9	2026-04-02	t
776	9	2026-04-03	f
777	9	2026-04-04	t
778	9	2026-04-05	f
779	9	2026-04-06	t
780	9	2026-04-07	t
781	9	2026-04-08	f
782	9	2026-04-09	t
783	9	2026-04-10	t
784	9	2026-04-11	t
785	9	2026-04-12	f
786	9	2026-04-13	t
787	9	2026-04-14	f
788	9	2026-04-15	t
789	9	2026-04-16	f
790	9	2026-04-17	t
791	9	2026-04-18	f
792	9	2026-04-19	t
793	9	2026-04-20	f
794	9	2026-04-21	t
795	9	2026-04-22	f
796	9	2026-04-23	t
797	9	2026-04-24	t
798	9	2026-04-25	t
799	9	2026-04-26	t
800	9	2026-04-27	t
801	9	2026-04-28	f
802	9	2026-04-29	t
803	9	2026-04-30	t
804	9	2026-05-01	f
805	9	2026-05-02	t
806	9	2026-05-03	f
807	9	2026-05-04	t
808	9	2026-05-05	t
809	9	2026-05-06	f
810	9	2026-05-07	f
811	10	2026-02-07	f
812	10	2026-02-08	f
813	10	2026-02-09	t
814	10	2026-02-10	t
815	10	2026-02-11	t
816	10	2026-02-12	t
817	10	2026-02-13	f
818	10	2026-02-14	t
819	10	2026-02-15	t
820	10	2026-02-16	t
821	10	2026-02-17	t
822	10	2026-02-18	t
823	10	2026-02-19	t
824	10	2026-02-20	f
825	10	2026-02-21	f
826	10	2026-02-22	t
827	10	2026-02-23	t
828	10	2026-02-24	f
829	10	2026-02-25	f
830	10	2026-02-26	t
831	10	2026-02-27	f
832	10	2026-02-28	t
833	10	2026-03-01	t
834	10	2026-03-02	f
835	10	2026-03-03	f
836	10	2026-03-04	t
837	10	2026-03-05	t
838	10	2026-03-06	t
839	10	2026-03-07	f
840	10	2026-03-08	f
841	10	2026-03-09	t
842	10	2026-03-10	t
843	10	2026-03-11	t
844	10	2026-03-12	t
845	10	2026-03-13	t
846	10	2026-03-14	t
847	10	2026-03-15	t
848	10	2026-03-16	t
849	10	2026-03-17	f
850	10	2026-03-18	t
851	10	2026-03-19	t
852	10	2026-03-20	t
853	10	2026-03-21	t
854	10	2026-03-22	t
855	10	2026-03-23	f
856	10	2026-03-24	f
857	10	2026-03-25	t
858	10	2026-03-26	f
859	10	2026-03-27	f
860	10	2026-03-28	t
861	10	2026-03-29	t
862	10	2026-03-30	f
863	10	2026-03-31	t
864	10	2026-04-01	t
865	10	2026-04-02	t
866	10	2026-04-03	t
867	10	2026-04-04	t
868	10	2026-04-05	t
869	10	2026-04-06	t
870	10	2026-04-07	t
871	10	2026-04-08	f
872	10	2026-04-09	t
873	10	2026-04-10	f
874	10	2026-04-11	t
875	10	2026-04-12	t
876	10	2026-04-13	t
877	10	2026-04-14	f
878	10	2026-04-15	f
879	10	2026-04-16	t
880	10	2026-04-17	f
881	10	2026-04-18	t
882	10	2026-04-19	f
883	10	2026-04-20	t
884	10	2026-04-21	f
885	10	2026-04-22	f
886	10	2026-04-23	t
887	10	2026-04-24	f
888	10	2026-04-25	t
889	10	2026-04-26	t
890	10	2026-04-27	f
891	10	2026-04-28	f
892	10	2026-04-29	f
893	10	2026-04-30	t
894	10	2026-05-01	t
895	10	2026-05-02	f
896	10	2026-05-03	t
897	10	2026-05-04	t
898	10	2026-05-05	f
899	10	2026-05-06	t
900	10	2026-05-07	t
901	11	2026-02-07	t
902	11	2026-02-08	t
903	11	2026-02-09	f
904	11	2026-02-10	t
905	11	2026-02-11	t
906	11	2026-02-12	t
907	11	2026-02-13	t
908	11	2026-02-14	t
909	11	2026-02-15	t
910	11	2026-02-16	t
911	11	2026-02-17	f
912	11	2026-02-18	t
913	11	2026-02-19	f
914	11	2026-02-20	t
915	11	2026-02-21	t
916	11	2026-02-22	t
917	11	2026-02-23	f
918	11	2026-02-24	f
919	11	2026-02-25	t
920	11	2026-02-26	f
921	11	2026-02-27	f
922	11	2026-02-28	t
923	11	2026-03-01	t
924	11	2026-03-02	t
925	11	2026-03-03	t
926	11	2026-03-04	t
927	11	2026-03-05	t
928	11	2026-03-06	t
929	11	2026-03-07	f
930	11	2026-03-08	t
931	11	2026-03-09	f
932	11	2026-03-10	f
933	11	2026-03-11	t
934	11	2026-03-12	f
935	11	2026-03-13	t
936	11	2026-03-14	f
937	11	2026-03-15	t
938	11	2026-03-16	f
939	11	2026-03-17	t
940	11	2026-03-18	t
941	11	2026-03-19	f
942	11	2026-03-20	t
943	11	2026-03-21	t
944	11	2026-03-22	t
945	11	2026-03-23	t
946	11	2026-03-24	t
947	11	2026-03-25	t
948	11	2026-03-26	t
949	11	2026-03-27	t
950	11	2026-03-28	t
951	11	2026-03-29	f
952	11	2026-03-30	t
953	11	2026-03-31	t
954	11	2026-04-01	f
955	11	2026-04-02	t
956	11	2026-04-03	t
957	11	2026-04-04	t
958	11	2026-04-05	t
959	11	2026-04-06	t
960	11	2026-04-07	f
961	11	2026-04-08	t
962	11	2026-04-09	t
963	11	2026-04-10	t
964	11	2026-04-11	f
965	11	2026-04-12	t
966	11	2026-04-13	f
967	11	2026-04-14	t
968	11	2026-04-15	t
969	11	2026-04-16	t
970	11	2026-04-17	t
971	11	2026-04-18	t
972	11	2026-04-19	t
973	11	2026-04-20	t
974	11	2026-04-21	t
975	11	2026-04-22	t
976	11	2026-04-23	t
977	11	2026-04-24	t
978	11	2026-04-25	t
979	11	2026-04-26	t
980	11	2026-04-27	t
981	11	2026-04-28	t
982	11	2026-04-29	t
983	11	2026-04-30	f
984	11	2026-05-01	f
985	11	2026-05-02	t
986	11	2026-05-03	t
987	11	2026-05-04	f
988	11	2026-05-05	t
989	11	2026-05-06	f
990	11	2026-05-07	f
991	12	2026-02-07	t
992	12	2026-02-08	t
993	12	2026-02-09	t
994	12	2026-02-10	t
995	12	2026-02-11	t
996	12	2026-02-12	t
997	12	2026-02-13	f
998	12	2026-02-14	t
999	12	2026-02-15	t
1000	12	2026-02-16	t
1001	12	2026-02-17	t
1002	12	2026-02-18	t
1003	12	2026-02-19	t
1004	12	2026-02-20	t
1005	12	2026-02-21	t
1006	12	2026-02-22	t
1007	12	2026-02-23	f
1008	12	2026-02-24	t
1009	12	2026-02-25	f
1010	12	2026-02-26	t
1011	12	2026-02-27	f
1012	12	2026-02-28	t
1013	12	2026-03-01	t
1014	12	2026-03-02	t
1015	12	2026-03-03	t
1016	12	2026-03-04	t
1017	12	2026-03-05	f
1018	12	2026-03-06	f
1019	12	2026-03-07	t
1020	12	2026-03-08	t
1021	12	2026-03-09	t
1022	12	2026-03-10	t
1023	12	2026-03-11	f
1024	12	2026-03-12	t
1025	12	2026-03-13	t
1026	12	2026-03-14	f
1027	12	2026-03-15	f
1028	12	2026-03-16	t
1029	12	2026-03-17	t
1030	12	2026-03-18	t
1031	12	2026-03-19	t
1032	12	2026-03-20	t
1033	12	2026-03-21	t
1034	12	2026-03-22	t
1035	12	2026-03-23	t
1036	12	2026-03-24	t
1037	12	2026-03-25	t
1038	12	2026-03-26	t
1039	12	2026-03-27	t
1040	12	2026-03-28	t
1041	12	2026-03-29	f
1042	12	2026-03-30	f
1043	12	2026-03-31	t
1044	12	2026-04-01	t
1045	12	2026-04-02	t
1046	12	2026-04-03	t
1047	12	2026-04-04	t
1048	12	2026-04-05	t
1049	12	2026-04-06	t
1050	12	2026-04-07	t
1051	12	2026-04-08	f
1052	12	2026-04-09	t
1053	12	2026-04-10	t
1054	12	2026-04-11	t
1055	12	2026-04-12	t
1056	12	2026-04-13	t
1057	12	2026-04-14	f
1058	12	2026-04-15	t
1059	12	2026-04-16	t
1060	12	2026-04-17	t
1061	12	2026-04-18	f
1062	12	2026-04-19	f
1063	12	2026-04-20	f
1064	12	2026-04-21	t
1065	12	2026-04-22	t
1066	12	2026-04-23	f
1067	12	2026-04-24	t
1068	12	2026-04-25	t
1069	12	2026-04-26	t
1070	12	2026-04-27	t
1071	12	2026-04-28	t
1072	12	2026-04-29	f
1073	12	2026-04-30	t
1074	12	2026-05-01	t
1075	12	2026-05-02	t
1076	12	2026-05-03	t
1077	12	2026-05-04	f
1078	12	2026-05-05	t
1079	12	2026-05-06	t
1080	12	2026-05-07	t
1081	13	2026-02-07	t
1082	13	2026-02-08	t
1083	13	2026-02-09	t
1084	13	2026-02-10	t
1085	13	2026-02-11	f
1086	13	2026-02-12	f
1087	13	2026-02-13	t
1088	13	2026-02-14	f
1089	13	2026-02-15	f
1090	13	2026-02-16	t
1091	13	2026-02-17	f
1092	13	2026-02-18	t
1093	13	2026-02-19	f
1094	13	2026-02-20	t
1095	13	2026-02-21	t
1096	13	2026-02-22	t
1097	13	2026-02-23	t
1098	13	2026-02-24	t
1099	13	2026-02-25	f
1100	13	2026-02-26	t
1101	13	2026-02-27	t
1102	13	2026-02-28	t
1103	13	2026-03-01	t
1104	13	2026-03-02	t
1105	13	2026-03-03	f
1106	13	2026-03-04	t
1107	13	2026-03-05	t
1108	13	2026-03-06	f
1109	13	2026-03-07	t
1110	13	2026-03-08	t
1111	13	2026-03-09	t
1112	13	2026-03-10	t
1113	13	2026-03-11	f
1114	13	2026-03-12	t
1115	13	2026-03-13	t
1116	13	2026-03-14	t
1117	13	2026-03-15	t
1118	13	2026-03-16	t
1119	13	2026-03-17	t
1120	13	2026-03-18	f
1121	13	2026-03-19	f
1122	13	2026-03-20	f
1123	13	2026-03-21	t
1124	13	2026-03-22	t
1125	13	2026-03-23	t
1126	13	2026-03-24	t
1127	13	2026-03-25	t
1128	13	2026-03-26	t
1129	13	2026-03-27	f
1130	13	2026-03-28	f
1131	13	2026-03-29	t
1132	13	2026-03-30	f
1133	13	2026-03-31	t
1134	13	2026-04-01	t
1135	13	2026-04-02	t
1136	13	2026-04-03	t
1137	13	2026-04-04	t
1138	13	2026-04-05	t
1139	13	2026-04-06	f
1140	13	2026-04-07	t
1141	13	2026-04-08	t
1142	13	2026-04-09	t
1143	13	2026-04-10	t
1144	13	2026-04-11	t
1145	13	2026-04-12	f
1146	13	2026-04-13	f
1147	13	2026-04-14	t
1148	13	2026-04-15	f
1149	13	2026-04-16	t
1150	13	2026-04-17	f
1151	13	2026-04-18	t
1152	13	2026-04-19	t
1153	13	2026-04-20	f
1154	13	2026-04-21	f
1155	13	2026-04-22	t
1156	13	2026-04-23	t
1157	13	2026-04-24	t
1158	13	2026-04-25	t
1159	13	2026-04-26	f
1160	13	2026-04-27	t
1161	13	2026-04-28	t
1162	13	2026-04-29	t
1163	13	2026-04-30	f
1164	13	2026-05-01	f
1165	13	2026-05-02	t
1166	13	2026-05-03	f
1167	13	2026-05-04	f
1168	13	2026-05-05	f
1169	13	2026-05-06	t
1170	13	2026-05-07	t
1171	14	2026-02-07	t
1172	14	2026-02-08	t
1173	14	2026-02-09	t
1174	14	2026-02-10	t
1175	14	2026-02-11	t
1176	14	2026-02-12	t
1177	14	2026-02-13	f
1178	14	2026-02-14	f
1179	14	2026-02-15	t
1180	14	2026-02-16	t
1181	14	2026-02-17	f
1182	14	2026-02-18	t
1183	14	2026-02-19	t
1184	14	2026-02-20	t
1185	14	2026-02-21	t
1186	14	2026-02-22	f
1187	14	2026-02-23	t
1188	14	2026-02-24	t
1189	14	2026-02-25	t
1190	14	2026-02-26	t
1191	14	2026-02-27	t
1192	14	2026-02-28	f
1193	14	2026-03-01	t
1194	14	2026-03-02	t
1195	14	2026-03-03	t
1196	14	2026-03-04	f
1197	14	2026-03-05	t
1198	14	2026-03-06	t
1199	14	2026-03-07	t
1200	14	2026-03-08	t
1201	14	2026-03-09	t
1202	14	2026-03-10	t
1203	14	2026-03-11	f
1204	14	2026-03-12	f
1205	14	2026-03-13	t
1206	14	2026-03-14	t
1207	14	2026-03-15	t
1208	14	2026-03-16	t
1209	14	2026-03-17	t
1210	14	2026-03-18	t
1211	14	2026-03-19	t
1212	14	2026-03-20	t
1213	14	2026-03-21	f
1214	14	2026-03-22	t
1215	14	2026-03-23	t
1216	14	2026-03-24	t
1217	14	2026-03-25	t
1218	14	2026-03-26	t
1219	14	2026-03-27	t
1220	14	2026-03-28	t
1221	14	2026-03-29	t
1222	14	2026-03-30	t
1223	14	2026-03-31	f
1224	14	2026-04-01	t
1225	14	2026-04-02	t
1226	14	2026-04-03	t
1227	14	2026-04-04	t
1228	14	2026-04-05	t
1229	14	2026-04-06	f
1230	14	2026-04-07	t
1231	14	2026-04-08	t
1232	14	2026-04-09	t
1233	14	2026-04-10	t
1234	14	2026-04-11	t
1235	14	2026-04-12	t
1236	14	2026-04-13	t
1237	14	2026-04-14	f
1238	14	2026-04-15	t
1239	14	2026-04-16	t
1240	14	2026-04-17	t
1241	14	2026-04-18	t
1242	14	2026-04-19	t
1243	14	2026-04-20	t
1244	14	2026-04-21	t
1245	14	2026-04-22	t
1246	14	2026-04-23	t
1247	14	2026-04-24	t
1248	14	2026-04-25	t
1249	14	2026-04-26	t
1250	14	2026-04-27	f
1251	14	2026-04-28	t
1252	14	2026-04-29	t
1253	14	2026-04-30	t
1254	14	2026-05-01	t
1255	14	2026-05-02	t
1256	14	2026-05-03	t
1257	14	2026-05-04	t
1258	14	2026-05-05	t
1259	14	2026-05-06	t
1260	14	2026-05-07	f
1261	15	2026-02-07	t
1262	15	2026-02-08	t
1263	15	2026-02-09	t
1264	15	2026-02-10	t
1265	15	2026-02-11	t
1266	15	2026-02-12	t
1267	15	2026-02-13	t
1268	15	2026-02-14	t
1269	15	2026-02-15	t
1270	15	2026-02-16	t
1271	15	2026-02-17	t
1272	15	2026-02-18	t
1273	15	2026-02-19	f
1274	15	2026-02-20	f
1275	15	2026-02-21	f
1276	15	2026-02-22	t
1277	15	2026-02-23	f
1278	15	2026-02-24	t
1279	15	2026-02-25	t
1280	15	2026-02-26	t
1281	15	2026-02-27	t
1282	15	2026-02-28	t
1283	15	2026-03-01	t
1284	15	2026-03-02	t
1285	15	2026-03-03	f
1286	15	2026-03-04	t
1287	15	2026-03-05	t
1288	15	2026-03-06	t
1289	15	2026-03-07	t
1290	15	2026-03-08	f
1291	15	2026-03-09	t
1292	15	2026-03-10	t
1293	15	2026-03-11	t
1294	15	2026-03-12	t
1295	15	2026-03-13	t
1296	15	2026-03-14	f
1297	15	2026-03-15	t
1298	15	2026-03-16	t
1299	15	2026-03-17	t
1300	15	2026-03-18	f
1301	15	2026-03-19	f
1302	15	2026-03-20	f
1303	15	2026-03-21	t
1304	15	2026-03-22	t
1305	15	2026-03-23	t
1306	15	2026-03-24	t
1307	15	2026-03-25	t
1308	15	2026-03-26	t
1309	15	2026-03-27	f
1310	15	2026-03-28	t
1311	15	2026-03-29	t
1312	15	2026-03-30	f
1313	15	2026-03-31	f
1314	15	2026-04-01	f
1315	15	2026-04-02	f
1316	15	2026-04-03	f
1317	15	2026-04-04	f
1318	15	2026-04-05	t
1319	15	2026-04-06	t
1320	15	2026-04-07	t
1321	15	2026-04-08	t
1322	15	2026-04-09	f
1323	15	2026-04-10	t
1324	15	2026-04-11	f
1325	15	2026-04-12	t
1326	15	2026-04-13	f
1327	15	2026-04-14	t
1328	15	2026-04-15	t
1329	15	2026-04-16	t
1330	15	2026-04-17	f
1331	15	2026-04-18	t
1332	15	2026-04-19	t
1333	15	2026-04-20	f
1334	15	2026-04-21	f
1335	15	2026-04-22	t
1336	15	2026-04-23	f
1337	15	2026-04-24	f
1338	15	2026-04-25	t
1339	15	2026-04-26	t
1340	15	2026-04-27	t
1341	15	2026-04-28	t
1342	15	2026-04-29	t
1343	15	2026-04-30	f
1344	15	2026-05-01	t
1345	15	2026-05-02	t
1346	15	2026-05-03	t
1347	15	2026-05-04	f
1348	15	2026-05-05	f
1349	15	2026-05-06	t
1350	15	2026-05-07	t
1351	16	2026-02-07	t
1352	16	2026-02-08	t
1353	16	2026-02-09	f
1354	16	2026-02-10	t
1355	16	2026-02-11	f
1356	16	2026-02-12	t
1357	16	2026-02-13	t
1358	16	2026-02-14	t
1359	16	2026-02-15	t
1360	16	2026-02-16	t
1361	16	2026-02-17	f
1362	16	2026-02-18	t
1363	16	2026-02-19	t
1364	16	2026-02-20	t
1365	16	2026-02-21	f
1366	16	2026-02-22	f
1367	16	2026-02-23	t
1368	16	2026-02-24	t
1369	16	2026-02-25	f
1370	16	2026-02-26	f
1371	16	2026-02-27	t
1372	16	2026-02-28	t
1373	16	2026-03-01	t
1374	16	2026-03-02	f
1375	16	2026-03-03	t
1376	16	2026-03-04	t
1377	16	2026-03-05	t
1378	16	2026-03-06	t
1379	16	2026-03-07	f
1380	16	2026-03-08	f
1381	16	2026-03-09	t
1382	16	2026-03-10	f
1383	16	2026-03-11	t
1384	16	2026-03-12	t
1385	16	2026-03-13	f
1386	16	2026-03-14	t
1387	16	2026-03-15	t
1388	16	2026-03-16	f
1389	16	2026-03-17	f
1390	16	2026-03-18	f
1391	16	2026-03-19	t
1392	16	2026-03-20	t
1393	16	2026-03-21	f
1394	16	2026-03-22	t
1395	16	2026-03-23	t
1396	16	2026-03-24	t
1397	16	2026-03-25	t
1398	16	2026-03-26	f
1399	16	2026-03-27	t
1400	16	2026-03-28	f
1401	16	2026-03-29	f
1402	16	2026-03-30	t
1403	16	2026-03-31	t
1404	16	2026-04-01	t
1405	16	2026-04-02	t
1406	16	2026-04-03	t
1407	16	2026-04-04	t
1408	16	2026-04-05	t
1409	16	2026-04-06	t
1410	16	2026-04-07	t
1411	16	2026-04-08	t
1412	16	2026-04-09	t
1413	16	2026-04-10	t
1414	16	2026-04-11	f
1415	16	2026-04-12	t
1416	16	2026-04-13	f
1417	16	2026-04-14	f
1418	16	2026-04-15	f
1419	16	2026-04-16	f
1420	16	2026-04-17	t
1421	16	2026-04-18	t
1422	16	2026-04-19	t
1423	16	2026-04-20	t
1424	16	2026-04-21	t
1425	16	2026-04-22	t
1426	16	2026-04-23	f
1427	16	2026-04-24	t
1428	16	2026-04-25	t
1429	16	2026-04-26	f
1430	16	2026-04-27	t
1431	16	2026-04-28	f
1432	16	2026-04-29	t
1433	16	2026-04-30	t
1434	16	2026-05-01	f
1435	16	2026-05-02	t
1436	16	2026-05-03	t
1437	16	2026-05-04	t
1438	16	2026-05-05	f
1439	16	2026-05-06	t
1440	16	2026-05-07	f
1441	17	2026-02-07	t
1442	17	2026-02-08	t
1443	17	2026-02-09	t
1444	17	2026-02-10	t
1445	17	2026-02-11	t
1446	17	2026-02-12	t
1447	17	2026-02-13	t
1448	17	2026-02-14	f
1449	17	2026-02-15	f
1450	17	2026-02-16	t
1451	17	2026-02-17	t
1452	17	2026-02-18	t
1453	17	2026-02-19	t
1454	17	2026-02-20	t
1455	17	2026-02-21	t
1456	17	2026-02-22	t
1457	17	2026-02-23	t
1458	17	2026-02-24	t
1459	17	2026-02-25	t
1460	17	2026-02-26	f
1461	17	2026-02-27	t
1462	17	2026-02-28	t
1463	17	2026-03-01	t
1464	17	2026-03-02	f
1465	17	2026-03-03	t
1466	17	2026-03-04	t
1467	17	2026-03-05	t
1468	17	2026-03-06	t
1469	17	2026-03-07	t
1470	17	2026-03-08	t
1471	17	2026-03-09	t
1472	17	2026-03-10	t
1473	17	2026-03-11	f
1474	17	2026-03-12	t
1475	17	2026-03-13	t
1476	17	2026-03-14	t
1477	17	2026-03-15	f
1478	17	2026-03-16	t
1479	17	2026-03-17	t
1480	17	2026-03-18	t
1481	17	2026-03-19	t
1482	17	2026-03-20	t
1483	17	2026-03-21	f
1484	17	2026-03-22	t
1485	17	2026-03-23	t
1486	17	2026-03-24	f
1487	17	2026-03-25	t
1488	17	2026-03-26	t
1489	17	2026-03-27	t
1490	17	2026-03-28	t
1491	17	2026-03-29	t
1492	17	2026-03-30	t
1493	17	2026-03-31	f
1494	17	2026-04-01	t
1495	17	2026-04-02	t
1496	17	2026-04-03	t
1497	17	2026-04-04	t
1498	17	2026-04-05	f
1499	17	2026-04-06	t
1500	17	2026-04-07	t
1501	17	2026-04-08	f
1502	17	2026-04-09	t
1503	17	2026-04-10	t
1504	17	2026-04-11	t
1505	17	2026-04-12	t
1506	17	2026-04-13	t
1507	17	2026-04-14	t
1508	17	2026-04-15	f
1509	17	2026-04-16	t
1510	17	2026-04-17	t
1511	17	2026-04-18	t
1512	17	2026-04-19	t
1513	17	2026-04-20	f
1514	17	2026-04-21	t
1515	17	2026-04-22	t
1516	17	2026-04-23	t
1517	17	2026-04-24	t
1518	17	2026-04-25	f
1519	17	2026-04-26	f
1520	17	2026-04-27	t
1521	17	2026-04-28	f
1522	17	2026-04-29	f
1523	17	2026-04-30	t
1524	17	2026-05-01	t
1525	17	2026-05-02	t
1526	17	2026-05-03	t
1527	17	2026-05-04	t
1528	17	2026-05-05	t
1529	17	2026-05-06	f
1530	17	2026-05-07	t
1531	18	2026-02-07	t
1532	18	2026-02-08	t
1533	18	2026-02-09	t
1534	18	2026-02-10	t
1535	18	2026-02-11	f
1536	18	2026-02-12	t
1537	18	2026-02-13	f
1538	18	2026-02-14	f
1539	18	2026-02-15	t
1540	18	2026-02-16	t
1541	18	2026-02-17	t
1542	18	2026-02-18	t
1543	18	2026-02-19	t
1544	18	2026-02-20	f
1545	18	2026-02-21	t
1546	18	2026-02-22	f
1547	18	2026-02-23	f
1548	18	2026-02-24	t
1549	18	2026-02-25	t
1550	18	2026-02-26	f
1551	18	2026-02-27	f
1552	18	2026-02-28	t
1553	18	2026-03-01	f
1554	18	2026-03-02	t
1555	18	2026-03-03	t
1556	18	2026-03-04	t
1557	18	2026-03-05	t
1558	18	2026-03-06	t
1559	18	2026-03-07	t
1560	18	2026-03-08	t
1561	18	2026-03-09	t
1562	18	2026-03-10	t
1563	18	2026-03-11	t
1564	18	2026-03-12	t
1565	18	2026-03-13	f
1566	18	2026-03-14	t
1567	18	2026-03-15	t
1568	18	2026-03-16	t
1569	18	2026-03-17	f
1570	18	2026-03-18	t
1571	18	2026-03-19	f
1572	18	2026-03-20	t
1573	18	2026-03-21	t
1574	18	2026-03-22	f
1575	18	2026-03-23	t
1576	18	2026-03-24	t
1577	18	2026-03-25	t
1578	18	2026-03-26	t
1579	18	2026-03-27	t
1580	18	2026-03-28	t
1581	18	2026-03-29	t
1582	18	2026-03-30	t
1583	18	2026-03-31	f
1584	18	2026-04-01	t
1585	18	2026-04-02	t
1586	18	2026-04-03	f
1587	18	2026-04-04	f
1588	18	2026-04-05	t
1589	18	2026-04-06	t
1590	18	2026-04-07	t
1591	18	2026-04-08	t
1592	18	2026-04-09	t
1593	18	2026-04-10	t
1594	18	2026-04-11	f
1595	18	2026-04-12	t
1596	18	2026-04-13	t
1597	18	2026-04-14	t
1598	18	2026-04-15	t
1599	18	2026-04-16	t
1600	18	2026-04-17	f
1601	18	2026-04-18	t
1602	18	2026-04-19	t
1603	18	2026-04-20	t
1604	18	2026-04-21	t
1605	18	2026-04-22	f
1606	18	2026-04-23	t
1607	18	2026-04-24	t
1608	18	2026-04-25	f
1609	18	2026-04-26	t
1610	18	2026-04-27	f
1611	18	2026-04-28	f
1612	18	2026-04-29	t
1613	18	2026-04-30	t
1614	18	2026-05-01	t
1615	18	2026-05-02	t
1616	18	2026-05-03	f
1617	18	2026-05-04	t
1618	18	2026-05-05	t
1619	18	2026-05-06	t
1620	18	2026-05-07	f
1621	19	2026-02-07	f
1622	19	2026-02-08	t
1623	19	2026-02-09	t
1624	19	2026-02-10	t
1625	19	2026-02-11	t
1626	19	2026-02-12	t
1627	19	2026-02-13	f
1628	19	2026-02-14	t
1629	19	2026-02-15	t
1630	19	2026-02-16	t
1631	19	2026-02-17	t
1632	19	2026-02-18	t
1633	19	2026-02-19	t
1634	19	2026-02-20	f
1635	19	2026-02-21	f
1636	19	2026-02-22	t
1637	19	2026-02-23	f
1638	19	2026-02-24	t
1639	19	2026-02-25	t
1640	19	2026-02-26	t
1641	19	2026-02-27	t
1642	19	2026-02-28	t
1643	19	2026-03-01	t
1644	19	2026-03-02	f
1645	19	2026-03-03	t
1646	19	2026-03-04	t
1647	19	2026-03-05	t
1648	19	2026-03-06	t
1649	19	2026-03-07	f
1650	19	2026-03-08	f
1651	19	2026-03-09	f
1652	19	2026-03-10	t
1653	19	2026-03-11	t
1654	19	2026-03-12	t
1655	19	2026-03-13	t
1656	19	2026-03-14	f
1657	19	2026-03-15	f
1658	19	2026-03-16	t
1659	19	2026-03-17	t
1660	19	2026-03-18	t
1661	19	2026-03-19	t
1662	19	2026-03-20	t
1663	19	2026-03-21	f
1664	19	2026-03-22	t
1665	19	2026-03-23	t
1666	19	2026-03-24	t
1667	19	2026-03-25	t
1668	19	2026-03-26	t
1669	19	2026-03-27	t
1670	19	2026-03-28	t
1671	19	2026-03-29	t
1672	19	2026-03-30	t
1673	19	2026-03-31	f
1674	19	2026-04-01	t
1675	19	2026-04-02	t
1676	19	2026-04-03	t
1677	19	2026-04-04	t
1678	19	2026-04-05	f
1679	19	2026-04-06	f
1680	19	2026-04-07	t
1681	19	2026-04-08	f
1682	19	2026-04-09	f
1683	19	2026-04-10	t
1684	19	2026-04-11	t
1685	19	2026-04-12	t
1686	19	2026-04-13	t
1687	19	2026-04-14	t
1688	19	2026-04-15	f
1689	19	2026-04-16	t
1690	19	2026-04-17	f
1691	19	2026-04-18	t
1692	19	2026-04-19	t
1693	19	2026-04-20	t
1694	19	2026-04-21	t
1695	19	2026-04-22	t
1696	19	2026-04-23	f
1697	19	2026-04-24	t
1698	19	2026-04-25	t
1699	19	2026-04-26	t
1700	19	2026-04-27	t
1701	19	2026-04-28	t
1702	19	2026-04-29	t
1703	19	2026-04-30	t
1704	19	2026-05-01	f
1705	19	2026-05-02	t
1706	19	2026-05-03	t
1707	19	2026-05-04	t
1708	19	2026-05-05	t
1709	19	2026-05-06	t
1710	19	2026-05-07	t
1711	20	2026-02-07	t
1712	20	2026-02-08	t
1713	20	2026-02-09	t
1714	20	2026-02-10	t
1715	20	2026-02-11	f
1716	20	2026-02-12	t
1717	20	2026-02-13	t
1718	20	2026-02-14	t
1719	20	2026-02-15	f
1720	20	2026-02-16	t
1721	20	2026-02-17	t
1722	20	2026-02-18	t
1723	20	2026-02-19	t
1724	20	2026-02-20	t
1725	20	2026-02-21	f
1726	20	2026-02-22	f
1727	20	2026-02-23	t
1728	20	2026-02-24	t
1729	20	2026-02-25	f
1730	20	2026-02-26	t
1731	20	2026-02-27	t
1732	20	2026-02-28	t
1733	20	2026-03-01	f
1734	20	2026-03-02	t
1735	20	2026-03-03	f
1736	20	2026-03-04	t
1737	20	2026-03-05	f
1738	20	2026-03-06	f
1739	20	2026-03-07	t
1740	20	2026-03-08	t
1741	20	2026-03-09	f
1742	20	2026-03-10	t
1743	20	2026-03-11	t
1744	20	2026-03-12	t
1745	20	2026-03-13	t
1746	20	2026-03-14	t
1747	20	2026-03-15	t
1748	20	2026-03-16	t
1749	20	2026-03-17	f
1750	20	2026-03-18	t
1751	20	2026-03-19	t
1752	20	2026-03-20	t
1753	20	2026-03-21	t
1754	20	2026-03-22	t
1755	20	2026-03-23	t
1756	20	2026-03-24	t
1757	20	2026-03-25	t
1758	20	2026-03-26	t
1759	20	2026-03-27	t
1760	20	2026-03-28	t
1761	20	2026-03-29	f
1762	20	2026-03-30	t
1763	20	2026-03-31	t
1764	20	2026-04-01	t
1765	20	2026-04-02	t
1766	20	2026-04-03	t
1767	20	2026-04-04	t
1768	20	2026-04-05	t
1769	20	2026-04-06	t
1770	20	2026-04-07	t
1771	20	2026-04-08	t
1772	20	2026-04-09	t
1773	20	2026-04-10	f
1774	20	2026-04-11	f
1775	20	2026-04-12	t
1776	20	2026-04-13	f
1777	20	2026-04-14	t
1778	20	2026-04-15	t
1779	20	2026-04-16	t
1780	20	2026-04-17	t
1781	20	2026-04-18	f
1782	20	2026-04-19	f
1783	20	2026-04-20	t
1784	20	2026-04-21	t
1785	20	2026-04-22	f
1786	20	2026-04-23	t
1787	20	2026-04-24	f
1788	20	2026-04-25	t
1789	20	2026-04-26	t
1790	20	2026-04-27	t
1791	20	2026-04-28	f
1792	20	2026-04-29	t
1793	20	2026-04-30	t
1794	20	2026-05-01	t
1795	20	2026-05-02	t
1796	20	2026-05-03	t
1797	20	2026-05-04	t
1798	20	2026-05-05	t
1799	20	2026-05-06	f
1800	20	2026-05-07	f
1801	21	2026-02-07	t
1802	21	2026-02-08	t
1803	21	2026-02-09	t
1804	21	2026-02-10	t
1805	21	2026-02-11	t
1806	21	2026-02-12	t
1807	21	2026-02-13	t
1808	21	2026-02-14	f
1809	21	2026-02-15	f
1810	21	2026-02-16	t
1811	21	2026-02-17	t
1812	21	2026-02-18	f
1813	21	2026-02-19	t
1814	21	2026-02-20	t
1815	21	2026-02-21	t
1816	21	2026-02-22	t
1817	21	2026-02-23	f
1818	21	2026-02-24	t
1819	21	2026-02-25	t
1820	21	2026-02-26	t
1821	21	2026-02-27	f
1822	21	2026-02-28	t
1823	21	2026-03-01	t
1824	21	2026-03-02	f
1825	21	2026-03-03	t
1826	21	2026-03-04	f
1827	21	2026-03-05	f
1828	21	2026-03-06	f
1829	21	2026-03-07	t
1830	21	2026-03-08	t
1831	21	2026-03-09	t
1832	21	2026-03-10	t
1833	21	2026-03-11	t
1834	21	2026-03-12	t
1835	21	2026-03-13	f
1836	21	2026-03-14	t
1837	21	2026-03-15	t
1838	21	2026-03-16	t
1839	21	2026-03-17	t
1840	21	2026-03-18	t
1841	21	2026-03-19	t
1842	21	2026-03-20	t
1843	21	2026-03-21	t
1844	21	2026-03-22	t
1845	21	2026-03-23	t
1846	21	2026-03-24	t
1847	21	2026-03-25	t
1848	21	2026-03-26	t
1849	21	2026-03-27	t
1850	21	2026-03-28	f
1851	21	2026-03-29	t
1852	21	2026-03-30	t
1853	21	2026-03-31	t
1854	21	2026-04-01	t
1855	21	2026-04-02	t
1856	21	2026-04-03	t
1857	21	2026-04-04	t
1858	21	2026-04-05	t
1859	21	2026-04-06	t
1860	21	2026-04-07	f
1861	21	2026-04-08	t
1862	21	2026-04-09	t
1863	21	2026-04-10	t
1864	21	2026-04-11	f
1865	21	2026-04-12	f
1866	21	2026-04-13	t
1867	21	2026-04-14	t
1868	21	2026-04-15	t
1869	21	2026-04-16	t
1870	21	2026-04-17	t
1871	21	2026-04-18	t
1872	21	2026-04-19	f
1873	21	2026-04-20	t
1874	21	2026-04-21	t
1875	21	2026-04-22	f
1876	21	2026-04-23	t
1877	21	2026-04-24	t
1878	21	2026-04-25	t
1879	21	2026-04-26	t
1880	21	2026-04-27	t
1881	21	2026-04-28	f
1882	21	2026-04-29	f
1883	21	2026-04-30	f
1884	21	2026-05-01	t
1885	21	2026-05-02	t
1886	21	2026-05-03	t
1887	21	2026-05-04	t
1888	21	2026-05-05	t
1889	21	2026-05-06	t
1890	21	2026-05-07	t
1891	22	2026-02-07	t
1892	22	2026-02-08	t
1893	22	2026-02-09	f
1894	22	2026-02-10	t
1895	22	2026-02-11	t
1896	22	2026-02-12	t
1897	22	2026-02-13	t
1898	22	2026-02-14	t
1899	22	2026-02-15	t
1900	22	2026-02-16	t
1901	22	2026-02-17	t
1902	22	2026-02-18	t
1903	22	2026-02-19	t
1904	22	2026-02-20	t
1905	22	2026-02-21	t
1906	22	2026-02-22	f
1907	22	2026-02-23	f
1908	22	2026-02-24	t
1909	22	2026-02-25	t
1910	22	2026-02-26	t
1911	22	2026-02-27	t
1912	22	2026-02-28	t
1913	22	2026-03-01	f
1914	22	2026-03-02	f
1915	22	2026-03-03	t
1916	22	2026-03-04	t
1917	22	2026-03-05	t
1918	22	2026-03-06	f
1919	22	2026-03-07	t
1920	22	2026-03-08	t
1921	22	2026-03-09	t
1922	22	2026-03-10	t
1923	22	2026-03-11	t
1924	22	2026-03-12	t
1925	22	2026-03-13	f
1926	22	2026-03-14	t
1927	22	2026-03-15	f
1928	22	2026-03-16	t
1929	22	2026-03-17	t
1930	22	2026-03-18	f
1931	22	2026-03-19	t
1932	22	2026-03-20	t
1933	22	2026-03-21	t
1934	22	2026-03-22	t
1935	22	2026-03-23	f
1936	22	2026-03-24	t
1937	22	2026-03-25	f
1938	22	2026-03-26	t
1939	22	2026-03-27	t
1940	22	2026-03-28	t
1941	22	2026-03-29	f
1942	22	2026-03-30	t
1943	22	2026-03-31	t
1944	22	2026-04-01	t
1945	22	2026-04-02	t
1946	22	2026-04-03	t
1947	22	2026-04-04	t
1948	22	2026-04-05	t
1949	22	2026-04-06	t
1950	22	2026-04-07	t
1951	22	2026-04-08	t
1952	22	2026-04-09	t
1953	22	2026-04-10	t
1954	22	2026-04-11	t
1955	22	2026-04-12	t
1956	22	2026-04-13	t
1957	22	2026-04-14	f
1958	22	2026-04-15	f
1959	22	2026-04-16	t
1960	22	2026-04-17	t
1961	22	2026-04-18	t
1962	22	2026-04-19	t
1963	22	2026-04-20	t
1964	22	2026-04-21	f
1965	22	2026-04-22	t
1966	22	2026-04-23	t
1967	22	2026-04-24	t
1968	22	2026-04-25	t
1969	22	2026-04-26	t
1970	22	2026-04-27	t
1971	22	2026-04-28	t
1972	22	2026-04-29	t
1973	22	2026-04-30	t
1974	22	2026-05-01	f
1975	22	2026-05-02	t
1976	22	2026-05-03	t
1977	22	2026-05-04	t
1978	22	2026-05-05	f
1979	22	2026-05-06	t
1980	22	2026-05-07	t
1981	23	2026-02-07	t
1982	23	2026-02-08	f
1983	23	2026-02-09	f
1984	23	2026-02-10	t
1985	23	2026-02-11	t
1986	23	2026-02-12	t
1987	23	2026-02-13	t
1988	23	2026-02-14	f
1989	23	2026-02-15	t
1990	23	2026-02-16	t
1991	23	2026-02-17	f
1992	23	2026-02-18	f
1993	23	2026-02-19	t
1994	23	2026-02-20	t
1995	23	2026-02-21	t
1996	23	2026-02-22	t
1997	23	2026-02-23	t
1998	23	2026-02-24	t
1999	23	2026-02-25	f
2000	23	2026-02-26	t
2001	23	2026-02-27	t
2002	23	2026-02-28	t
2003	23	2026-03-01	f
2004	23	2026-03-02	f
2005	23	2026-03-03	f
2006	23	2026-03-04	t
2007	23	2026-03-05	f
2008	23	2026-03-06	t
2009	23	2026-03-07	t
2010	23	2026-03-08	t
2011	23	2026-03-09	t
2012	23	2026-03-10	t
2013	23	2026-03-11	f
2014	23	2026-03-12	t
2015	23	2026-03-13	f
2016	23	2026-03-14	t
2017	23	2026-03-15	f
2018	23	2026-03-16	f
2019	23	2026-03-17	t
2020	23	2026-03-18	t
2021	23	2026-03-19	t
2022	23	2026-03-20	f
2023	23	2026-03-21	t
2024	23	2026-03-22	t
2025	23	2026-03-23	t
2026	23	2026-03-24	t
2027	23	2026-03-25	t
2028	23	2026-03-26	t
2029	23	2026-03-27	t
2030	23	2026-03-28	t
2031	23	2026-03-29	f
2032	23	2026-03-30	t
2033	23	2026-03-31	t
2034	23	2026-04-01	t
2035	23	2026-04-02	t
2036	23	2026-04-03	t
2037	23	2026-04-04	f
2038	23	2026-04-05	t
2039	23	2026-04-06	t
2040	23	2026-04-07	t
2041	23	2026-04-08	t
2042	23	2026-04-09	t
2043	23	2026-04-10	f
2044	23	2026-04-11	f
2045	23	2026-04-12	t
2046	23	2026-04-13	t
2047	23	2026-04-14	t
2048	23	2026-04-15	f
2049	23	2026-04-16	f
2050	23	2026-04-17	f
2051	23	2026-04-18	t
2052	23	2026-04-19	f
2053	23	2026-04-20	t
2054	23	2026-04-21	t
2055	23	2026-04-22	f
2056	23	2026-04-23	f
2057	23	2026-04-24	t
2058	23	2026-04-25	t
2059	23	2026-04-26	f
2060	23	2026-04-27	t
2061	23	2026-04-28	t
2062	23	2026-04-29	t
2063	23	2026-04-30	t
2064	23	2026-05-01	t
2065	23	2026-05-02	t
2066	23	2026-05-03	t
2067	23	2026-05-04	f
2068	23	2026-05-05	f
2069	23	2026-05-06	t
2070	23	2026-05-07	t
2071	24	2026-02-07	t
2072	24	2026-02-08	t
2073	24	2026-02-09	f
2074	24	2026-02-10	t
2075	24	2026-02-11	t
2076	24	2026-02-12	t
2077	24	2026-02-13	t
2078	24	2026-02-14	t
2079	24	2026-02-15	f
2080	24	2026-02-16	f
2081	24	2026-02-17	f
2082	24	2026-02-18	f
2083	24	2026-02-19	f
2084	24	2026-02-20	t
2085	24	2026-02-21	t
2086	24	2026-02-22	t
2087	24	2026-02-23	t
2088	24	2026-02-24	f
2089	24	2026-02-25	t
2090	24	2026-02-26	t
2091	24	2026-02-27	f
2092	24	2026-02-28	f
2093	24	2026-03-01	t
2094	24	2026-03-02	t
2095	24	2026-03-03	f
2096	24	2026-03-04	t
2097	24	2026-03-05	t
2098	24	2026-03-06	t
2099	24	2026-03-07	t
2100	24	2026-03-08	t
2101	24	2026-03-09	t
2102	24	2026-03-10	t
2103	24	2026-03-11	f
2104	24	2026-03-12	f
2105	24	2026-03-13	t
2106	24	2026-03-14	f
2107	24	2026-03-15	t
2108	24	2026-03-16	t
2109	24	2026-03-17	t
2110	24	2026-03-18	t
2111	24	2026-03-19	t
2112	24	2026-03-20	t
2113	24	2026-03-21	t
2114	24	2026-03-22	t
2115	24	2026-03-23	t
2116	24	2026-03-24	f
2117	24	2026-03-25	t
2118	24	2026-03-26	t
2119	24	2026-03-27	t
2120	24	2026-03-28	t
2121	24	2026-03-29	t
2122	24	2026-03-30	t
2123	24	2026-03-31	t
2124	24	2026-04-01	f
2125	24	2026-04-02	f
2126	24	2026-04-03	t
2127	24	2026-04-04	t
2128	24	2026-04-05	t
2129	24	2026-04-06	t
2130	24	2026-04-07	t
2131	24	2026-04-08	t
2132	24	2026-04-09	f
2133	24	2026-04-10	t
2134	24	2026-04-11	t
2135	24	2026-04-12	t
2136	24	2026-04-13	f
2137	24	2026-04-14	t
2138	24	2026-04-15	t
2139	24	2026-04-16	t
2140	24	2026-04-17	t
2141	24	2026-04-18	t
2142	24	2026-04-19	t
2143	24	2026-04-20	t
2144	24	2026-04-21	t
2145	24	2026-04-22	f
2146	24	2026-04-23	t
2147	24	2026-04-24	t
2148	24	2026-04-25	f
2149	24	2026-04-26	t
2150	24	2026-04-27	t
2151	24	2026-04-28	t
2152	24	2026-04-29	t
2153	24	2026-04-30	t
2154	24	2026-05-01	t
2155	24	2026-05-02	t
2156	24	2026-05-03	t
2157	24	2026-05-04	t
2158	24	2026-05-05	t
2159	24	2026-05-06	t
2160	24	2026-05-07	t
2161	25	2026-02-07	t
2162	25	2026-02-08	t
2163	25	2026-02-09	t
2164	25	2026-02-10	f
2165	25	2026-02-11	t
2166	25	2026-02-12	t
2167	25	2026-02-13	f
2168	25	2026-02-14	t
2169	25	2026-02-15	f
2170	25	2026-02-16	f
2171	25	2026-02-17	t
2172	25	2026-02-18	t
2173	25	2026-02-19	t
2174	25	2026-02-20	f
2175	25	2026-02-21	t
2176	25	2026-02-22	t
2177	25	2026-02-23	f
2178	25	2026-02-24	f
2179	25	2026-02-25	f
2180	25	2026-02-26	t
2181	25	2026-02-27	t
2182	25	2026-02-28	f
2183	25	2026-03-01	t
2184	25	2026-03-02	f
2185	25	2026-03-03	f
2186	25	2026-03-04	f
2187	25	2026-03-05	t
2188	25	2026-03-06	f
2189	25	2026-03-07	t
2190	25	2026-03-08	t
2191	25	2026-03-09	t
2192	25	2026-03-10	t
2193	25	2026-03-11	t
2194	25	2026-03-12	t
2195	25	2026-03-13	t
2196	25	2026-03-14	t
2197	25	2026-03-15	t
2198	25	2026-03-16	f
2199	25	2026-03-17	t
2200	25	2026-03-18	f
2201	25	2026-03-19	f
2202	25	2026-03-20	t
2203	25	2026-03-21	t
2204	25	2026-03-22	f
2205	25	2026-03-23	t
2206	25	2026-03-24	t
2207	25	2026-03-25	f
2208	25	2026-03-26	f
2209	25	2026-03-27	t
2210	25	2026-03-28	f
2211	25	2026-03-29	f
2212	25	2026-03-30	t
2213	25	2026-03-31	t
2214	25	2026-04-01	t
2215	25	2026-04-02	f
2216	25	2026-04-03	t
2217	25	2026-04-04	t
2218	25	2026-04-05	t
2219	25	2026-04-06	t
2220	25	2026-04-07	t
2221	25	2026-04-08	t
2222	25	2026-04-09	t
2223	25	2026-04-10	t
2224	25	2026-04-11	t
2225	25	2026-04-12	t
2226	25	2026-04-13	t
2227	25	2026-04-14	t
2228	25	2026-04-15	f
2229	25	2026-04-16	t
2230	25	2026-04-17	t
2231	25	2026-04-18	t
2232	25	2026-04-19	t
2233	25	2026-04-20	t
2234	25	2026-04-21	f
2235	25	2026-04-22	f
2236	25	2026-04-23	t
2237	25	2026-04-24	t
2238	25	2026-04-25	f
2239	25	2026-04-26	t
2240	25	2026-04-27	f
2241	25	2026-04-28	t
2242	25	2026-04-29	t
2243	25	2026-04-30	t
2244	25	2026-05-01	t
2245	25	2026-05-02	t
2246	25	2026-05-03	t
2247	25	2026-05-04	f
2248	25	2026-05-05	t
2249	25	2026-05-06	f
2250	25	2026-05-07	t
2251	26	2026-02-07	t
2252	26	2026-02-08	t
2253	26	2026-02-09	f
2254	26	2026-02-10	f
2255	26	2026-02-11	f
2256	26	2026-02-12	f
2257	26	2026-02-13	f
2258	26	2026-02-14	f
2259	26	2026-02-15	t
2260	26	2026-02-16	t
2261	26	2026-02-17	t
2262	26	2026-02-18	t
2263	26	2026-02-19	t
2264	26	2026-02-20	t
2265	26	2026-02-21	f
2266	26	2026-02-22	t
2267	26	2026-02-23	t
2268	26	2026-02-24	t
2269	26	2026-02-25	t
2270	26	2026-02-26	f
2271	26	2026-02-27	f
2272	26	2026-02-28	t
2273	26	2026-03-01	f
2274	26	2026-03-02	t
2275	26	2026-03-03	t
2276	26	2026-03-04	t
2277	26	2026-03-05	t
2278	26	2026-03-06	f
2279	26	2026-03-07	t
2280	26	2026-03-08	t
2281	26	2026-03-09	t
2282	26	2026-03-10	t
2283	26	2026-03-11	t
2284	26	2026-03-12	f
2285	26	2026-03-13	f
2286	26	2026-03-14	t
2287	26	2026-03-15	t
2288	26	2026-03-16	t
2289	26	2026-03-17	t
2290	26	2026-03-18	f
2291	26	2026-03-19	f
2292	26	2026-03-20	t
2293	26	2026-03-21	t
2294	26	2026-03-22	f
2295	26	2026-03-23	t
2296	26	2026-03-24	t
2297	26	2026-03-25	f
2298	26	2026-03-26	t
2299	26	2026-03-27	f
2300	26	2026-03-28	t
2301	26	2026-03-29	f
2302	26	2026-03-30	t
2303	26	2026-03-31	t
2304	26	2026-04-01	f
2305	26	2026-04-02	f
2306	26	2026-04-03	t
2307	26	2026-04-04	t
2308	26	2026-04-05	t
2309	26	2026-04-06	t
2310	26	2026-04-07	f
2311	26	2026-04-08	t
2312	26	2026-04-09	f
2313	26	2026-04-10	t
2314	26	2026-04-11	t
2315	26	2026-04-12	t
2316	26	2026-04-13	f
2317	26	2026-04-14	t
2318	26	2026-04-15	t
2319	26	2026-04-16	t
2320	26	2026-04-17	t
2321	26	2026-04-18	f
2322	26	2026-04-19	f
2323	26	2026-04-20	t
2324	26	2026-04-21	t
2325	26	2026-04-22	f
2326	26	2026-04-23	t
2327	26	2026-04-24	t
2328	26	2026-04-25	t
2329	26	2026-04-26	t
2330	26	2026-04-27	t
2331	26	2026-04-28	t
2332	26	2026-04-29	t
2333	26	2026-04-30	f
2334	26	2026-05-01	t
2335	26	2026-05-02	t
2336	26	2026-05-03	t
2337	26	2026-05-04	f
2338	26	2026-05-05	t
2339	26	2026-05-06	t
2340	26	2026-05-07	t
2341	27	2026-02-07	f
2342	27	2026-02-08	f
2343	27	2026-02-09	f
2344	27	2026-02-10	f
2345	27	2026-02-11	t
2346	27	2026-02-12	t
2347	27	2026-02-13	f
2348	27	2026-02-14	f
2349	27	2026-02-15	t
2350	27	2026-02-16	t
2351	27	2026-02-17	t
2352	27	2026-02-18	f
2353	27	2026-02-19	t
2354	27	2026-02-20	t
2355	27	2026-02-21	t
2356	27	2026-02-22	f
2357	27	2026-02-23	t
2358	27	2026-02-24	t
2359	27	2026-02-25	t
2360	27	2026-02-26	t
2361	27	2026-02-27	t
2362	27	2026-02-28	t
2363	27	2026-03-01	t
2364	27	2026-03-02	t
2365	27	2026-03-03	t
2366	27	2026-03-04	t
2367	27	2026-03-05	t
2368	27	2026-03-06	t
2369	27	2026-03-07	t
2370	27	2026-03-08	t
2371	27	2026-03-09	f
2372	27	2026-03-10	t
2373	27	2026-03-11	t
2374	27	2026-03-12	f
2375	27	2026-03-13	t
2376	27	2026-03-14	f
2377	27	2026-03-15	t
2378	27	2026-03-16	t
2379	27	2026-03-17	t
2380	27	2026-03-18	t
2381	27	2026-03-19	t
2382	27	2026-03-20	t
2383	27	2026-03-21	t
2384	27	2026-03-22	t
2385	27	2026-03-23	t
2386	27	2026-03-24	t
2387	27	2026-03-25	f
2388	27	2026-03-26	t
2389	27	2026-03-27	f
2390	27	2026-03-28	t
2391	27	2026-03-29	f
2392	27	2026-03-30	t
2393	27	2026-03-31	t
2394	27	2026-04-01	t
2395	27	2026-04-02	t
2396	27	2026-04-03	t
2397	27	2026-04-04	f
2398	27	2026-04-05	t
2399	27	2026-04-06	t
2400	27	2026-04-07	t
2401	27	2026-04-08	f
2402	27	2026-04-09	t
2403	27	2026-04-10	f
2404	27	2026-04-11	f
2405	27	2026-04-12	f
2406	27	2026-04-13	t
2407	27	2026-04-14	t
2408	27	2026-04-15	t
2409	27	2026-04-16	t
2410	27	2026-04-17	t
2411	27	2026-04-18	t
2412	27	2026-04-19	t
2413	27	2026-04-20	t
2414	27	2026-04-21	t
2415	27	2026-04-22	t
2416	27	2026-04-23	t
2417	27	2026-04-24	t
2418	27	2026-04-25	f
2419	27	2026-04-26	f
2420	27	2026-04-27	t
2421	27	2026-04-28	t
2422	27	2026-04-29	t
2423	27	2026-04-30	t
2424	27	2026-05-01	t
2425	27	2026-05-02	t
2426	27	2026-05-03	f
2427	27	2026-05-04	f
2428	27	2026-05-05	t
2429	27	2026-05-06	t
2430	27	2026-05-07	t
2431	28	2026-02-07	t
2432	28	2026-02-08	t
2433	28	2026-02-09	f
2434	28	2026-02-10	t
2435	28	2026-02-11	t
2436	28	2026-02-12	t
2437	28	2026-02-13	t
2438	28	2026-02-14	t
2439	28	2026-02-15	f
2440	28	2026-02-16	t
2441	28	2026-02-17	t
2442	28	2026-02-18	f
2443	28	2026-02-19	f
2444	28	2026-02-20	t
2445	28	2026-02-21	t
2446	28	2026-02-22	f
2447	28	2026-02-23	t
2448	28	2026-02-24	t
2449	28	2026-02-25	f
2450	28	2026-02-26	f
2451	28	2026-02-27	f
2452	28	2026-02-28	t
2453	28	2026-03-01	t
2454	28	2026-03-02	f
2455	28	2026-03-03	t
2456	28	2026-03-04	t
2457	28	2026-03-05	f
2458	28	2026-03-06	t
2459	28	2026-03-07	t
2460	28	2026-03-08	t
2461	28	2026-03-09	t
2462	28	2026-03-10	t
2463	28	2026-03-11	t
2464	28	2026-03-12	t
2465	28	2026-03-13	t
2466	28	2026-03-14	t
2467	28	2026-03-15	t
2468	28	2026-03-16	t
2469	28	2026-03-17	t
2470	28	2026-03-18	f
2471	28	2026-03-19	t
2472	28	2026-03-20	f
2473	28	2026-03-21	t
2474	28	2026-03-22	t
2475	28	2026-03-23	f
2476	28	2026-03-24	t
2477	28	2026-03-25	t
2478	28	2026-03-26	f
2479	28	2026-03-27	f
2480	28	2026-03-28	f
2481	28	2026-03-29	t
2482	28	2026-03-30	t
2483	28	2026-03-31	t
2484	28	2026-04-01	t
2485	28	2026-04-02	t
2486	28	2026-04-03	t
2487	28	2026-04-04	t
2488	28	2026-04-05	t
2489	28	2026-04-06	t
2490	28	2026-04-07	f
2491	28	2026-04-08	f
2492	28	2026-04-09	t
2493	28	2026-04-10	t
2494	28	2026-04-11	t
2495	28	2026-04-12	t
2496	28	2026-04-13	t
2497	28	2026-04-14	t
2498	28	2026-04-15	f
2499	28	2026-04-16	t
2500	28	2026-04-17	t
2501	28	2026-04-18	t
2502	28	2026-04-19	t
2503	28	2026-04-20	f
2504	28	2026-04-21	t
2505	28	2026-04-22	f
2506	28	2026-04-23	f
2507	28	2026-04-24	t
2508	28	2026-04-25	t
2509	28	2026-04-26	t
2510	28	2026-04-27	f
2511	28	2026-04-28	t
2512	28	2026-04-29	t
2513	28	2026-04-30	t
2514	28	2026-05-01	t
2515	28	2026-05-02	t
2516	28	2026-05-03	t
2517	28	2026-05-04	t
2518	28	2026-05-05	t
2519	28	2026-05-06	t
2520	28	2026-05-07	t
2521	29	2026-02-07	f
2522	29	2026-02-08	t
2523	29	2026-02-09	t
2524	29	2026-02-10	t
2525	29	2026-02-11	f
2526	29	2026-02-12	f
2527	29	2026-02-13	f
2528	29	2026-02-14	t
2529	29	2026-02-15	f
2530	29	2026-02-16	t
2531	29	2026-02-17	f
2532	29	2026-02-18	t
2533	29	2026-02-19	t
2534	29	2026-02-20	t
2535	29	2026-02-21	t
2536	29	2026-02-22	t
2537	29	2026-02-23	t
2538	29	2026-02-24	t
2539	29	2026-02-25	t
2540	29	2026-02-26	t
2541	29	2026-02-27	t
2542	29	2026-02-28	f
2543	29	2026-03-01	t
2544	29	2026-03-02	t
2545	29	2026-03-03	t
2546	29	2026-03-04	f
2547	29	2026-03-05	f
2548	29	2026-03-06	t
2549	29	2026-03-07	f
2550	29	2026-03-08	f
2551	29	2026-03-09	t
2552	29	2026-03-10	t
2553	29	2026-03-11	t
2554	29	2026-03-12	t
2555	29	2026-03-13	f
2556	29	2026-03-14	t
2557	29	2026-03-15	t
2558	29	2026-03-16	t
2559	29	2026-03-17	t
2560	29	2026-03-18	t
2561	29	2026-03-19	t
2562	29	2026-03-20	t
2563	29	2026-03-21	t
2564	29	2026-03-22	t
2565	29	2026-03-23	f
2566	29	2026-03-24	f
2567	29	2026-03-25	f
2568	29	2026-03-26	t
2569	29	2026-03-27	t
2570	29	2026-03-28	f
2571	29	2026-03-29	t
2572	29	2026-03-30	f
2573	29	2026-03-31	t
2574	29	2026-04-01	t
2575	29	2026-04-02	t
2576	29	2026-04-03	f
2577	29	2026-04-04	t
2578	29	2026-04-05	t
2579	29	2026-04-06	t
2580	29	2026-04-07	t
2581	29	2026-04-08	t
2582	29	2026-04-09	f
2583	29	2026-04-10	t
2584	29	2026-04-11	f
2585	29	2026-04-12	t
2586	29	2026-04-13	t
2587	29	2026-04-14	f
2588	29	2026-04-15	t
2589	29	2026-04-16	t
2590	29	2026-04-17	t
2591	29	2026-04-18	t
2592	29	2026-04-19	t
2593	29	2026-04-20	t
2594	29	2026-04-21	t
2595	29	2026-04-22	t
2596	29	2026-04-23	t
2597	29	2026-04-24	t
2598	29	2026-04-25	t
2599	29	2026-04-26	t
2600	29	2026-04-27	t
2601	29	2026-04-28	t
2602	29	2026-04-29	f
2603	29	2026-04-30	t
2604	29	2026-05-01	t
2605	29	2026-05-02	t
2606	29	2026-05-03	f
2607	29	2026-05-04	t
2608	29	2026-05-05	f
2609	29	2026-05-06	t
2610	29	2026-05-07	t
2611	30	2026-02-07	t
2612	30	2026-02-08	t
2613	30	2026-02-09	t
2614	30	2026-02-10	t
2615	30	2026-02-11	t
2616	30	2026-02-12	t
2617	30	2026-02-13	t
2618	30	2026-02-14	f
2619	30	2026-02-15	t
2620	30	2026-02-16	t
2621	30	2026-02-17	t
2622	30	2026-02-18	t
2623	30	2026-02-19	f
2624	30	2026-02-20	f
2625	30	2026-02-21	t
2626	30	2026-02-22	t
2627	30	2026-02-23	t
2628	30	2026-02-24	t
2629	30	2026-02-25	t
2630	30	2026-02-26	t
2631	30	2026-02-27	t
2632	30	2026-02-28	t
2633	30	2026-03-01	t
2634	30	2026-03-02	f
2635	30	2026-03-03	t
2636	30	2026-03-04	t
2637	30	2026-03-05	t
2638	30	2026-03-06	t
2639	30	2026-03-07	t
2640	30	2026-03-08	t
2641	30	2026-03-09	t
2642	30	2026-03-10	t
2643	30	2026-03-11	t
2644	30	2026-03-12	t
2645	30	2026-03-13	t
2646	30	2026-03-14	f
2647	30	2026-03-15	t
2648	30	2026-03-16	t
2649	30	2026-03-17	t
2650	30	2026-03-18	f
2651	30	2026-03-19	t
2652	30	2026-03-20	t
2653	30	2026-03-21	f
2654	30	2026-03-22	f
2655	30	2026-03-23	t
2656	30	2026-03-24	t
2657	30	2026-03-25	t
2658	30	2026-03-26	t
2659	30	2026-03-27	t
2660	30	2026-03-28	f
2661	30	2026-03-29	f
2662	30	2026-03-30	t
2663	30	2026-03-31	f
2664	30	2026-04-01	t
2665	30	2026-04-02	t
2666	30	2026-04-03	t
2667	30	2026-04-04	f
2668	30	2026-04-05	f
2669	30	2026-04-06	t
2670	30	2026-04-07	t
2671	30	2026-04-08	t
2672	30	2026-04-09	f
2673	30	2026-04-10	t
2674	30	2026-04-11	f
2675	30	2026-04-12	t
2676	30	2026-04-13	t
2677	30	2026-04-14	f
2678	30	2026-04-15	t
2679	30	2026-04-16	t
2680	30	2026-04-17	t
2681	30	2026-04-18	f
2682	30	2026-04-19	t
2683	30	2026-04-20	t
2684	30	2026-04-21	t
2685	30	2026-04-22	f
2686	30	2026-04-23	t
2687	30	2026-04-24	t
2688	30	2026-04-25	t
2689	30	2026-04-26	t
2690	30	2026-04-27	t
2691	30	2026-04-28	f
2692	30	2026-04-29	t
2693	30	2026-04-30	t
2694	30	2026-05-01	t
2695	30	2026-05-02	t
2696	30	2026-05-03	f
2697	30	2026-05-04	t
2698	30	2026-05-05	t
2699	30	2026-05-06	f
2700	30	2026-05-07	t
2701	31	2026-02-07	t
2702	31	2026-02-08	t
2703	31	2026-02-09	t
2704	31	2026-02-10	t
2705	31	2026-02-11	f
2706	31	2026-02-12	t
2707	31	2026-02-13	t
2708	31	2026-02-14	t
2709	31	2026-02-15	t
2710	31	2026-02-16	t
2711	31	2026-02-17	t
2712	31	2026-02-18	f
2713	31	2026-02-19	f
2714	31	2026-02-20	t
2715	31	2026-02-21	f
2716	31	2026-02-22	t
2717	31	2026-02-23	f
2718	31	2026-02-24	t
2719	31	2026-02-25	t
2720	31	2026-02-26	t
2721	31	2026-02-27	t
2722	31	2026-02-28	t
2723	31	2026-03-01	f
2724	31	2026-03-02	f
2725	31	2026-03-03	t
2726	31	2026-03-04	t
2727	31	2026-03-05	f
2728	31	2026-03-06	t
2729	31	2026-03-07	t
2730	31	2026-03-08	t
2731	31	2026-03-09	t
2732	31	2026-03-10	f
2733	31	2026-03-11	t
2734	31	2026-03-12	t
2735	31	2026-03-13	t
2736	31	2026-03-14	t
2737	31	2026-03-15	t
2738	31	2026-03-16	t
2739	31	2026-03-17	t
2740	31	2026-03-18	t
2741	31	2026-03-19	t
2742	31	2026-03-20	t
2743	31	2026-03-21	f
2744	31	2026-03-22	t
2745	31	2026-03-23	t
2746	31	2026-03-24	f
2747	31	2026-03-25	t
2748	31	2026-03-26	t
2749	31	2026-03-27	t
2750	31	2026-03-28	t
2751	31	2026-03-29	f
2752	31	2026-03-30	t
2753	31	2026-03-31	t
2754	31	2026-04-01	t
2755	31	2026-04-02	t
2756	31	2026-04-03	f
2757	31	2026-04-04	f
2758	31	2026-04-05	t
2759	31	2026-04-06	t
2760	31	2026-04-07	t
2761	31	2026-04-08	f
2762	31	2026-04-09	f
2763	31	2026-04-10	t
2764	31	2026-04-11	t
2765	31	2026-04-12	f
2766	31	2026-04-13	f
2767	31	2026-04-14	t
2768	31	2026-04-15	t
2769	31	2026-04-16	t
2770	31	2026-04-17	f
2771	31	2026-04-18	t
2772	31	2026-04-19	t
2773	31	2026-04-20	t
2774	31	2026-04-21	f
2775	31	2026-04-22	f
2776	31	2026-04-23	t
2777	31	2026-04-24	f
2778	31	2026-04-25	t
2779	31	2026-04-26	t
2780	31	2026-04-27	t
2781	31	2026-04-28	t
2782	31	2026-04-29	f
2783	31	2026-04-30	t
2784	31	2026-05-01	t
2785	31	2026-05-02	t
2786	31	2026-05-03	t
2787	31	2026-05-04	f
2788	31	2026-05-05	t
2789	31	2026-05-06	f
2790	31	2026-05-07	t
2791	32	2026-02-07	t
2792	32	2026-02-08	t
2793	32	2026-02-09	t
2794	32	2026-02-10	f
2795	32	2026-02-11	f
2796	32	2026-02-12	t
2797	32	2026-02-13	t
2798	32	2026-02-14	f
2799	32	2026-02-15	t
2800	32	2026-02-16	f
2801	32	2026-02-17	t
2802	32	2026-02-18	t
2803	32	2026-02-19	t
2804	32	2026-02-20	t
2805	32	2026-02-21	t
2806	32	2026-02-22	t
2807	32	2026-02-23	t
2808	32	2026-02-24	t
2809	32	2026-02-25	t
2810	32	2026-02-26	t
2811	32	2026-02-27	t
2812	32	2026-02-28	t
2813	32	2026-03-01	t
2814	32	2026-03-02	t
2815	32	2026-03-03	f
2816	32	2026-03-04	t
2817	32	2026-03-05	f
2818	32	2026-03-06	t
2819	32	2026-03-07	t
2820	32	2026-03-08	t
2821	32	2026-03-09	t
2822	32	2026-03-10	t
2823	32	2026-03-11	t
2824	32	2026-03-12	t
2825	32	2026-03-13	t
2826	32	2026-03-14	t
2827	32	2026-03-15	t
2828	32	2026-03-16	t
2829	32	2026-03-17	f
2830	32	2026-03-18	t
2831	32	2026-03-19	t
2832	32	2026-03-20	t
2833	32	2026-03-21	t
2834	32	2026-03-22	t
2835	32	2026-03-23	t
2836	32	2026-03-24	f
2837	32	2026-03-25	t
2838	32	2026-03-26	f
2839	32	2026-03-27	t
2840	32	2026-03-28	t
2841	32	2026-03-29	t
2842	32	2026-03-30	t
2843	32	2026-03-31	f
2844	32	2026-04-01	t
2845	32	2026-04-02	t
2846	32	2026-04-03	f
2847	32	2026-04-04	t
2848	32	2026-04-05	t
2849	32	2026-04-06	f
2850	32	2026-04-07	f
2851	32	2026-04-08	t
2852	32	2026-04-09	t
2853	32	2026-04-10	f
2854	32	2026-04-11	t
2855	32	2026-04-12	t
2856	32	2026-04-13	t
2857	32	2026-04-14	t
2858	32	2026-04-15	t
2859	32	2026-04-16	t
2860	32	2026-04-17	t
2861	32	2026-04-18	t
2862	32	2026-04-19	t
2863	32	2026-04-20	t
2864	32	2026-04-21	t
2865	32	2026-04-22	t
2866	32	2026-04-23	t
2867	32	2026-04-24	t
2868	32	2026-04-25	t
2869	32	2026-04-26	t
2870	32	2026-04-27	t
2871	32	2026-04-28	t
2872	32	2026-04-29	t
2873	32	2026-04-30	t
2874	32	2026-05-01	t
2875	32	2026-05-02	t
2876	32	2026-05-03	t
2877	32	2026-05-04	f
2878	32	2026-05-05	t
2879	32	2026-05-06	t
2880	32	2026-05-07	t
2881	33	2026-02-07	t
2882	33	2026-02-08	t
2883	33	2026-02-09	t
2884	33	2026-02-10	t
2885	33	2026-02-11	t
2886	33	2026-02-12	t
2887	33	2026-02-13	f
2888	33	2026-02-14	t
2889	33	2026-02-15	t
2890	33	2026-02-16	t
2891	33	2026-02-17	t
2892	33	2026-02-18	t
2893	33	2026-02-19	t
2894	33	2026-02-20	t
2895	33	2026-02-21	t
2896	33	2026-02-22	t
2897	33	2026-02-23	t
2898	33	2026-02-24	t
2899	33	2026-02-25	t
2900	33	2026-02-26	t
2901	33	2026-02-27	t
2902	33	2026-02-28	t
2903	33	2026-03-01	t
2904	33	2026-03-02	f
2905	33	2026-03-03	t
2906	33	2026-03-04	t
2907	33	2026-03-05	t
2908	33	2026-03-06	t
2909	33	2026-03-07	f
2910	33	2026-03-08	t
2911	33	2026-03-09	t
2912	33	2026-03-10	t
2913	33	2026-03-11	t
2914	33	2026-03-12	t
2915	33	2026-03-13	t
2916	33	2026-03-14	t
2917	33	2026-03-15	f
2918	33	2026-03-16	t
2919	33	2026-03-17	f
2920	33	2026-03-18	f
2921	33	2026-03-19	t
2922	33	2026-03-20	t
2923	33	2026-03-21	t
2924	33	2026-03-22	t
2925	33	2026-03-23	t
2926	33	2026-03-24	t
2927	33	2026-03-25	t
2928	33	2026-03-26	f
2929	33	2026-03-27	t
2930	33	2026-03-28	t
2931	33	2026-03-29	t
2932	33	2026-03-30	f
2933	33	2026-03-31	t
2934	33	2026-04-01	t
2935	33	2026-04-02	f
2936	33	2026-04-03	t
2937	33	2026-04-04	t
2938	33	2026-04-05	t
2939	33	2026-04-06	t
2940	33	2026-04-07	f
2941	33	2026-04-08	t
2942	33	2026-04-09	t
2943	33	2026-04-10	f
2944	33	2026-04-11	t
2945	33	2026-04-12	t
2946	33	2026-04-13	t
2947	33	2026-04-14	t
2948	33	2026-04-15	f
2949	33	2026-04-16	f
2950	33	2026-04-17	t
2951	33	2026-04-18	f
2952	33	2026-04-19	f
2953	33	2026-04-20	t
2954	33	2026-04-21	t
2955	33	2026-04-22	f
2956	33	2026-04-23	f
2957	33	2026-04-24	t
2958	33	2026-04-25	f
2959	33	2026-04-26	t
2960	33	2026-04-27	t
2961	33	2026-04-28	t
2962	33	2026-04-29	t
2963	33	2026-04-30	t
2964	33	2026-05-01	t
2965	33	2026-05-02	f
2966	33	2026-05-03	t
2967	33	2026-05-04	t
2968	33	2026-05-05	t
2969	33	2026-05-06	f
2970	33	2026-05-07	t
2971	34	2026-02-07	t
2972	34	2026-02-08	t
2973	34	2026-02-09	t
2974	34	2026-02-10	t
2975	34	2026-02-11	f
2976	34	2026-02-12	t
2977	34	2026-02-13	t
2978	34	2026-02-14	t
2979	34	2026-02-15	t
2980	34	2026-02-16	f
2981	34	2026-02-17	f
2982	34	2026-02-18	t
2983	34	2026-02-19	t
2984	34	2026-02-20	t
2985	34	2026-02-21	t
2986	34	2026-02-22	t
2987	34	2026-02-23	t
2988	34	2026-02-24	t
2989	34	2026-02-25	t
2990	34	2026-02-26	t
2991	34	2026-02-27	t
2992	34	2026-02-28	t
2993	34	2026-03-01	t
2994	34	2026-03-02	t
2995	34	2026-03-03	t
2996	34	2026-03-04	f
2997	34	2026-03-05	t
2998	34	2026-03-06	t
2999	34	2026-03-07	t
3000	34	2026-03-08	t
3001	34	2026-03-09	t
3002	34	2026-03-10	t
3003	34	2026-03-11	f
3004	34	2026-03-12	t
3005	34	2026-03-13	t
3006	34	2026-03-14	t
3007	34	2026-03-15	t
3008	34	2026-03-16	t
3009	34	2026-03-17	t
3010	34	2026-03-18	t
3011	34	2026-03-19	t
3012	34	2026-03-20	t
3013	34	2026-03-21	t
3014	34	2026-03-22	t
3015	34	2026-03-23	t
3016	34	2026-03-24	t
3017	34	2026-03-25	f
3018	34	2026-03-26	t
3019	34	2026-03-27	f
3020	34	2026-03-28	t
3021	34	2026-03-29	t
3022	34	2026-03-30	t
3023	34	2026-03-31	f
3024	34	2026-04-01	t
3025	34	2026-04-02	t
3026	34	2026-04-03	f
3027	34	2026-04-04	t
3028	34	2026-04-05	f
3029	34	2026-04-06	t
3030	34	2026-04-07	t
3031	34	2026-04-08	t
3032	34	2026-04-09	t
3033	34	2026-04-10	f
3034	34	2026-04-11	t
3035	34	2026-04-12	t
3036	34	2026-04-13	t
3037	34	2026-04-14	t
3038	34	2026-04-15	t
3039	34	2026-04-16	f
3040	34	2026-04-17	f
3041	34	2026-04-18	t
3042	34	2026-04-19	f
3043	34	2026-04-20	t
3044	34	2026-04-21	f
3045	34	2026-04-22	t
3046	34	2026-04-23	t
3047	34	2026-04-24	t
3048	34	2026-04-25	t
3049	34	2026-04-26	t
3050	34	2026-04-27	t
3051	34	2026-04-28	t
3052	34	2026-04-29	t
3053	34	2026-04-30	t
3054	34	2026-05-01	t
3055	34	2026-05-02	t
3056	34	2026-05-03	t
3057	34	2026-05-04	f
3058	34	2026-05-05	t
3059	34	2026-05-06	t
3060	34	2026-05-07	t
\.


--
-- Data for Name: rooms; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.rooms (id, hostel_id, room_type, price, capacity, available_units, is_available, created_at) FROM stdin;
1	1	single	7471	1	2	t	2025-10-30 15:26:53.050732
2	1	bed_sitter	16121	1	1	t	2025-09-01 15:26:53.051037
3	1	bed_sitter	14535	1	3	t	2025-09-20 15:26:53.051213
4	1	studio	19514	1	3	t	2025-08-17 15:26:53.051373
5	1	studio	19401	1	1	t	2025-10-28 15:26:53.051528
6	1	single	8311	1	2	t	2025-10-04 15:26:53.051681
7	1	studio	19073	1	2	t	2025-10-01 15:26:53.052175
8	1	studio	21811	1	1	t	2025-12-03 15:26:53.052685
9	1	studio	20948	1	3	f	2025-12-29 15:26:53.052862
10	1	bed_sitter	15158	1	0	t	2025-10-04 15:26:53.053018
11	1	single	7974	1	2	t	2025-11-03 15:26:53.053191
12	2	bed_sitter	14645	1	3	f	2025-11-10 15:26:53.074905
13	2	studio	19868	1	3	t	2025-10-02 15:26:53.075041
14	2	single	7387	1	3	t	2025-12-05 15:26:53.07512
15	2	double	13736	2	3	f	2025-09-07 15:26:53.075192
16	2	studio	20590	1	2	t	2025-10-07 15:26:53.075262
17	3	bed_sitter	15878	1	2	f	2025-10-29 15:26:53.084233
18	3	bed_sitter	15335	1	2	f	2025-09-08 15:26:53.084489
19	3	single	8855	1	2	t	2025-09-09 15:26:53.084873
20	3	studio	21970	1	1	t	2025-09-12 15:26:53.085009
21	3	double	13722	2	1	t	2025-11-01 15:26:53.085094
22	3	single	7431	1	0	t	2025-10-28 15:26:53.085169
23	3	studio	19747	1	0	f	2025-11-07 15:26:53.085243
24	3	studio	19274	1	1	t	2025-10-26 15:26:53.085317
25	4	bed_sitter	15055	1	1	t	2025-08-18 15:26:53.099234
26	4	double	11641	2	1	t	2026-01-02 15:26:53.099431
27	4	studio	20103	1	1	t	2025-10-16 15:26:53.099521
28	4	bed_sitter	14844	1	0	t	2025-11-27 15:26:53.099599
29	4	bed_sitter	15662	1	0	t	2025-08-16 15:26:53.099674
30	4	double	11585	2	1	f	2025-11-04 15:26:53.099748
31	4	studio	21122	1	1	f	2025-11-30 15:26:53.09982
32	4	double	13486	2	3	t	2025-10-13 15:26:53.099893
33	4	single	9591	1	0	t	2025-12-01 15:26:53.099965
34	4	studio	19789	1	1	t	2025-10-16 15:26:53.100038
\.


--
-- Data for Name: settings; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.settings (id, key, value, updated_at) FROM stdin;
1	commission_rate	10	2026-02-07 15:26:52.896914
2	min_booking_days	30	2026-02-07 15:26:52.897248
3	max_booking_days	365	2026-02-07 15:26:52.897362
4	auto_cancel_hours	24	2026-02-07 15:26:52.897422
5	app_name	HostelHub	2026-02-07 15:26:52.897569
6	contact_email	support@hostelhub.com	2026-02-07 15:26:52.897627
7	contact_phone	+254700123456	2026-02-07 15:26:52.897667
8	currency	KES	2026-02-07 15:26:52.897705
9	tax_rate	16	2026-02-07 15:26:52.897742
10	max_hostels_per_host	5	2026-02-07 15:26:52.897779
11	review_window_days	14	2026-02-07 15:26:52.897816
12	refund_window_days	7	2026-02-07 15:26:52.897855
13	maintenance_mode	false	2026-02-07 15:26:52.897892
\.


--
-- Data for Name: support_tickets; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.support_tickets (id, user_id, subject, message, status, created_at) FROM stdin;
1	7	General inquiry	I can't log into my account	open	2026-01-25 15:26:54.909477
2	8	General inquiry	Question about your services	in_progress	2026-01-03 15:26:54.917933
\.


--
-- Data for Name: tokens; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.tokens (id, user_id, token, token_type, expires_at, created_at) FROM stdin;
2	9	d6524a74-cc4d-4d79-97a8-4b84dd20ebd2	revoked	2026-02-07 12:41:48.454636	2026-02-07 12:41:48.456104
3	9	f67d2232-650f-4ca7-8e10-9e8a6e2ed2e6	password_reset	2026-02-07 13:49:16.890643	2026-02-07 12:49:16.899256
5	9	2ff4cf96-cb81-4ac2-814c-3a67ee9b9b7c	revoked	2026-02-07 13:08:21.672787	2026-02-07 13:08:21.676093
6	10	5c4bbca3-c3f2-441b-b39e-d7e0556e53ad	email_verification	2026-02-08 13:28:55.404787	2026-02-07 13:28:55.406535
7	10	6bfd4826-4d20-40f2-b81c-6ff179255dd5	revoked	2026-02-07 13:42:09.258819	2026-02-07 13:42:09.260425
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.users (id, first_name, last_name, email, password_hash, phone, role, is_verified, last_login_at, login_count, created_at, updated_at) FROM stdin;
1	Admin	System	admin@hostelhub.com	scrypt:32768:8:1$xjhMFTSx119duNvP$844beceb3565a5bf70c9a06a0dafa1c70f315236e2a547a0e248f4cce4fcb277ef5938cacf59006283bef0eae37cd3290dd5ce2f1e3bd4ce6e34d47d46e2656b	+254700000001	admin	t	2026-02-06 15:26:51.545465	50	2025-11-04 15:26:51.691057	2026-02-07 15:26:50.946251
2	John	Kamau	john.kamau@example.com	scrypt:32768:8:1$bC2ft0yL5jVtLM7E$93c48d1fafd0ed287470cc87a93a838dcd592dd53ba3e46139bb12d5756b88b9c00591dc8b47ef13dbdeb642c5ca1ab90736c796af26a954b2406dd1a42493ec	+254711222333	host	t	2026-02-04 15:26:51.545486	25	2025-12-29 15:26:51.809539	2026-02-07 15:26:50.946251
3	Sarah	Mwangi	sarah.m@example.com	scrypt:32768:8:1$AyCVMNElWZdhdW5L$66c300ee8932b3e18d25921e8c839bd2c5875fd94135ed30165c605aafbc1f2418386c373d4c81446fcd85590654a21cee0103d6ecd671b12856490af724e572	+254722333444	host	t	2026-02-02 15:26:51.545492	15	2025-11-17 15:26:51.978334	2026-02-07 15:26:50.946251
4	David	Ochieng	david.o@example.com	scrypt:32768:8:1$rxxjQPdWe4NET91l$b393d53a2d005dcd46f91575dcba30861412d00b7e8c61b94804293b5e928c320b6ca8d0c0765e430300b15b2d1eceee6cf15afb1196aef666f699e7815bc1f7	+254733444555	host	f	2026-01-28 15:26:51.545497	8	2025-09-24 15:26:52.112391	2026-02-07 15:26:50.946251
5	Alice	Wanjiru	alice.w@student.com	scrypt:32768:8:1$HPSM3UOIzyqiDgzY$22c726455f6b86b0dacb74c9e9a749c8fa9b10697ec07e1c1651222d17588d32f5494aa24ba6b60a87d1f6b3bda68030cf4aacdf8c3f8dbe3cb699a75c8220cb	+254744555666	student	t	2026-02-07 13:26:51.545501	30	2025-09-03 15:26:52.290784	2026-02-07 15:26:50.946251
6	Brian	Omondi	brian.o@student.com	scrypt:32768:8:1$WwXgHGygQVamNGav$0779fe815132fd29d762d03c3ff9cd17ca5efc1bc43f9586e4736672ba1003c1780bd40ce844b12076fde33f97378176bd394ad0116557dd04dd2a0294ab91bc	+254755666777	student	t	2026-02-06 15:26:51.545507	20	2025-08-16 15:26:52.467011	2026-02-07 15:26:50.946251
7	Grace	Akinyi	grace.a@student.com	scrypt:32768:8:1$GELl1ewQXIuz24XM$1d939c6ce7a3b0173d23a30de611a8144ffc3d98dfef4d37e698b47b62ab38a1ac8f6a51fc89fe4d5bca349e6d163c09dae611c9331764cf4c094baefd28340c	+254766777888	student	t	2026-02-03 15:26:51.545511	12	2025-10-31 15:26:52.649078	2026-02-07 15:26:50.946251
8	Peter	Mutiso	peter.m@student.com	scrypt:32768:8:1$QFgxeMDVzlTTq1fr$335135c0410549d01d91899b70f91b0e68f3a1903900ed45c1ad105e33d9e84190bb75ad66b14b1b2dd2494609f8df423b4d12efa494ef2fb48d0fab97a116fe	+254777888999	student	f	2026-01-31 15:26:51.545515	3	2025-10-03 15:26:52.829238	2026-02-07 15:26:50.946251
9	Nelson	Munyua	nelsonmunyua8@gmail.com	$2b$12$n/eIbw.gpOWXYj9rOBSaM.Ud6JA9mA0CLVoNsqaUtJFI4L8/6lFoy	0748442693	host	t	2026-02-07 13:05:54.712666	2	2026-02-07 15:26:13.099096	2026-02-07 15:57:31.944121
10	john	doe	johndoe@gmail.com	$2b$12$86kPq6Dt7DxI5kRLCC8Yx.6S3dQ/aZjXjPironxelxFQaZK0xG8o6	0742368897	admin	f	2026-02-07 13:56:07.711353	2	2026-02-07 16:18:00.360351	2026-02-07 16:54:54.942708
\.


--
-- Data for Name: wishlists; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.wishlists (id, user_id, hostel_id, created_at) FROM stdin;
1	5	1	2026-01-12 15:26:53.613543
2	6	3	2026-01-14 15:26:53.624208
3	6	4	2026-01-23 15:26:53.627958
4	7	2	2026-01-25 15:26:53.634555
5	7	1	2026-01-25 15:26:53.634705
6	8	1	2026-01-18 15:26:53.634799
7	8	2	2026-01-18 15:26:53.634862
\.


--
-- Name: bookings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.bookings_id_seq', 11, true);


--
-- Name: host_earnings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.host_earnings_id_seq', 7, true);


--
-- Name: host_verifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.host_verifications_id_seq', 3, true);


--
-- Name: hostels_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.hostels_id_seq', 4, true);


--
-- Name: notifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.notifications_id_seq', 42, true);


--
-- Name: payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.payments_id_seq', 13, true);


--
-- Name: reviews_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.reviews_id_seq', 2, true);


--
-- Name: room_availability_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.room_availability_id_seq', 3060, true);


--
-- Name: rooms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.rooms_id_seq', 34, true);


--
-- Name: settings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.settings_id_seq', 13, true);


--
-- Name: support_tickets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.support_tickets_id_seq', 2, true);


--
-- Name: tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.tokens_id_seq', 7, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- Name: wishlists_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.wishlists_id_seq', 7, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: bookings pk_bookings; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT pk_bookings PRIMARY KEY (id);


--
-- Name: host_earnings pk_host_earnings; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.host_earnings
    ADD CONSTRAINT pk_host_earnings PRIMARY KEY (id);


--
-- Name: host_verifications pk_host_verifications; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.host_verifications
    ADD CONSTRAINT pk_host_verifications PRIMARY KEY (id);


--
-- Name: hostels pk_hostels; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.hostels
    ADD CONSTRAINT pk_hostels PRIMARY KEY (id);


--
-- Name: notifications pk_notifications; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT pk_notifications PRIMARY KEY (id);


--
-- Name: payments pk_payments; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT pk_payments PRIMARY KEY (id);


--
-- Name: reviews pk_reviews; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT pk_reviews PRIMARY KEY (id);


--
-- Name: room_availability pk_room_availability; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.room_availability
    ADD CONSTRAINT pk_room_availability PRIMARY KEY (id);


--
-- Name: rooms pk_rooms; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT pk_rooms PRIMARY KEY (id);


--
-- Name: settings pk_settings; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.settings
    ADD CONSTRAINT pk_settings PRIMARY KEY (id);


--
-- Name: support_tickets pk_support_tickets; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.support_tickets
    ADD CONSTRAINT pk_support_tickets PRIMARY KEY (id);


--
-- Name: tokens pk_tokens; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.tokens
    ADD CONSTRAINT pk_tokens PRIMARY KEY (id);


--
-- Name: users pk_users; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT pk_users PRIMARY KEY (id);


--
-- Name: wishlists pk_wishlists; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.wishlists
    ADD CONSTRAINT pk_wishlists PRIMARY KEY (id);


--
-- Name: reviews uq_review_booking; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT uq_review_booking UNIQUE (booking_id);


--
-- Name: room_availability uq_room_date; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.room_availability
    ADD CONSTRAINT uq_room_date UNIQUE (room_id, date);


--
-- Name: settings uq_settings_key; Type: CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.settings
    ADD CONSTRAINT uq_settings_key UNIQUE (key);


--
-- Name: ix_payments_reference; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_payments_reference ON public.payments USING btree (reference);


--
-- Name: ix_tokens_token; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_tokens_token ON public.tokens USING btree (token);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_phone; Type: INDEX; Schema: public; Owner: root
--

CREATE UNIQUE INDEX ix_users_phone ON public.users USING btree (phone);


--
-- Name: bookings fk_bookings_room_id_rooms; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT fk_bookings_room_id_rooms FOREIGN KEY (room_id) REFERENCES public.rooms(id);


--
-- Name: bookings fk_bookings_student_id_users; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.bookings
    ADD CONSTRAINT fk_bookings_student_id_users FOREIGN KEY (student_id) REFERENCES public.users(id);


--
-- Name: host_earnings fk_host_earnings_booking_id_bookings; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.host_earnings
    ADD CONSTRAINT fk_host_earnings_booking_id_bookings FOREIGN KEY (booking_id) REFERENCES public.bookings(id);


--
-- Name: host_earnings fk_host_earnings_host_id_users; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.host_earnings
    ADD CONSTRAINT fk_host_earnings_host_id_users FOREIGN KEY (host_id) REFERENCES public.users(id);


--
-- Name: host_verifications fk_host_verifications_host_id_users; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.host_verifications
    ADD CONSTRAINT fk_host_verifications_host_id_users FOREIGN KEY (host_id) REFERENCES public.users(id);


--
-- Name: host_verifications fk_host_verifications_reviewed_by_users; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.host_verifications
    ADD CONSTRAINT fk_host_verifications_reviewed_by_users FOREIGN KEY (reviewed_by) REFERENCES public.users(id);


--
-- Name: hostels fk_hostels_host_id_users; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.hostels
    ADD CONSTRAINT fk_hostels_host_id_users FOREIGN KEY (host_id) REFERENCES public.users(id);


--
-- Name: notifications fk_notifications_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT fk_notifications_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: payments fk_payments_booking_id_bookings; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT fk_payments_booking_id_bookings FOREIGN KEY (booking_id) REFERENCES public.bookings(id);


--
-- Name: reviews fk_reviews_booking_id_bookings; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT fk_reviews_booking_id_bookings FOREIGN KEY (booking_id) REFERENCES public.bookings(id);


--
-- Name: reviews fk_reviews_hostel_id_hostels; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT fk_reviews_hostel_id_hostels FOREIGN KEY (hostel_id) REFERENCES public.hostels(id);


--
-- Name: reviews fk_reviews_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT fk_reviews_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: room_availability fk_room_availability_room_id_rooms; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.room_availability
    ADD CONSTRAINT fk_room_availability_room_id_rooms FOREIGN KEY (room_id) REFERENCES public.rooms(id);


--
-- Name: rooms fk_rooms_hostel_id_hostels; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT fk_rooms_hostel_id_hostels FOREIGN KEY (hostel_id) REFERENCES public.hostels(id);


--
-- Name: support_tickets fk_support_tickets_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.support_tickets
    ADD CONSTRAINT fk_support_tickets_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: tokens fk_tokens_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.tokens
    ADD CONSTRAINT fk_tokens_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: wishlists fk_wishlists_hostel_id_hostels; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.wishlists
    ADD CONSTRAINT fk_wishlists_hostel_id_hostels FOREIGN KEY (hostel_id) REFERENCES public.hostels(id);


--
-- Name: wishlists fk_wishlists_user_id_users; Type: FK CONSTRAINT; Schema: public; Owner: root
--

ALTER TABLE ONLY public.wishlists
    ADD CONSTRAINT fk_wishlists_user_id_users FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict M4M6fOg5WK0VJPXnTGWZsv8KT2R3znDiGUSCuQdYPWF0tGkWQQizHR1gNL7jNA5

