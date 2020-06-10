CREATE TABLE offers_resender_cron
(
    id           serial primary key,
    operation_id text                     not null,
    row_version  bigint                   not null,
    created_at   timestamp with time zone not null
);

CREATE TABLE offers_resender_stats
(
    operation_id         text                     not null,
    founded_from_elastic bigint                   not null,
    need_update          bigint                   not null,
    not_found_in_db      bigint                   not null,
    created_at           timestamp with time zone not null
);
