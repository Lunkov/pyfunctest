CREATE SEQUENCE public.schedule_id_seq;
CREATE TABLE public.schedule
(
    id   bigint       NOT NULL DEFAULT nextval('schedule_id_seq'),
    name varchar(255) NOT NULL DEFAULT '',
    cron varchar(255) NOT NULL DEFAULT '',
    PRIMARY KEY (id),
    CONSTRAINT "schedule_name_cron" UNIQUE (name, cron)
);
