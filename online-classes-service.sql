--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5
-- Dumped by pg_dump version 14.5

-- Started on 2022-10-27 13:45:00

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
-- TOC entry 834 (class 1247 OID 32985)
-- Name: role; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.role AS ENUM (
    'teacher',
    'student'
);


ALTER TYPE public.role OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 210 (class 1259 OID 32969)
-- Name: class; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.class (
    id integer NOT NULL,
    title character varying NOT NULL,
    description character varying,
    teacher integer NOT NULL
);


ALTER TABLE public.class OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 32968)
-- Name: class_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.class ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.class_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 214 (class 1259 OID 33006)
-- Name: class_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.class_user (
    class integer NOT NULL,
    "user" integer NOT NULL
);


ALTER TABLE public.class_user OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 33021)
-- Name: request; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.request (
    class integer NOT NULL,
    "user" integer NOT NULL
);


ALTER TABLE public.request OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 32989)
-- Name: teacher; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teacher (
    user_id integer NOT NULL,
    diplomas character varying[] NOT NULL,
    employment character varying
);


ALTER TABLE public.teacher OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 32977)
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying NOT NULL,
    "firstName" character varying NOT NULL,
    "lastName" character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    phone character varying,
    role public.role NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 32976)
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public."user" ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 3185 (class 2606 OID 32975)
-- Name: class class_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class
    ADD CONSTRAINT class_pkey PRIMARY KEY (id);


--
-- TOC entry 3191 (class 2606 OID 33010)
-- Name: class_user class_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_user
    ADD CONSTRAINT class_user_pkey PRIMARY KEY (class, "user");


--
-- TOC entry 3193 (class 2606 OID 33025)
-- Name: request request_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request
    ADD CONSTRAINT request_pkey PRIMARY KEY (class, "user");


--
-- TOC entry 3189 (class 2606 OID 33000)
-- Name: teacher teacher_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacher
    ADD CONSTRAINT teacher_pkey PRIMARY KEY (user_id);


--
-- TOC entry 3187 (class 2606 OID 32983)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 3196 (class 2606 OID 33011)
-- Name: class_user class; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_user
    ADD CONSTRAINT class FOREIGN KEY (class) REFERENCES public.class(id);


--
-- TOC entry 3198 (class 2606 OID 33026)
-- Name: request class; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request
    ADD CONSTRAINT class FOREIGN KEY (class) REFERENCES public.class(id);


--
-- TOC entry 3194 (class 2606 OID 33001)
-- Name: class teacher; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class
    ADD CONSTRAINT teacher FOREIGN KEY (teacher) REFERENCES public.teacher(user_id) NOT VALID;


--
-- TOC entry 3197 (class 2606 OID 33016)
-- Name: class_user user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.class_user
    ADD CONSTRAINT "user" FOREIGN KEY ("user") REFERENCES public."user"(id);


--
-- TOC entry 3199 (class 2606 OID 33031)
-- Name: request user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.request
    ADD CONSTRAINT "user" FOREIGN KEY ("user") REFERENCES public."user"(id);


--
-- TOC entry 3195 (class 2606 OID 32994)
-- Name: teacher user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacher
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES public."user"(id);


-- Completed on 2022-10-27 13:45:01

--
-- PostgreSQL database dump complete
--

