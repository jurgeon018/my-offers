create table moderation_alerts
(
    user_id         bigint                   not null primary key,
    last_visit_date timestamp with time zone not null
)