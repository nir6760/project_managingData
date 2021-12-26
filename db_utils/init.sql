-- Table: public.ADMINS

-- DROP TABLE IF EXISTS public."ADMINS";

CREATE TABLE IF NOT EXISTS public."ADMINS"
(
    id_admin text COLLATE pg_catalog."default" NOT NULL,
    admin_name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "ADMINS_pkey" PRIMARY KEY (id_admin)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."ADMINS"
    OWNER to postgres;


-- **********************************************************************************************************
-- Table: public.POLLS

-- DROP TABLE IF EXISTS public."POLLS";

CREATE TABLE IF NOT EXISTS public."POLLS"
(
    id_poll text COLLATE pg_catalog."default" NOT NULL,
    question text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "POLLS_pkey" PRIMARY KEY (id_poll)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."POLLS"
    OWNER to postgres;

-- **********************************************************************************************************
-- Table: public.USERS

-- DROP TABLE IF EXISTS public."USERS";

CREATE TABLE IF NOT EXISTS public."USERS"
(
    id_user text COLLATE pg_catalog."default" NOT NULL,
    user_name text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "USERS_pkey" PRIMARY KEY (id_user)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."USERS"
    OWNER to postgres;

-- **********************************************************************************************************
-- Table: public.POLLS_ADMINS

-- DROP TABLE IF EXISTS public."POLLS_ADMINS";

CREATE TABLE IF NOT EXISTS public."POLLS_ADMINS"
(
    id_poll text COLLATE pg_catalog."default" NOT NULL,
    id_admin text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "POLLS_ADMINS_pkey" PRIMARY KEY (id_poll, id_admin),
    CONSTRAINT id_admin_fk FOREIGN KEY (id_admin)
        REFERENCES public."ADMINS" (id_admin) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT id_poll_fk FOREIGN KEY (id_poll)
        REFERENCES public."POLLS" (id_poll) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."POLLS_ADMINS"
    OWNER to postgres;