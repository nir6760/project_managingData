-- Table: public.users

-- DROP TABLE IF EXISTS public.users;

CREATE TABLE IF NOT EXISTS public.users
(
    id_user character varying COLLATE pg_catalog."default" NOT NULL,
    user_name character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT users_pkey PRIMARY KEY (id_user)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users
    OWNER to postgres;

---------------------------------------------------------------------------------------------

-- Table: public.polls

-- DROP TABLE IF EXISTS public.polls;

CREATE TABLE IF NOT EXISTS public.polls
(
    id_poll character varying COLLATE pg_catalog."default" NOT NULL,
    poll_content character varying COLLATE pg_catalog."default",
    date date,
    CONSTRAINT polls_pkey PRIMARY KEY (id_poll)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.polls
    OWNER to postgres;

---------------------------------------------------------------------------------------------

-- Table: public.admins

-- DROP TABLE IF EXISTS public.admins;

CREATE TABLE IF NOT EXISTS public.admins
(
    id_admin character varying COLLATE pg_catalog."default" NOT NULL,
    admin_name character varying COLLATE pg_catalog."default" NOT NULL,
    hash_password character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT admins_pkey PRIMARY KEY (id_admin)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.admins
    OWNER to postgres;

---------------------------------------------------------------------------------------------

-- Table: public.choices

-- DROP TABLE IF EXISTS public.choices;

CREATE TABLE IF NOT EXISTS public.choices
(
    id_poll character varying COLLATE pg_catalog."default" NOT NULL,
    "number" integer NOT NULL,
    answer character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT choices_pkey PRIMARY KEY (id_poll, "number", answer),
    CONSTRAINT choices_id_poll_fkey FOREIGN KEY (id_poll)
        REFERENCES public.polls (id_poll) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.choices
    OWNER to postgres;
---------------------------------------------------------------------------------------------


-- Table: public.users_polls

-- DROP TABLE IF EXISTS public.users_polls;

CREATE TABLE IF NOT EXISTS public.users_polls
(
    id_user character varying COLLATE pg_catalog."default",
    id_poll character varying COLLATE pg_catalog."default",
    "number" integer,
    CONSTRAINT users_polls_id_poll_fkey FOREIGN KEY (id_poll)
        REFERENCES public.polls (id_poll) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT users_polls_id_user_fkey FOREIGN KEY (id_user)
        REFERENCES public.users (id_user) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.users_polls
    OWNER to postgres;
---------------------------------------------------------------------------------------------


-- Table: public.admins_polls

-- DROP TABLE IF EXISTS public.admins_polls;

CREATE TABLE IF NOT EXISTS public.admins_polls
(
    id_admin character varying COLLATE pg_catalog."default",
    id_poll character varying COLLATE pg_catalog."default",
    CONSTRAINT admins_polls_id_admin_fkey FOREIGN KEY (id_admin)
        REFERENCES public.admins (id_admin) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT admins_polls_id_poll_fkey FOREIGN KEY (id_poll)
        REFERENCES public.polls (id_poll) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.admins_polls
    OWNER to postgres;
---------------------------------------------------------------------------------------------