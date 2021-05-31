CREATE TABLE public.job
(
    name        varchar(255) NOT NULL,
    description varchar(255) NOT NULL DEFAULT '',
    last_start  timestamp             DEFAULT CURRENT_TIMESTAMP,
    status      varchar(255) NOT NULL DEFAULT 'WAIT',
    PRIMARY KEY (name)
);
