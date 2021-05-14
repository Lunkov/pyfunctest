CREATE TABLE public.article2 (
    article_id bigserial primary key,
    article_name varchar(20) NOT NULL,
    article_desc text NOT NULL,
    date_added timestamp default NULL
);

CREATE TABLE public.article3 (
    article_id bigserial primary key,
    article_name varchar(20) NOT NULL,
    article_desc text NOT NULL,
    date_added timestamp default NULL
);