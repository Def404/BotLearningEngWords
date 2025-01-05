CREATE DATABASE learning_english_words
    WITH
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;


CREATE SCHEMA IF NOT EXISTS profile;

CREATE TABLE IF NOT EXISTS profile."user"
(
    uid uuid NOT NULL DEFAULT uuid_generate_v4(),
    telegram_user_id bigint NOT NULL,
    telegram_user_name text COLLATE pg_catalog."default" NOT NULL,
    created timestamp with time zone NOT NULL DEFAULT now(),
    modified timestamp with time zone,
    CONSTRAINT user_pkey PRIMARY KEY (uid),
    CONSTRAINT unq_telegram_user_id UNIQUE (telegram_user_id)
)

CREATE TABLE IF NOT EXISTS profile.dictionary
(
    uid uuid NOT NULL DEFAULT uuid_generate_v4(),
    user_uid uuid NOT NULL,
    word text COLLATE pg_catalog."default" NOT NULL,
    translate text[] COLLATE pg_catalog."default",
    created timestamp with time zone NOT NULL DEFAULT now(),
    modified timestamp with time zone,
    CONSTRAINT dictionary_pkey PRIMARY KEY (uid),
    CONSTRAINT dictionary_user_uid_fkey FOREIGN KEY (user_uid)
        REFERENCES profile."user" (uid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)